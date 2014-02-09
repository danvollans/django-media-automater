from __future__ import division
import requests
from media_automater.config import *
import json
from time import sleep

__all__ = ["addDownload", "getStatus"]


def addDownload(download_url, directory):
    request_json = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                               'method': 'aria2.addUri',
                               'params': [[download_url], {'dir': directory}]})

    request = requests.post(ARIA_HOST, request_json, auth=(ARIA_USER, ARIA_PASS))
    if request.text:
        return json.dumps({'status': 'success', 'data': request.text})
    else:
        return json.dumps({'status': 'failure', 'data': request.status_code})


def getStatus(download_id):
    request_json = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                               'method': 'aria2.tellStatus',
                               'params': [download_id]})

    return requests.post(ARIA_HOST, request_json, auth=(ARIA_USER, ARIA_PASS))


if __name__ == '__main__':
    new_request = addDownload('http://ipv4.download.thinkbroadband.com/512MB.zip', '/mnt/nas/downloads')
    response = json.loads(new_request.text)
    if response['result']:
        sleep(16)
        status = getStatus(response['result'])
        status_response = json.loads(status.text)
        if status_response['result']['completedLength'] != '0' and status_response['result']['totalLength'] != '0':
            print(status_response['result']['completedLength'] + ' / ' + status_response['result']['totalLength'])
            percent = format((int(status_response['result']['completedLength']) / int(status_response['result']['totalLength'])) * 100, '.2f')
            print(str(percent) + '%')



