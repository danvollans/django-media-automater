from __future__ import division
import requests
import json
from media_automater.config import *

__all__ = ["add_download", "tell_active", "tell_stopped", "tell_waiting", "get_global_stat", "downloads_information", "purge_finished"]


def purge_finished():
    # First retrieve all finished downloads
    request_json = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                               'method': 'aria2.purgeDownloadResult' })

    return requests.post(ARIA_HOST, request_json, auth=(ARIA_USER, ARIA_PASS))


def add_download(download_url, directory):
    request_json = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                               'method': 'aria2.addUri',
                               'params': [[download_url], {'dir': directory, 'http-user': TRANSMISSION_USER, 'http-passwd': TRANSMISSION_PASS}]})

    request = requests.post(ARIA_HOST, request_json, auth=(ARIA_USER, ARIA_PASS))
    return request


def tell_waiting(waiting=None):
    if not waiting:
        waiting = 1
    request_json = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                               'method': 'aria2.tellWaiting',
                               'params': [0, waiting]})

    return requests.post(ARIA_HOST, request_json, auth=(ARIA_USER, ARIA_PASS))


def tell_active():
    request_json = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                               'method': 'aria2.tellActive'})

    return requests.post(ARIA_HOST, request_json, auth=(ARIA_USER, ARIA_PASS))


def tell_stopped(stopped=None):
    if not stopped:
        stopped = 1
    request_json = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                               'method': 'aria2.tellStopped',
                               'params': [0, stopped]})

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
            stopped_dict = json.loads(tell_stopped(stopped=int(global_dict['result']['numStopped'])).text)['result']
        else:
            stopped_dict = dict()
        if int(global_dict['result']['numWaiting']) > 0:
            waiting_dict = json.loads(tell_waiting(waiting=int(global_dict['result']['numWaiting'])).text)['result']
        else:
            waiting_dict = dict()
        status = 'success'
        error = ''
    else:
        active = dict()
        stopped = dict()
        waiting = dict()
        status = 'failure'
        error = global_query.status_code
    results = dict(active=active_dict, stopped=stopped_dict, waiting=waiting_dict, status=status, error=error)
    return results


if __name__ == '__main__':
    #print(purge_finished())
    #print(downloads_information())
    print(tell_waiting().text)