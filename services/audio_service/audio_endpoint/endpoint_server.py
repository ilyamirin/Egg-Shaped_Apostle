import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

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
destination = 'localhost:5722'


def wrap_response(response):
    resp = jsonify(response)
    resp.headers.add('Access-Control-Allow-Origin', destination)
    return resp


#  card, mic, time, file
@app.route('/record', methods=['POST'])
def start_record():
    try:
        print(request.args)
        print(request.form)
        file = audio_service.record(request.form['card'],
                                    request.form['mic'],
                                    request.form['time'])
        resp = wrap_response({'response': f'{file}'})
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
        resp = wrap_response({'error': str(e)})
    return resp


@app.route('/send', methods=['POST'])
def send():
    try:
        print(request.form)
        resp = send_from_directory(config['ENV']['DATA_DIR'], request.form['filename'])
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
    return resp


@app.route('/devices', methods=['GET'])
def get_devices():
    try:
        resp = wrap_response(audio_service.get_devices())
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
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


@app.route('/parallel_rec/start', methods=['POST'])
def start_parallel_record():
    try:
        resp = wrap_response({'response': audio_service.start_standalone_recording(request.form['time'])})
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
    return resp


@app.route('/parallel_rec/stop', methods=['GET'])
def stop_parallel_record():
    try:
        resp = wrap_response({'response': audio_service.stop_standalone_recording()})
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
    return resp


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=config['FILE_SERVER']['WEB_API_PORT'])