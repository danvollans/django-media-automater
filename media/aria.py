from __future__ import division
import requests
from media_automater.config import *
import json

__all__ = ["add_download", "get_status"]


def add_download(download_url, directory):
    request_json = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                               'method': 'aria2.addUri',
                               'params': [[download_url], {'dir': directory}]})

    request = requests.post(ARIA_HOST, request_json, auth=(ARIA_USER, ARIA_PASS))
    return request


def get_status(download_id):
    request_json = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                               'method': 'aria2.tellStatus',
                               'params': [download_id]})

    return requests.post(ARIA_HOST, request_json, auth=(ARIA_USER, ARIA_PASS))


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



