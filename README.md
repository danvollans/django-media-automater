django-media-automater
======================

This project is a media automation tool using Django 1.5 and Python 3.3 It is intended for use with Plex for Media, and Transmission for torrent management.


Required Software:
------------------
* Plex Media Server for the media search functions
* Transmission as a torrent client running the RPC Server
* A server running aria2 for downloading files over HTTPS:
  * Command for running aria2 in daemon mode with RPC:
    * aria2c --daemon --enable-rpc --rpc-listen-all --rpc-user=user --rpc-passwd=pass --check-certificate=false --log-level=warn --log=/tmp/aria2.log

Required Python Software:
-------------------------
* python3.3
* django >= 1.5
* json
* django-dajax
* django-dajaxice
* ast
* transmissionrpc
* operator
* requests
* django-crispy-forms
* xml
* urllib
* bs4

General Requirements:
---------------------
The server that is running the aria2 daemon must at least have the storage that the Plex server uses mounted, or have it as local storage.


Installation Instructions:
--------------------------
### Preferred Setup ###
Plex:
  1.  Two sections, TV Shows and Movies.
  2.  TV Shows storage format:
    * TV Shows/\<Showname\>/Season \<#\>/\<Episode\>
  3.  Movies storage format:
    * Movies/\<Moviename\> (\<Year\>)/\<Movie\>


### Configuration ###
1.  Copy config-example.py to config.py
2.  Plex configurations

        PLEX_URL = "https://127.0.0.1:32400"
        PLEX_SECTIONS = "library/sections"

        TRANSMISSION_HOST = ''
        TRANSMISSION_PORT = ''
        TRANSMISSION_USER = ''
        TRANSMISSION_PASS = ''

        ARIA_HOST = ''
        ARIA_USER = ''
        ARIA_PASS = ''
        ARIA_LOCATION = ''