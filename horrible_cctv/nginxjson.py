import sys
import json
import pprint
import time
import logging
import glob
import os
import traceback
import socket
import random
import requests
import re
from datetime import datetime

"""Retrieves json file list from json auto index enabled NGINX server.

Performs various sorting / filtering actions on the json file list prior
to returning to the calling application.
"""

logger = logging.getLogger(__name__)

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

def sort_json_files(url, max_age_days, file_regex, max_size):
    """Filters/sorts json list retrieved from get_file_list in various ways.

    max_age_days : int - Number of days from now() that mtime ("mtime":"Tue, 31 Oct 2017 09:16:03 GMT") must be within
    file_regex   : regular expression of files to match
    size         : int - size in bytes that size ("size":11441932) must be within
    - "type" is always filtered for file and files are sorted in mtime descending order
    - mtime_dt field is added to each entry, it is the datetime object version of the mtime date string
    Filtered/sorted list of dicts is returned
    """
    file_list = []
    # Get raw file list
    raw_file_list = get_file_list(url)
    logger.debug('Found %s total files from nginx json url %s', len(raw_file_list), url)
    for i in raw_file_list:
        if i['type'] == 'file':
            if i['size'] < max_size:
                if re.search(file_regex, i['name']):
                    # Adds mtime_dt datetime field - "mtime":"Sun, 29 Oct 2017 15:10:00 GMT"
                    i['mtime_dt'] = datetime.strptime(i['mtime'].replace(' GMT', ''), '%a, %d %b %Y %H:%M:%S')
                    file_list.append(i)
                else:
                    logger.info('%s file does not match file regex %s - Will not process file', i['name'], file_regex)
            else:
                logger.info('%s file size %s is greater than max size %s - Will not process file', i['name'], ['size'], max_size)
    logger.debug('Filtered nginx file list to %s files', len(file_list))
    # Sort list of dict by [{'mtime_dt':] desc
    file_list = sorted(file_list, key = lambda k: k["mtime_dt"], reverse=True)
    return file_list

def download_file(url, filepath):
    """Download http path (url) to local file (filepath)"""
    logger.debug('Attempting to download file %s', url)
    try:
        session = requests.Session()
        session.trust_env = False
        r = session.get(url, stream=True, timeout=30)
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
        r.close()
    except Exception:
        logger.exception('Problem downloading remote file %s', url)
        raise

def get_trend_health_report_dict(url):
    """Returns dict of trend health report data for devices from NGINX json autoindex.

    Iterates through list of directories with device_id names, then iterates through sub-directories and retrieves
    both health report txt and html files, which are associated with the device within a dict as strings.
    Associated dict is returned.
    """
    data = []
    # Get list of directories which are named after the devices
    raw_file_list = get_file_list(url)
    logger.debug('Found %s possible files for trend health report', len(raw_file_list))
    for i in raw_file_list:
        if i['type'] == 'directory':
            entry = {
                'device_id': i['name'],
                'latest_trending_report_txt_url': url + i['name'] + '/',
                'latest_trending_report_html_url': url + i['name'] + '/html/',
            }
            entry['latest_trending_report_txt'] = get_latest_trend_health(entry['latest_trending_report_txt_url'], entry['device_id'])
            entry['latest_trending_report_html'] = get_latest_trend_health(entry['latest_trending_report_html_url'], entry['device_id'])
            data.append(entry)
    return data

def get_latest_trend_health(url, device):
    """Identifies and returns the latest .tar.txt or .tar.html health check file content.

    Example results:
    { "name":"log_ATPCF001_ssd_20171010_0700.tar.txt", "type":"file", "mtime":"Sat, 28 Oct 2017 17:32:06 GMT", "size":2961 },
    { "name":"log_ATPCF001_ssd_20171011_0700.tar.txt", "type":"file", "mtime":"Sat, 28 Oct 2017 15:26:20 GMT", "size":3687 },
    { "name":"log_ATPCF001_ssd_20171012_0700.tar.txt", "type":"file", "mtime":"Sat, 28 Oct 2017 13:17:41 GMT", "size":3487 },

    Identifies the latest based on "mtime", captures the txt file content to a string and returns the string.
    """
    raw_file_list = get_file_list(url)
    health_file = None
    logger.debug('Found %s health report text files', len(raw_file_list))
    # Add mtime_dt field to all entries in dict and sort by mtime_dt desc
    sorted_file_list = sort_by_mtime_dt_desc(add_mtime_dt_to_file_list(raw_file_list))
    # health_file = the most recent file that matches device name
    for i in sorted_file_list:
        if re.search(device, i['name']):
            health_file = i['name']
            break
    # Retrieve remote http file content
    if not health_file:
        raise Exception
    content = get_http_file_content(url + health_file)
    return content

def sort_by_mtime_dt_desc(file_list):
    """Sorts an nginx json autoindex file list by mtime_dt field descending (mtime_dt field is not default and must be added).

    mtime_dt field is added with function add_mtime_dt_to_file_list() function
    """
    sorted_file_list = sorted(file_list, key = lambda k: k["mtime_dt"], reverse=True)
    return sorted_file_list


def convert_mtime_to_datetime(mtime):
    """Converts an nginx json autoindex mtime to datetime.

    Example: "mtime":"Sat, 28 Oct 2017 17:32:06 GMT"
    returns : datetime object
    """
    dt = datetime.strptime(mtime.replace(' GMT', ''), '%a, %d %b %Y %H:%M:%S')
    return dt

def add_mtime_dt_to_file_list(files):
    """Adds "mtime_dt" (datetime from mtime) field to an NGINX json retrieved file list for each entry

    String "mtime":"Sat, 28 Oct 2017 17:32:06 GMT" is converted to a datetime object and set as mtime_dt
    returns : Updated file list dict
    """
    new_files = []
    for i in files:
        i['mtime_dt'] = convert_mtime_to_datetime(i['mtime'])
        new_files.append(i)
    return new_files

def get_http_file_content(url):
    """Returns the content of a file via http."""
    session = requests.Session()
    session.trust_env = False
    try:
        r = session.get(url, timeout=30)
        if r.status_code == 200:
            logger.debug('Retrieved remote file content with return state code %s', r.status_code)
            return r.text
        else:
            connection_error = "Error retrieving remote file content with status code %s and message %s and url %s" % (r.status_code, r.text, url)
            raise ConnectionError(connection_error)
    except ConnectionError:
        logger.exception('Problem retrieving content from url  %s', url)
        raise

