import requests
import json
import os
from flask import Flask, jsonify, request, abort, send_from_directory
from flask_cors import CORS, cross_origin

from config_gen import get_config
from logger import get_logger

config = get_config()
logger = get_logger("analytics_service", config['SETTINGS']['DEBUG'])

storage_service_api = f'http://{config["NETWORK"]["STORAGE_SERVICE_IP"]}:{config["NETWORK"]["STORAGE_SERVICE_PORT"]}'
audio_service_api = f'http://{config["NETWORK"]["AUDIO_SERVICE_IP"]}:{config["NETWORK"]["AUDIO_SERVICE_PORT"]}'
diarization_service_api = f'http://{config["NETWORK"]["DIARIZATION_SERVICE_IP"]}:' \
                          f'{config["NETWORK"]["DIARIZATION_SERVICE_PORT"]}'

config = get_config()


logger.info('starting web server...')

app = Flask(__name__)
CORS(app)


@app.route('/health', methods=['GET'])
def health():
    return {
        'service': 'analytics-service',
        'status': 'OK'
    }


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
destination = 'localhost:4200'


@app.route('/analyse/', methods=['POST'])
def analyse():
    try:
        result = None
    except Exception as e:
        logger.error(e)
        return {'type': str(type(e).__name__), 'message': str(e)}, 500

    return {'result': result}, 200


@app.route('/diarize/', methods=['POST'])
def diarize():
    try:
        headers = {"Content-Type": "application/json"}
        print(request.json)
        files_list = requests.post(audio_service_api+'/records/filter', headers=headers, data=json.dumps(request.json)).json()['response']
        result = []
        for file in files_list:
            headers = {"Filename": file}
            annotation = requests.get(diarization_service_api + '/annotation', headers=headers).json()['result']
            annotation['filename'] = file
            result.append(annotation)
        return {'result': result}, 200
    except Exception as e:
        logger.error(e)
        return {'type': str(type(e).__name__), 'message': str(e)}, 500


def draw_imgs(text_list):
    print(text_list)
    texts = [i[5] for i in text_list]
    texts = text_list
    # print(texts)
    return texts


if __name__ == '__main__':
    app.run(host=config['NETWORK']['WEB_API_IP'], debug=True, port=config['NETWORK']['WEB_API_PORT'])