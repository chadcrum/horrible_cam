#!/usr/bin/env python3
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
    bla = 'test'
    file_dir = '/recordings/driveway'
    files = os.listdir(file_dir)
    files = glob.glob(file_dir + "/*.mp4")
    files.sort(key=os.path.getmtime, reverse=True)
    logger.debug(files)
    return bla

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
