import os
import requests
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask import send_file
from io import BytesIO
import threading
from datetime import datetime
from time import sleep
import db

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

auto_diarize_flag = False


def start_auto_diarization():
    global diarize_flag
    start_hour = datetime.time(datetime.strptime(config["SETTINGS"]["DIAR_START_HOUR"], '%H:%M'))
    end_hour = datetime.time(datetime.strptime(config["SETTINGS"]["DIAR_END_HOUR"], '%H:%M'))
    logger.info(f'start diarization by time between {config["SETTINGS"]["DIAR_START_HOUR"]}\
    and {config["SETTINGS"]["DIAR_END_HOUR"]}...')
    while auto_diarize_flag:
        date_now = datetime.date(datetime.now())
        start_datetime = datetime.combine(date_now, start_hour)
        end_datetime = datetime.combine(date_now, end_hour)
        start_delta = datetime.now().timestamp() - start_datetime.timestamp()
        end_delta = datetime.now().timestamp() - end_datetime.timestamp()
        if start_delta > 0 > end_delta or date_now.weekday() in [5, 6] or True:
            logger.debug(f'Non-working hours, diarizing...')
            all_records = requests.get(f'{audio_service_api}/records').json()
            for record in sorted(all_records, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'))[::-1]:
                if db.check_if_exists_by_name(record['name']):
                    # logger.debug(f'file {audio_service_api}/record/{record["name"]} is already diarized')
                    continue
                else:
                    logger.debug(f'Diarizing {audio_service_api}/record/{record["name"]}...')
                    resp = requests.get(f'{audio_service_api}/record/{record["name"]}')
                    filename = os.path.join(config['ENV']['ROOT_ABS_PATH'], record["name"])
                    with open(filename, 'wb') as file:
                        file.write(resp.content)
                    diarize(filename)
                    os.remove(filename)
                    break
            sleep(10)
            logger.debug('Check for undiarized files...')
        else:
            logger.debug(f'Working hours, sleeping...')
            sleep(10)


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
        annotation()
        return send_file(BytesIO(visualize(request.headers.get('filename'))), mimetype='image/svg+xml')
    except Exception as e:
        logger.error(e)
        return {'type': str(type(e).__name__), 'message': str(e)}, 500


if __name__ == '__main__':
    auto_diarize_flag = True
    auto_diarizing = threading.Thread(target=start_auto_diarization, daemon=True)
    auto_diarizing.start()
    app.run(host=config['NETWORK']['WEB_API_IP'], debug=False, port=config['NETWORK']['WEB_API_PORT'])