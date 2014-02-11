__author__ = 'djvol_000'

"""

Parse RSS feed from Kat.ph and return dataset

"""

from xml.etree import ElementTree as etree
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen, URLError
from urllib.parse import urlencode
from collections import OrderedDict
import sys

__all__ = ["parse_rss", 'parse_kickass', 'parse_torrenthound']


site_choices = ['Kickass', 'TorrentHound']


def parse_torrenthound(search_filter):
    rss_url = 'http://www.torrenthound.com'

    try:
        search_page = requests.post(rss_url + '/search/1/' + search_filter.replace(' ', '+') + '/seeds:desc')
    except URLError:
        return dict()

    search_soup = BeautifulSoup(search_page.text)

    links = search_soup.select('div[class="sfloat"]')

    search_results = list()
    for torrent in links:
        item = torrent.parent
        torrent_link = item.find('a', title="Magnet download")
        torrent_text = torrent.findNextSibling('a')
        if torrent_link and torrent_text:
            search_results.append(dict(url=torrent_link['href'], title=torrent_text.text))

    return search_results


def parse_kickass(search_filter):
    rss_url = 'http://kickass.to'
    rss_tag = urlencode({'rss': '1', 'field': 'seeders', 'sorder': 'desc'})
    get_data = search_filter.lower()

    try:
        search_page = urlopen(rss_url + '/usearch/%s/?%s' % (get_data, rss_tag))
    except URLError:
        return dict()

    xml_section = etree.parse(search_page)
    torrents = list(xml_section.iter('item'))

    search_results = list()
    for torrent in torrents:
        title = torrent.find('title').text
        torrent_url = torrent.find('{http://xmlns.ezrss.it/0.1/}magnetURI').text
        #torrent_url = torrent.find('enclosure').get('url')
        search_results.append(dict( title = title, url = torrent_url ))

    return search_results


def parse_rss(search_site, search_filter):
    if search_site not in site_choices:
        return 'Not a valid search site'
    if search_filter == "":
        return dict()

    # Determine the proper parsing function to use
    if search_site == 'Kickass':
        return parse_kickass(search_filter)
    elif search_site == 'TorrentHound':
        return parse_torrenthound(search_filter)


if __name__ == '__main__':
    #results = parse_rss(search_filter = "melissa and joey s03e01 720p")
    results = parse_torrenthound(search_filter='Psych S08E02 720p')

    print(results)