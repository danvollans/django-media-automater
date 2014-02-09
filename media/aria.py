from __future__ import division
import requests
import json
from media_automater.config import *

__all__ = ["add_download", "tell_active", "tell_stopped", "tell_waiting", "get_global_stat", "downloads_information"]


def add_download(download_url, directory):
    request_json = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                               'method': 'aria2.addUri',
                               'params': [[download_url], {'dir': directory, 'http-user': TRANSMISSION_USER, 'http-passwd': TRANSMISSION_PASS}]})

    request = requests.post(ARIA_HOST, request_json, auth=(ARIA_USER, ARIA_PASS))
    return request


def tell_waiting():
    request_json = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                               'method': 'aria2.tellWaiting'})

    return requests.post(ARIA_HOST, request_json, auth=(ARIA_USER, ARIA_PASS))


def tell_active():
    request_json = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                               'method': 'aria2.tellActive'})

    return requests.post(ARIA_HOST, request_json, auth=(ARIA_USER, ARIA_PASS))


def tell_stopped():
    global_query = get_global_stat()
    if global_query.text:
        global_dict = json.loads(global_query.text)
        max_stopped = int(global_dict['result']['numStopped'])
    else:
        max_stopped = 1
    request_json = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                               'method': 'aria2.tellStopped',
                               'params': [0, max_stopped]})

    return requests.post(ARIA_HOST, request_json, auth=(ARIA_USER, ARIA_PASS))


def get_global_stat():
    request_json = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                               'method': 'aria2.getGlobalStat'})
    request = requests.post(ARIA_HOST, request_json, auth=(ARIA_USER, ARIA_PASS))
    return request


def downloads_information():
    global_query = get_global_stat()
    if global_query.text:
        global_dict = json.loads(global_query.text)
        if int(global_dict['result']['numActive']) > 0:
            active_dict = json.loads(tell_active().text)['result']
        else:
            active_dict = dict()
        if int(global_dict['result']['numStopped']) > 0:
            stopped_dict = json.loads(tell_stopped().text)['result']
        else:
            stopped_dict = dict()
        if int(global_dict['result']['numWaiting']) > 0:
            waiting_dict = json.loads(tell_waiting().text)['result']
        else:
            waiting_dict = dict()
    results = dict(active=active_dict, stopped=stopped_dict, waiting=waiting_dict)
    return results


if __name__ == '__main__':
    print('Loaded')