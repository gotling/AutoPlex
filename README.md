# AutoPlex
A small service for auto starting a movie every night. Very easy to use (after configured).

We have a cinema on playing movies every night at 19:00. A laptop with Windows is running Plex Media Server and hosting the movies. On that same machine AutoPlex is running on port 80. Every evening before it gets dark a projector with a Raspberry Pi attached to it is carried out and connected to power and speakers. At 18:30 a power socket timer is turned on giving power to projector, Raspberry and speakers. For half an hour the screen saver shows random pictures and then at 19:00 a scheduled task executes the batch script which requests a url in the Plex server API which starts the movie. After the movie has started the movie for tomorrow is set in a web page.

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
Find it by opening ```http://<plex_server_ip>:<plex_server_port>/clients``` in a web browser and find the value of *host*

**plex_client_port:**
Same as above, find the value of *port*

**plex_client_identifier:**
Same as above, find the value of *machineIdentifier*

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

## RasPlex
We use [RasPlex](http://www.rasplex.com/) on the Raspberry Pi. Some adjustments is required for optimal function.

**Startup delay**

**Disable rainbox**

**Custom boot logo**
It is quite complicated to set you custom logo that shows during startup of RasPlex but is well worth the work. Follow [this guide](https://forums.plex.tv/discussion/163058/guide-use-custom-boot-screens) in the Plex forum for doing it.

# Installation
## Requirements
[Python](https://www.python.org/downloads/)
[curl](https://curl.haxx.se/download.html)

Install Python requirements:

```pip install -r requirements.txt```

Create a scheduled task to run at the time you want the movie to start. Set it to execute **play-movie.bat**.

Start the web service with *auto-plex.bat* or put it in auto start.

# Usage
1. Open ```http://<server>:<port>``` in a web browser.
2. Select which movie should be played next.
3. Click *Save*.
