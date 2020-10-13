import requests
import json
import os
from flask import Flask, jsonify, request, abort, send_from_directory
from flask_cors import CORS, cross_origin

from config_gen import get_config
from logger import get_logger

config = get_config()
if config.has_section('SETTINGS'):
    if 'DEBUG' in config['SETTINGS'].keys():
        logger = get_logger("text_service", config['SETTINGS']['DEBUG'])
else:
    logger = get_logger("audio_service", '1')

storage_service_api = f'http://{config["NETWORK"]["STORAGE_SERVICE_IP"]}:{config["NETWORK"]["STORAGE_SERVICE_PORT"]}'

config = get_config()
if config.has_section('SETTINGS') and 'DEBUG' in config['SETTINGS'].keys():
    logger = get_logger("audio_service", config['SETTINGS']['DEBUG'])
else: logger = get_logger("analytics_service", '1')


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
destination = 'localhost:4200'


def wrap_response(response):
    resp = jsonify(response)
    resp.headers.add('Access-Control-Allow-Origin', destination)
    return resp


@app.route('/analyse/', methods=['GET'])
def analyse():
    work_place = request.args.get('work_place', '')
    role = request.args.get('role', '')
    date_time_start = request.args.get('date_time_start', '')
    date_time_end = request.args.get('date_time_end', '')
    headers = {
        'Content-Type': 'application/json'
    }
    data = json.dumps({
        'work_place': work_place,
        'role': role,
        'date_time_start': date_time_start,
        'date_time_end': date_time_end,
        })
    r = requests.get(storage_service_api + '/filter',
                     data=data,
                     headers=headers)
    resp = r.json()
    # resp = draw_imgs(r.json()['response'][0])
    return jsonify(resp)


def draw_imgs(text_list):
    print(text_list)
    texts = [i[5] for i in text_list]
    texts = text_list
    # print(texts)
    return texts


if __name__ == '__main__':
    app.run(host=config['NETWORK']['WEB_API_IP'], debug=True, port=config['NETWORK']['WEB_API_PORT'])