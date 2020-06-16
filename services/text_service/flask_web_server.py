#!/usr/bin/env python
# -*- coding: utf-8 -*-
# creates config.ini and sets default settings if not exists
__author__ = "Paul Maksimov"
__copyright__ = "Copyright 2020, The Egg-Shaped Apostle Project"
__version__ = "1.0.0"
__maintainer__ = "Paul Maksimov"
__email__ = "work.xenus@gmail.com"
__status__ = "Production"
from flask import Flask, jsonify, request, abort, send_from_directory
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
destination = 'localhost:4200'


def wrap_response(response):
    resp = jsonify(response)
    resp.headers.add('Access-Control-Allow-Origin', destination)
    return resp
