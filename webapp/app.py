#!/usr/bin/env python3
import os
import json
import re
from flask import Flask, request, abort, render_template, redirect, url_for, session, flash
import pprint
import logging
import subprocess
import glob
import time

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
def start():
    image_path = '/app/static/sd_cam'
    images = os.listdir(image_path)
    logger.debug(images)
    return render_template('all_cams.html', images=images, image_path=image_path) 

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=int(80), debug=True, threaded=True)
