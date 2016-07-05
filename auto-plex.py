import datetime
import pickle
from flask import Flask, render_template, request, flash
import untangle
import requests
from requests import ConnectTimeout

app = Flask(__name__)

app.secret_key = 'fjas7df98afh879sfh8'

file_name = 'todays-movie-id.txt'
history_file_name = 'history.txt'
section = 1
http_port = 5000

plex_server_ip = '10.0.0.14'
plex_server_port = 32400
plex_server_identifier = '28cff6063535af7fd68b313ed816c6bde08d7e8d'

plex_client_ip = '10.0.0.27'
plex_client_port = 3005
plex_client_identifier = 'c3cf6e7d-46e2-4bf0-bf47-931b80d17a91'


def write_todays_movie(movie_id):
    with open(file_name, 'w') as file:
        file.truncate()
        file.write(movie_id)


def write_history(movies, todays_id, history):
    last_movie = [x for x in movies if x['id'] == todays_id][0]

    today = datetime.datetime.now()
    if today.hour < 19:
        today = today - datetime.timedelta(days=1)

    if len(history) == 0 or history[0]['title'] != last_movie['title']:
        history.insert(0, {"day": today.date(), "title": last_movie['title']})
        pickle.dump(history, open(history_file_name, "wb"))


@app.route('/', methods=['GET', 'POST'])
def index():
    file = open(file_name, 'r')
    todays_id = file.read()

    movies = untangle.parse('http://{plex_server_ip}:{plex_server_port}/library/sections/{section}/all'.format(
        plex_server_ip=plex_server_ip, plex_server_port=plex_server_port, section=section))
    movies = [{'id': movie['ratingKey'], 'title': movie['title'], 'art': movie['thumb']} for movie in
              movies.MediaContainer.Video]

    try:
        history = pickle.load(open(history_file_name, "rb"))
    except EOFError:
        history = []

    if request.method == 'POST':
        write_todays_movie(request.form['movie'])

        write_history(movies, todays_id, history)

        todays_id = request.form['movie']

        todays_movie = [x for x in movies if x['id'] == todays_id][0]

        if 'play' in request.form:
            try:
                url = "http://{plex_client_ip}:{plex_client_port}/player/playback/stop" \
                    .format(plex_client_ip=plex_client_ip, plex_client_port=plex_client_port)

                requests.get(url, timeout=10)

                url = "http://{plex_client_ip}:{plex_client_port}/player/playback/playMedia?key=/library/metadata/{movie_id}" \
                      "&address={plex_server_ip}&port={plex_server_port}&X-Plex-Client-Identifier={plex_client_identifier}" \
                      "&machineIdentifier={plex_server_identifier}&protocol=http" \
                      "&path=http://{plex_server_ip}:{plex_server_port}/library/metadata/{movie_id}" \
                    .format(plex_client_ip=plex_client_ip, plex_client_port=plex_client_port,
                            plex_client_identifier=plex_client_identifier,
                            plex_server_ip=plex_server_ip, plex_server_port=plex_server_port,
                            plex_server_identifier=plex_server_identifier,
                            movie_id=todays_id)

                requests.get(url, timeout=10)

                flash('Started playback of movie ' + todays_movie['title'], 'info')
            except (ConnectionError, ConnectTimeout):
                flash('Could not connect to client or server', 'error')
        else:
            flash('Set next movie to ' + todays_movie['title'], 'info')

    context = {
        'movies': movies,
        'todays_id': todays_id,
        'history': history[:20],
        'plex_server_address': "{}:{}".format(plex_server_ip, plex_server_port)
    }

    return render_template('index.html', **context)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=http_port, debug=True, threaded=True)
