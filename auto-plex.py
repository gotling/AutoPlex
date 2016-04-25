import datetime
import pickle
from flask import Flask, render_template, request
import untangle

app = Flask(__name__)

file_name = 'todays-movie-id.txt'
history_file_name = 'history.txt'
plex_server_address = '10.0.0.14:32400'
section = 1
http_port = 5000


def write_todays_movie(movie_id):
    with open(file_name, 'w') as file:
        file.truncate()
        file.write(movie_id)


def write_history(movies, todays_id, history):
    last_movie = [x for x in movies if x['id'] == todays_id][0]

    today = datetime.datetime.now()
    if today.hour < 19:
        today = today - datetime.timedelta(days=1)

    history.insert(0, {"day": today.date(), "title": last_movie['title']})
    pickle.dump(history, open(history_file_name, "wb"))


@app.route('/', methods=['GET', 'POST'])
def index():
    file = open(file_name, 'r')
    todays_id = file.read()

    movies = untangle.parse('http://{}/library/sections/{}/all'.format(plex_server_address, section))
    movies = [{'id': movie['ratingKey'], 'title': movie['title'], 'art': movie['thumb']} for movie in movies.MediaContainer.Video]

    try:
        history = pickle.load(open(history_file_name, "rb"))
    except EOFError:
        history = []

    if request.method == 'POST':
        write_todays_movie(request.form['movie'])

        write_history(movies, todays_id, history)

        todays_id = request.form['movie']

    context = {
        'movies': movies,
        'todays_id': todays_id,
        'history': history,
        'plex_server_address': plex_server_address
    }

    return render_template('index.html', **context)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=http_port, debug=True, threaded=True)
