__author__ = 'djvol_000'

import json
from dajaxice.decorators import dajaxice_register
from media.plex_funcs import *
from media.aria import *
from media.forms import SearchForm, TorrentForm
from media.torrent_rss import parse_rss
import ast
import transmissionrpc
from time import sleep
import re
import operator
from collections import OrderedDict
from media_automater.config import *


@dajaxice_register(method='POST')
def purge_downloads(request):
    response = purge_finished().status_code
    if response == 200:
        return json.dumps({'status': 'success'})
    else:
        return json.dumps({'status': 'failure'})


@dajaxice_register(method='POST')
def load_downloads(request):
    downloads = downloads_information()
    return json.dumps(downloads)


@dajaxice_register(method='POST')
def load_media(request):
    # Load the media from Plex
    movies = list_movies()
    shows = list_shows()
    return json.dumps({'movies': movies, 'shows': shows})


@dajaxice_register(method='POST')
def transfer_file(request):
    posted_json = request.POST.getlist('argv')
    posted_data = ast.literal_eval(posted_json[0])
    download_url = posted_data['url']
    location = posted_data['location']
    download_request = add_download(download_url, ARIA_LOCATION + location)

    if download_request.text:
        return json.dumps({'status': 'success', 'data': download_request.text})
    else:
        return json.dumps({'status': 'failure', 'data': download_request.status_code})


@dajaxice_register(method='POST')
def search_media(request):
    posted_json = request.POST.getlist('argv')
    if not posted_json:
        return
    posted_data = ast.literal_eval(posted_json[0])
    search_form = SearchForm(posted_data)

    if search_form.is_valid():
        # Call plex search data based on form data
        # Is this a movie or a tv show search?
        search_type = search_form.cleaned_data['type']
        search_text = search_form.cleaned_data['search_text']
        if search_form.cleaned_data['optional_season']:
            search_season = search_form.cleaned_data['optional_season']
        else:
            search_season = ""
        if search_form.cleaned_data['optional_episode']:
            search_episode = search_form.cleaned_data['optional_episode']
        else:
            search_episode = ""
        search_results = search_plex(search_type=search_type, search=dict(search=search_text, season=search_season, episode=search_episode))

        return json.dumps({ 'status':'success', 'data': search_results })
    else:
        return json.dumps({ 'status': '%s' % search_form.errors })


@dajaxice_register(method='POST')
def search_torrent(request):
    posted_json = request.POST.getlist('argv')
    if not posted_json:
        return
    posted_data = ast.literal_eval(posted_json[0])
    torrent_form = TorrentForm(posted_data)

    if torrent_form.is_valid():
        # Parse the RSS feed based on this search text
        search_result = parse_rss( search_site=torrent_form.cleaned_data['torrent_search_site'], search_filter = torrent_form.cleaned_data['torrent_search_text'] )

        return json.dumps({ 'status': 'success', 'data': search_result })
    else:
        return json.dumps({ 'status': '%s FUCK' % torrent_form.errors })


@dajaxice_register(method='POST')
def transmission_torrent(request):
    posted_json = request.POST.getlist('argv')
    posted_data = ast.literal_eval(posted_json[0])
    posted_url = posted_data['url']
    element_id = posted_data['id']

    # Create a transmission rpc object and send the torrent off!
    try:
        transmission_client = transmissionrpc.Client(TRANSMISSION_HOST, port=TRANSMISSION_PORT, user=TRANSMISSION_USER, password=TRANSMISSION_PASS)
        torrent_return = transmission_client.add_torrent( posted_url )
    except (transmissionrpc.TransmissionError, KeyError) as error:
        return json.dumps({ 'status': 'failure', 'data': "There was an error getting the file to transmission, please try again.", 'id': element_id })

    # Check return data after a short sleep
    sleep(2)

    # Get the status of this torrent
    torrent_key = torrent_return.id
    torrent = transmission_client.get_torrent(torrent_key)
    torrent_status = torrent.status

    return json.dumps({ 'status': 'success', 'data': torrent_status, 'id': element_id })


@dajaxice_register(method='POST')
def refresh_files(request):
    try:
        transmission_client = transmissionrpc.Client(TRANSMISSION_HOST, port=TRANSMISSION_PORT, user=TRANSMISSION_USER, password=TRANSMISSION_PASS)
        torrents = transmission_client.get_torrents()
    except:
        return json.dumps({ 'status': 'failure' })

    current_torrents = dict(active=dict(), finished=dict())
    for torrent in torrents:
        torrent_id = torrent.id
        torrent_files = torrent.files()
        torrent_progress = torrent.progress
        torrent_speed = torrent.rateDownload
        if torrent_progress == 100.0:
            type_dict = 'finished'
        else:
            type_dict = 'active'
        current_torrents[type_dict][torrent_id] = dict(id=torrent_id, files=torrent_files, progress=torrent_progress, speed=torrent_speed)

    return json.dumps({ 'status': 'success', 'data': current_torrents })

    regex_match = r"\.(avi|mkv|mp4|wmv|iso)$"
    files = OrderedDict()
    for torrent in torrents:
        torrent_files = torrent.files()
        for torrent_key in torrent_files:
            if re.search(regex_match, torrent_files[torrent_key]['name']) and torrent_files[torrent_key]['completed'] >= torrent_files[torrent_key]['size']:
                if not files.get(torrent.id):
                    files[torrent.id] = [ torrent_files[torrent_key]['name'] ]
                else:
                    files[torrent.id].append(torrent_files[torrent_key]['name'])

    return json.dumps({ 'status': 'success', 'data': files })


@dajaxice_register(method='POST')
def delete_torrent(request):
    posted_json = request.POST.getlist('argv')
    posted_data = ast.literal_eval(posted_json[0])
    torrent_id = posted_data['id']
    try:
        transmission_client = transmissionrpc.Client(TRANSMISSION_HOST, port=TRANSMISSION_PORT, user=TRANSMISSION_USER, password=TRANSMISSION_PASS)
        torrent = transmission_client.remove_torrent(torrent_id, delete_data=True)

        return json.dumps({ 'status': 'success', 'data': '', 'id': torrent_id })
    except:
        return json.dumps({ 'status': 'failure' })