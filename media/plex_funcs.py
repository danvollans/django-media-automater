# -*- coding: utf-8 -*-
__author__ = 'djvol_000'

"""

This module allows parsing of all plex library sections into python data structures.

You can also search on that dat, and the usage is in the __main__ section

"""

from xml.dom import minidom
from urllib.request import urlopen
from urllib.parse import urlencode
from collections import OrderedDict
import sys
from media_automater.config import *
import re

__all__ = ["list_movies", "list_shows", "search_plex"]


def list_movies():
    source = 'movie'
    xml_sections = minidom.parse(urlopen(PLEX_URL + '/' + PLEX_SECTIONS))
    sections = xml_sections.getElementsByTagName('Directory')
    movie_list = list()

    try:
        for section in sections:
            if section.getAttribute('type') == source:
                key = section.getAttribute('key')
                xml_section = minidom.parse(urlopen('%s/%s/%s/all' % (PLEX_URL, PLEX_SECTIONS, key)))
                media = xml_section.getElementsByTagName('Video')
                for movie in media:
                    title = movie.getAttribute('title').lower()
                    year = movie.getAttribute('year')
                    summary = movie.getAttribute('summary')
                    media_id = movie.getAttribute('ratingKey')
                    movie_list.append( title + ' ' + year)

        return movie_list
    except:
        print(sys.exc_info())
        return list()


def list_shows():
    source = 'show'
    xml_sections = minidom.parse(urlopen(PLEX_URL + '/' + PLEX_SECTIONS))
    sections = xml_sections.getElementsByTagName('Directory')
    show_dict = OrderedDict()
    try:
        for section in sections:
            if section.getAttribute('type') == source:
                key = section.getAttribute('key')
                xml_section = minidom.parse(urlopen('%s/%s/%s/search?type=4' % (PLEX_URL, PLEX_SECTIONS, key)))
                videos = xml_section.getElementsByTagName('Video')

                for video in videos:
                    show_name = video.getAttribute('grandparentTitle')
                    show_season = "Season " + video.getAttribute('parentIndex')
                    show_episode_number = int(video.getAttribute('index'))
                    show_episode_title = video.getAttribute('title')
                    show_summary = video.getAttribute('summary')
                    media_id = video.getAttribute('ratingKey')
                    if show_name not in show_dict:
                        show_dict[show_name] = OrderedDict()
                    if show_season not in show_dict[show_name]:
                        show_dict[show_name][show_season] = OrderedDict()
                    show_dict[show_name][show_season][show_episode_number] = OrderedDict( title = show_episode_title, summary = show_summary, media_id = media_id )

        # Resort this dictionary
        show_dict = OrderedDict( sorted( show_dict.items() ) )
        for show in show_dict:
            show_dict[show] = OrderedDict( sorted( show_dict[show].items() ) )
            for season in show_dict[show]:
                show_dict[show][season] = OrderedDict( sorted( show_dict[show][season].items() ) )

        return show_dict
    except:
        print(sys.exc_info())
        return dict()


# New TV Show search using Plex HTTP API
def search_plex(search_type, search):
    # Get the key mapping for sections
    search_query = '/library/sections/'
    xml_sections = minidom.parse(urlopen(PLEX_URL + search_query))
    sections_results = xml_sections.getElementsByTagName('Directory')
    key_mapping = dict()

    for section in sections_results:
        key_mapping[section.getAttribute('type')] = section.getAttribute('key')
    if search_type == 'movie':
        search_query = '/library/sections/%s/search?' % key_mapping[search_type]
        get_data = urlencode({'type': '1', 'query': search['search']})
        xml_section = minidom.parse(urlopen(PLEX_URL + search_query + get_data))
        search_results = xml_section.getElementsByTagName('Video')
    elif search_type == 'show':
        search_query = '/library/sections/%s/search?' % key_mapping[search_type]
        get_data = urlencode({'type': '2', 'query': search['search']})
        xml_section = minidom.parse(urlopen(PLEX_URL + search_query + get_data))
        directories = xml_section.getElementsByTagName('Directory')
        search_results = []
        if directories:
            for directory in directories:
                search_key = directory.getAttribute('ratingKey')
                if not search.get('season', None) or search['season'] == '':
                    # Make new request to get all episodes
                    search_query = '/library/metadata/' + search_key + '/allLeaves'
                    xml_section = minidom.parse(urlopen(PLEX_URL + search_query))
                    for result in xml_section.getElementsByTagName('Video'):
                        search_results.append(result)
                elif search['season'] and search['season'] != '':
                    # Make new request to get all episodes
                    search_query = '/library/metadata/' + search_key + '/children'
                    xml_section = minidom.parse(urlopen(PLEX_URL + search_query))
                    # Now retrieve all children seasons
                    for result in xml_section.getElementsByTagName('Directory'):
                        if result.getAttribute('index') == search['season']:
                            episodes_by_season_query = result.getAttribute('key')
                            new_xml_section = minidom.parse(urlopen(PLEX_URL + episodes_by_season_query))
                            for new_result in new_xml_section.getElementsByTagName('Video'):
                                if search.get('episode', None) and search['episode'] != '':
                                    if search['episode'].isdigit() and search['episode'] == new_result.getAttribute('index'):
                                        search_results.append(new_result)
                                    elif re.match(search['episode'], new_result.getAttribute('title')):
                                        search_results.append(new_result)
                                else:
                                    search_results.append(new_result)
    # Parse through search_results
    # These should all be video elements at this point
    return_results = []
    for video in search_results:
        video_title = video.getAttribute('title')
        video_year = video.getAttribute('year')
        video_summary = video.getAttribute('summary')
        video_type = video.getAttribute('type')
        video_id = video.getAttribute('ratingKey')
        video_dict = dict( summary = video_summary, media_id = video_id, title = video_title + ' ' + video_year)
        return_results.append(video_dict)
    return return_results


if __name__ == '__main__':
    #movies = list_movies()
    #tv_shows = list_shows()

    #search_show = "Breaking Bad"
    #search_season = 1
    #search_episode = 2

    #print(search_exist(search_type = "show", structure = tv_shows, search_filters = dict( name = search_show, season = search_season, episode = search_episode)))
    #print(search_exist(search_type = "show", structure = tv_shows, search_filters = dict( name = search_show, season = search_season, episode = "")))

    #search_movie = "Aliens"
    #print(search_exist(search_type = "movie", structure = movies, search_filters = dict( name = search_movie)))

    #search_text = "star wars"
    #print(search_plex( search_filter = search_text ))

    # Try new plex search
    print(search_exist2(search_type='movie', search=dict(search='Indiana Jones',season='1', episode='1')))