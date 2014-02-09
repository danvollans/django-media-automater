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
    request_json = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                               'method': 'aria2.tellStopped',
                               'params': [0, 2]})

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

    new_request = add_download('http://ipv4.download.thinkbroadband.com/512MB.zip', '/mnt/nas/downloads')
    response = json.loads(new_request.text)
    if response['result']:
        status = get_status(response['result'])
        status_response = json.loads(status.text)
        if status_response['result']['completedLength'] != '0' and status_response['result']['totalLength'] != '0':
            print(status_response['result']['completedLength'] + ' / ' + status_response['result']['totalLength'])
            percent = format((int(status_response['result']['completedLength']) / int(status_response['result']['totalLength'])) * 100, '.2f')
            print(str(percent) + '%')



