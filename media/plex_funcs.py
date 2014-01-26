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

__all__ = ["list_movies", "list_shows", "search_exist", "search_plex"]


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
                    show_name = video.getAttribute('grandparentTitle').lower()
                    show_season = int(video.getAttribute('parentIndex'))
                    show_episode_number = int(video.getAttribute('index'))
                    show_episode_title = video.getAttribute('title').lower()
                    show_summary = video.getAttribute('summary')
                    media_id = video.getAttribute('ratingKey')
                    if show_name not in show_dict:
                        show_dict[show_name] = OrderedDict( seasons = OrderedDict() )
                    if show_season not in show_dict[show_name]["seasons"]:
                        show_dict[show_name]["seasons"][show_season] = OrderedDict()
                    show_dict[show_name]["seasons"][show_season][show_episode_number] = OrderedDict( title = show_episode_title, summary = show_summary, media_id = media_id )

        # Resort this dictionary
        show_dict = OrderedDict( sorted( show_dict.items() ) )
        for show in show_dict:
            show_dict[show]["seasons"] = OrderedDict( sorted( show_dict[show]["seasons"].items() ) )
            for season in show_dict[show]["seasons"]:
                show_dict[show]["seasons"][season] = OrderedDict( sorted( show_dict[show]["seasons"][season].items() ) )

        return show_dict
    except:
        print(sys.exc_info())
        return dict()

# Use this for searching TV Shows
def search_exist(search_type, structure, search_filters):
    search_name = search_filters["name"].lower()
    results = OrderedDict()
    if search_type == "movie":
        list_match = [movie for movie in structure if search_name in movie]
        return list_match
    elif search_type == "show":
        result_set = structure.get(search_name, {}).get('seasons', {}).get(search_filters["season"], {}).get(search_filters["episode"], {})
        if result_set:
            title = structure[search_name]["seasons"][search_filters["season"]][search_filters["episode"]]["title"]
            media_id = structure[search_name]["seasons"][search_filters["season"]][search_filters["episode"]]["media_id"]
            results[title] = dict( title = title, summary = structure[search_name]["seasons"][search_filters["season"]][search_filters["episode"]]["summary"], media_id = media_id )
            return results
        result_set = structure.get(search_name, {}).get('seasons', {}).get(search_filters["season"], {})
        if result_set:
            return result_set



# Use this for searching Movies
def search_plex(search_filter):
    get_data = urlencode({ 'query' : search_filter })
    xml_section = minidom.parse(urlopen(PLEX_URL + '/search?%s' % get_data))
    videos = xml_section.getElementsByTagName('Video')

    results = OrderedDict()
    for video in videos:
        video_title = video.getAttribute('title')
        video_year = video.getAttribute('year')
        video_summary = video.getAttribute('summary')
        video_type = video.getAttribute('type')
        video_id = video.getAttribute('ratingKey')

        # Ignore tv show results for now, another searching mechanism
        if video_type == "movie":
            results[video_title + ' ' + video_year] = dict( summary = video_summary, media_id = video_id, title = video_title + ' ' + video_year)

    return results

if __name__ == '__main__':
    movies = list_movies()
    tv_shows = list_shows()

    search_show = "Breaking Bad"
    search_season = 1
    search_episode = 2

    print(search_exist(search_type = "show", structure = tv_shows, search_filters = dict( name = search_show, season = search_season, episode = search_episode)))
    print(search_exist(search_type = "show", structure = tv_shows, search_filters = dict( name = search_show, season = search_season, episode = "")))

    search_movie = "Aliens"
    print(search_exist(search_type = "movie", structure = movies, search_filters = dict( name = search_movie)))

    search_text = "star wars"
    print(search_plex( search_filter = search_text ))