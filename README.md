# AutoPlex
A small service for auto starting a movie every night in our beach cinema.

# Configuration
## play-movie.bat
Windows batch file starting playback. Can easely be converted to bash if needed.

**plex_server_ip**
IP of the server hosting the media.

**plex_server_port**
Default 32000

**plex_server_identifier**
Open http://<plex_server_ip>:<plex_server_port> in a web browser and find the value of *machineIdentifier*

**plex_client_ip**
IP of the client playing the media.

**plex_client_port**
Find it by opening http://<plex_server_ip>:<plex_server_port>/clients in a web browser and find the value of *?*

**plex_client_identifier**
Same as above, find the value of *?*

## auto-plex.py
**plex_server_address**
IP and port of the server in the format of <plex_server_ip>:<plex_server_port>

**section**
The id of the Library in Plex that the media is stored in. Find it by navigation to the Plex web interface at
http://<plex_server_ip>:<plex_server_port>/web and clicking on the Library. The section number is in the end
of the URL field.

**http_port**
Which port the web server where movies are configured from is reached. On windows it can easely be set to 80 if 
no other server is running on that port. In Linux that will required running the service as root.
