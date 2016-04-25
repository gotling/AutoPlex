@echo off
SET plex_server_ip=10.0.0.14
SET plex_server_port=32400
SET plex_server_identifier=28cff6063535af7fd68b313ed816c6bde08d7e8d

SET plex_client_ip=10.0.0.27
SET plex_client_port=3005
SET plex_client_identifier=c3cf6e7d-46e2-4bf0-bf47-931b80d17a91

cd %~dp0
curl -s "http://%plex_client_ip%:%plex_client_port%/player/playback/stop"
set /p movie-id=<todays-movie-id.txt
curl "http://%plex_client_ip%:%plex_client_port%/player/playback/playMedia?key=/library/metadata/%movie-id%&address=%plex_server_ip%&port=%plex_server_port%&X-Plex-Client-Identifier=%plex_client_identifier%&machineIdentifier=%plex_server_identifier%&protocol=http&path=http://%plex_server_ip%:%plex_server_port%/library/metadata/%movie-id%"
exit 0