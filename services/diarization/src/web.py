import os
import requests
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from diarization import diarize

from logger import get_logger
from config_gen import get_config
from visualization import visualize

config = get_config()
logger = get_logger("diarization_service", config['SETTINGS']['DEBUG'])

audio_service_api = f'http://{config["NETWORK"]["AUDIO_SERVICE_IP"]}:{config["NETWORK"]["AUDIO_SERVICE_PORT"]}'

logger.info('starting web server...')

app = Flask(__name__)
CORS(app)


@app.route('/health', methods=['GET'])
def health():
    return {
        'service': 'diarization-service',
        'status': 'OK'
    }


@app.route('/annotation', methods=['GET'])
def annotation():
    print(request.headers)
    if 'Filename' not in request.headers:
        return {'type': 'BadRequestException', 'message': 'No filename provided'}, 400
    try:
        resp = requests.get(f'{audio_service_api}/record/{request.headers["Filename"]}')
        filename = os.path.join(config['ENV']['ROOT_ABS_PATH'], request.headers['Filename'])

        with open(filename, 'wb') as file:
            file.write(resp.content)
        result = diarize(filename)
        os.remove(filename)

    except Exception as e:
        logger.error(e)
        return {'type': str(type(e).__name__), 'message': str(e)}, 500

    return {'result': result}


@app.route('/svg', methods=['GET'])
def svg():
    try:
        return visualize(request.headers.get('filename'))
    except Exception as e:
        logger.error(e)
        return {'type': str(type(e).__name__), 'message': str(e)}, 500


app.run(host=config['NETWORK']['WEB_API_IP'], debug=False, port=config['NETWORK']['WEB_API_PORT'])
