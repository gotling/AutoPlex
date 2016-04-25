# AutoPlex
A small service for auto starting a movie every night. Very easy to use (after configured).

We have a cinema on playing movies every night at 19:00. A laptop with Windows is running Plex Media Server and hosting the movies. On that same machine AutoPlex is running on port 80. Every evening before it gets dark a projector with a Raspberry Pi attached to it is carried out and connected to power and speakers. At 18:30 a power socket timer is turned on giving power to projector, Raspberry and speakers. For half an hour the screen saver shows random pictures and then at 19:00 a scheduled task executes the batch script which requests a url in the Plex server API which starts the movie.

![Screenshot](/web/screenshot.png)

# Configuration
## play-movie.bat
Windows batch file starting playback. Can easely be converted to bash if needed.

**plex_server_ip:**
IP of the server hosting the media.

**plex_server_port:**
Default 32000

**plex_server_identifier**
Open ```http://<plex_server_ip>:<plex_server_port>``` in a web browser and find the value of *machineIdentifier*

**plex_client_ip:**
IP of the client playing the media.

**plex_client_port:**
Find it by opening ```http://<plex_server_ip>:<plex_server_port>/clients``` in a web browser and find the value of *?*

**plex_client_identifier:**
Same as above, find the value of *?*

## auto-plex.py
**plex_server_address:**
IP and port of the server in the format of ```<plex_server_ip>:<plex_server_port>```

**section:**
The id of the Library in Plex that the media is stored in. Find it by navigation to the Plex web interface at
```http://<plex_server_ip>:<plex_server_port>/web``` and clicking on the Library. The section number is in the end
of the URL field.

**http_port:**
Which port the web server where movies are configured from is reached. On windows it can easely be set to 80 if 
no other server is running on that port. In Linux that will required running the service as root.

# Installation
Create a scheduled task to run at the time you want the movie to start. Set it to execute **play-movie.bat**.

Start the web service with *auto-plex.bat* or put it in auto start.

# Usage
1. Open ```http://<server>:<port>``` in a web browser.
2. Select which movie should be played next.
3. Click *Save*.
