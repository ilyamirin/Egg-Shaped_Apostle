import os
import subprocess
import configparser
from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin

from config_gen import get_config
from audio_logger import get_logger
import audio_service

config = get_config()
if config.has_section('SETTINGS'):
    if 'DEBUG' in config['SETTINGS'].keys():
        logger = get_logger("audio_service", config['SETTINGS']['DEBUG'])
else:
    logger = get_logger("audio_service", '1')

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
destination = 'localhost:4200'


def wrap_response(response):
    resp = jsonify(response)
    resp.headers.add('Access-Control-Allow-Origin', destination)
    return resp


#  card, mic, time, file
@app.route('/record', methods=['POST'])
def start_record():
    try:
        print(request)
        file = audio_service.record(**request.json)
        resp = wrap_response({'response': f'file {file} was recorded'})
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
    return resp


@app.route('/records', methods=['GET'])
def get_records():
    try:
        resp = wrap_response(audio_service.get_files_list())
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': e})
    return resp


#  filename
@app.route('/send', methods=['POST'])
def record():
    try:
        file, output_file = audio_service.send(request.json['filename'])
        resp = wrap_response({'response': f'file {file} was sended to {output_file} in main storage server'})
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': e})
    return resp


@app.route('/devices', methods=['GET'])
def get_devices():
    try:
        resp = wrap_response(audio_service.get_devices())
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': e})
    return resp


@app.route('/config', methods=['GET'])
def get_config():
    if 'config.ini' in os.listdir('.'):
        with open('config.ini', 'r') as config:
            resp = wrap_response(config.read())
    else:
        resp = wrap_response({'error': 'there is no config'})
    return resp


@app.route('/config', methods=['POST'])
def set_config():
    with open('config.ini', 'w') as config:
        config.write(request.json['config'])
    resp = jsonify({'response': 'successful overwriting of config.ini'})
    return resp


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5721')