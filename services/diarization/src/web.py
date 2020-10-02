import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from diarization import diarize

from logger import get_logger
from config_gen import get_config
from visualization import visualize

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


@app.route('/annotation', methods=['POST'])
def annotation():
    if 'audio' not in request.files or request.files['audio'].filename == '':
        return { 'type': 'BadRequestException', 'message': 'No file provided' }, 400

    file_ = request.files['audio']

    try:
        filename = os.path.join(config['ENV']['ROOT_ABS_PATH'], file_.filename)
        with open(filename, 'wb') as out_file:
            out_file.write(file_.read())
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


app.run(host=config['NETWORK']['WEB_API_IP'], debug=True, port=config['NETWORK']['WEB_API_PORT'])