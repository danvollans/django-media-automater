__author__ = 'djvol_000'

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from media.plex_funcs import *
from media.forms import SearchForm, TorrentForm
from media.torrent_rss import parse_rss
import ast
import transmissionrpc
from time import sleep
import re
import operator
from collections import OrderedDict
from media_automater.config import *
from media.plex_funcs import *


@dajaxice_register(method='POST')
def load_media(request):
    # Load the media from Plex
    movies = list_movies()
    shows = list_shows()
    return simplejson.dumps({'movies': movies, 'shows': shows})


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
        search_results = search_exist2(search_type=search_type, search=dict(search=search_text, season=search_season, episode=search_episode))

        return simplejson.dumps({ 'status':'success', 'data': search_results })
    else:
        return simplejson.dumps({ 'status': '%s' % search_form.errors })


@dajaxice_register(method='POST')
def search_torrent(request):
    posted_json = request.POST.getlist('argv')
    if not posted_json:
        return
    posted_data = ast.literal_eval(posted_json[0])
    torrent_form = TorrentForm(posted_data)

    if torrent_form.is_valid():
        # Parse the RSS feed based on this search text
        search_result = parse_rss( search_filter = torrent_form.cleaned_data['torrent_search_text'] )

        return simplejson.dumps({ 'status': 'success', 'data': search_result })
    else:
        return simplejson.dumps({ 'status': '%s FUCK' % torrent_form.errors })


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
    except transmissionrpc.TransmissionError:
        return simplejson.dumps({ 'status': 'failure', 'data': "There was an error getting the file to transmission, please try again.", 'id': element_id })

    # Check return data after a short sleep
    sleep(2)

    # Get the status of this torrent
    torrent_key = torrent_return.id
    torrent = transmission_client.get_torrent(torrent_key)
    torrent_status = torrent.status

    return simplejson.dumps({ 'status': 'success', 'data': torrent_status, 'id': element_id })


@dajaxice_register(method='POST')
def refresh_files(request):
    try:
        transmission_client = transmissionrpc.Client(TRANSMISSION_HOST, port=TRANSMISSION_PORT, user=TRANSMISSION_USER, password=TRANSMISSION_PASS)
        torrents = transmission_client.get_torrents()
    except:
        return simplejson.dumps({ 'status': 'failure' })

    regex_match = r"\.(avi|mkv|mp4|wmv)$"
    files = OrderedDict()
    for torrent in torrents:
        torrent_files = torrent.files()
        for torrent_key in torrent_files:
            if re.search(regex_match, torrent_files[torrent_key]['name']) and torrent_files[torrent_key]['completed'] >= torrent_files[torrent_key]['size']:
                if not files.get(torrent.id):
                    files[torrent.id] = [ torrent_files[torrent_key]['name'] ]
                else:
                    files[torrent.id].append(torrent_files[torrent_key]['name'])

    return simplejson.dumps({ 'status': 'success', 'data': files })


@dajaxice_register(method='POST')
def delete_torrent(request):
    posted_json = request.POST.getlist('argv')
    posted_data = ast.literal_eval(posted_json[0])
    torrent_id = posted_data['id']
    try:
        transmission_client = transmissionrpc.Client(TRANSMISSION_HOST, port=TRANSMISSION_PORT, user=TRANSMISSION_USER, password=TRANSMISSION_PASS)
        torrent = transmission_client.remove_torrent(torrent_id, delete_data=True)

        return simplejson.dumps({ 'status': 'success', 'data': '', 'id': torrent_id })
    except:
        return simplejson.dumps({ 'status': 'failure' })