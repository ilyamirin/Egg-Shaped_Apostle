# берет все устройства из локальной сети
import os
import json
import pyaudio

from flask import Flask, jsonify, request, abort, send_from_directory, redirect, url_for, Response
from flask_cors import CORS, cross_origin

from logger import get_logger
from config_gen import get_config


config = get_config()
if config.has_section('SETTINGS') and 'DEBUG' in config['SETTINGS'].keys():
    logger = get_logger("audio_service", config['SETTINGS']['DEBUG'])
else: logger = get_logger("audio_service", '1')

if not os.path.exists(config['ENV']['EXT_DATA_DIR']):
    logger.debug('can\'t find data dir, trying to create...')
    try:
        os.makedirs(config['ENV']['DATA_DIR'])
    except Exception as e:
        logger.error(e)

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
destination = 'http://localhost:4200'


def wrap_response(response):
    resp = jsonify(response)
    resp.headers.add('Access-Control-Allow-Origin', destination)
    return resp


@app.route('/substract', methods=['GET'])
def substract(filename):
    try:
        return send_from_directory(config['ENV']['EXT_DATA_DIR'], filename)
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
        return resp


if __name__ == '__main__':
    app.run(host=config['NETWORK']['WEB_API_IP'], debug=True, port=config['NETWORK']['WEB_API_PORT'])