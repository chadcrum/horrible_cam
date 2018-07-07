#!/usr/bin/env python3
from datetime import datetime, timedelta
import humanfriendly
import requests
import glob
import json
import re
from flask import Flask, request, abort, render_template, redirect, url_for, session, flash
import pprint
import logging
import subprocess
import os

pp = pprint.PrettyPrinter(indent=4)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s [ %(module)s:%(funcName)s:%(lineno)d ] - %(message)s','%b %d %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    base_url = os.environ['BASE_URL']
    crap = '<html><head></head><body><h2>Recordings</h2>' 
    for i in get_file_list(base_url):
        crap += '<a href="/videos/' + i["name"] + '">' + i["name"] + '</a></br>'
    return crap

@app.route("/videos/<video_dir>", methods=['GET'])
@app.route("/videos/<video_dir>/<page>", methods=['GET'])
def list_videos(video_dir, page=0):
    page_offset = 10
    time_offset = os.environ['TIME_OFFSET']
    video_url = os.environ['BASE_URL'] + video_dir + '/'
    bla = sort_json_files(video_url)
    logger.debug(bla)
    crap = '<html><head></head><body><h3>' + video_dir + '</h3>'
    for i in bla[int(page):int(page) + page_offset]:   
        tmp_date = i['mtime_dt'] - timedelta(hours=int(os.environ['TIME_OFFSET']))
        crap += '<h3>' + tmp_date.strftime('%b %d, %Y - %H:%M:%S') + ' - ' + str(humanfriendly.format_size(i['size'])) + '</h3>'
        crap += '<video width="320" height="240" controls > <source src="' + video_url + i['name'] + '" type="video/mp4"></video><br>'
        #crap += '<video width="320" height="240" controls preload="none"> <source src="' + video_url + i['name'] + '" type="video/mp4"></video><br>'
        crap += "<hr>"
    return crap
    

def get_file_list(url):
    """Retrieves a json file list from a url"""
    session = requests.Session()
    session.trust_env = False
    try:
        r = session.get(url, timeout=30, headers={'Content-type': 'application/json', 'Accept': 'application/json'})
        if r.status_code == 200:
            logger.debug('Retrieved remote file list return state code %s', r.status_code)
            file_list = json.loads(r.text)
            return file_list
        else:
            connection_error = "Error retrieving remote file list with status code %s and message %s and url %s" % (r.status_code, r.text, url)
            raise ConnectionError(connection_error)
    except ConnectionError:
        logger.exception('Problem connecting to remote server %s to retrieve file list', url)
        raise
    return file_list

def sort_json_files(url):
    file_list = []
    # Get raw file list
    raw_file_list = get_file_list(url)
    for i in raw_file_list:
        if i['type'] == 'file':
            # Adds mtime_dt datetime field - "mtime":"Sun, 29 Oct 2017 15:10:00 GMT"
            i['mtime_dt'] = datetime.strptime(i['mtime'].replace(' GMT', ''), '%a, %d %b %Y %H:%M:%S')
            file_list.append(i)
    # Sort list of dict by [{'mtime_dt':] desc
    file_list = sorted(file_list, key = lambda k: k["mtime_dt"], reverse=True)
    return file_list

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
