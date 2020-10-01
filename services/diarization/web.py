import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from diarisation import diarize

from logger import get_logger
from config_gen import get_config
config = get_config()
logger = get_logger("diarization_service", config['SETTINGS']['DEBUG'])

logger.info('starting web server...')

app = Flask(__name__)
CORS(app)


@app.route('/health', methods=['GET'])
def health():
    return {
        'service': 'diarization-service',
        'status': 'OK'
    }


@app.route('/diarizate', methods=['POST'])
def transcript():
    if 'audio' not in request.files or request.files['audio'].filename == '':
        return { 'type': 'BadRequestException', 'message': 'No file provided' }, 400

    file_ = request.files['audio']

    try:
        with open('temp_file.wav', 'wb') as out_file:
            out_file.write(file_.read())
        result = diarize('temp_file.wav')

    except Exception as e:
        logger.error(e)
        return { 'type': str(type(e).__name__), 'message': str(e) }, 500

    return { 'result': result }


app.run(host=config['NETWORK']['WEB_API_IP'], debug=True, port=config['NETWORK']['WEB_API_PORT'])