__author__ = 'djvol_000'

"""

Parse RSS feed from Kat.ph and return dataset

"""

from xml.etree import ElementTree as etree
from urllib.request import urlopen
from urllib.parse import urlencode
from collections import OrderedDict
import sys

__all__ = ["parse_rss"]

rss_url = "http://kickass.to"

def parse_rss(search_filter):
    if search_filter == "":
        return dict()
    get_data = search_filter.lower()
    rss_tag = urlencode( {'rss': '1', 'field': 'seeders', 'sorder': 'desc'} )
    xml_section = etree.parse(urlopen(rss_url + '/usearch/%s/?%s' % (get_data, rss_tag)))
    torrents = list(xml_section.iter('item'))

    search_results = OrderedDict()
    counter = 0
    for torrent in torrents:
        title = torrent.find('title').text
        torrent_url = torrent.find('{http://xmlns.ezrss.it/0.1/}magnetURI').text
        #torrent_url = torrent.find('enclosure').get('url')
        search_results[counter] = OrderedDict( title = title, url = torrent_url )
        counter += 1

    return search_results

if __name__ == '__main__':
    results = parse_rss(search_filter = "melissa and joey s03e01 720p")

    print(results)