# берет все устройства из локальной сети
import os
import json
from raspberry_api import Raspberry
from datetime import datetime

from flask import Flask, jsonify, request, send_from_directory, redirect, url_for, Response
from flask_cors import CORS

from audio_logger import get_logger
from config_gen import get_config
config = get_config()
logger = get_logger("audio_service", config['SETTINGS']['DEBUG'])

if not os.path.exists(config['ENV']['EXT_DATA_DIR']):
    logger.debug('can\'t find data dir, trying to create...')
    try:
        os.makedirs(config['ENV']['EXT_DATA_DIR'])
    except Exception as e:
        logger.error(e)


def read_rasp_map() -> dict:
    rasp_map = {}
    try:
        with open('raspberries.json', 'r') as rasp_map_file:
            rasp_map = json.load(rasp_map_file)
    except json.decoder.JSONDecodeError:
        logger.debug('there is no raspberries declared')
    except FileNotFoundError:
        logger.debug('no raspberries.json in directory')
    except Exception as e:
        logger.error(e)
    return rasp_map


def get_raspberries():
    """
    loads raspberries.json
    """
    _raspberries_ = []
    rasp_map = read_rasp_map()
    for ip in rasp_map:
        _raspberries_.append(Raspberry(ip))

    return _raspberries_


def extract_metadata(filename):
    raspberry, card, device, date = filename[:-4].split(
        '_')  # разбиваем название файла по "_", получаем метаданные расположения
    workplace = raspberry
    role = 0
    if 'mic_map.json' in os.listdir('.'):
        with open('mic_map.json', 'r') as map_file:
            map = json.load(map_file)
            try:
                workplace = map[raspberry][card][device]['workplace']
                role = map[raspberry][card][device]['role']
            except KeyError:
                pass
    return workplace, role, date

max_workplace = 0
for filename in os.listdir(config['ENV']['EXT_DATA_DIR']):
    workplace_cur, role_cur, date_cur = extract_metadata(filename)
    workplace_cur = int(workplace_cur)
    max_workplace = workplace_cur if max_workplace < workplace_cur else max_workplace

def wrap_response(response):
    resp = jsonify(response)
    resp.headers.add('Access-Control-Allow-Origin', destination)
    return resp


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
destination = f'http://{config["NETWORK"]["FRONTEND_IP"]}:{config["NETWORK"]["FRONTEND_PORT"]}'


# records API


@app.route('/records', methods=['GET'])
def get_records():
    try:
        records = [i for i in os.listdir(config['ENV']['EXT_DATA_DIR']) if i.endswith('.wav')]
        record_obj_list = []
        id_ = 0
        for record in records:
            record_obj = {}
            workplace, role, date = extract_metadata(record)
            record_obj['id'] = id_
            record_obj['name'] = record
            record_obj['workplace'] = workplace
            record_obj['role'] = role
            record_obj['date'] = date
            record_obj['url'] = f"http://{config['NETWORK']['WEB_API_IP']}:" \
                                f"{config['NETWORK']['WEB_API_PORT']}" \
                                f"{url_for('get_record', filename=record)}"
            record_obj_list.append(record_obj)
            id_ += 1
        resp = wrap_response(record_obj_list)
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
    return resp


@app.route('/record/<filename>', methods=['GET'])
def get_record(filename):
    try:
        return send_from_directory(config['ENV']['EXT_DATA_DIR'], filename)
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
        return resp


@app.route('/record/<filename>', methods=['POST'])
def post_record(filename):
    try:
        if not os.path.exists(config['ENV']['EXT_DATA_DIR']):
            os.makedirs(config['ENV']['EXT_DATA_DIR'])
        with open(os.path.join(config['ENV']['EXT_DATA_DIR'], filename), 'wb') as audio_file:
            audio_file.write(request.data)
        resp = wrap_response({'result': 'ok'})
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'result': 'error', 'error': e})
    return resp


@app.route('/records/update', methods=['GET'])
def get_update():
    try:
        records = []
        old_records = set(get_records().json)
        for raspberry in raspberries:
            local_records = set(raspberry.get_records())
            new_records = local_records - old_records
            for filename in new_records:
                raspberry.send(config['ENV']['EXT_DATA_DIR'], filename)
            records.append(list(new_records))
        print(records)
        resp = wrap_response({'response': records})
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
    return resp


# TODO: add to README.md
@app.route('/records/filter', methods=['POST'])
def filter_records():
    try:
        #print(request.json['date_time_start'])
        work_places = request.json['work_places'] if 'work_places' in request.json else list(range(max_workplace+1))
        # print(request.json['work_places'])
        # print(work_places)
        roles = [int(i) for i in request.json['roles']] if 'roles' in request.json else [0, 1]
        if 2 in roles: roles = [0, 1]
        date_time_start = datetime.strptime(request.json['date_time_start'], '%Y-%m-%dT%H:%M:%S.%fZ')\
            if 'date_time_start' in request.json else datetime.strptime('2020-01-01T00:00:00.000', '%Y-%m-%dT%H:%M:%S.%f')
        date_time_end = datetime.strptime(request.json['date_time_end'], '%Y-%m-%dT%H:%M:%S.%fZ')\
            if 'date_time_end' in request.json else datetime.strptime('2099-01-01T00:00:00.000', '%Y-%m-%dT%H:%M:%S.%f')
        # print(request.json)
        #print(roles)
        results = []
        id_ = 0
        for filename in os.listdir(config['ENV']['EXT_DATA_DIR']):
            # print(filename)
            workplace_cur, role_cur, date_cur = extract_metadata(filename)
            workplace_cur = int(workplace_cur)
            role_cur = int(role_cur)
            date_cur = datetime.strptime(date_cur, '%Y-%m-%dT%H:%M:%S.%f')
            # print(workplace_cur, '--', work_places)
            # print(role_cur, '--', roles)
            # print(date_time_start, date_cur, date_time_end)
            if workplace_cur in work_places and role_cur in roles and date_time_start <= date_cur <= date_time_end:
                record_obj = {}
                record_obj['id'] = id_
                record_obj['name'] = filename
                record_obj['workplace'] = workplace_cur
                record_obj['role'] = role_cur
                record_obj['date'] = date_cur
                record_obj['url'] = f"http://{config['NETWORK']['WEB_API_IP']}:" \
                                    f"{config['NETWORK']['WEB_API_PORT']}" \
                                    f"{url_for('get_record', filename=filename)}"
                results.append(record_obj)
                id_ += 1
        return jsonify(results), 200
    except Exception as e:
        logger.error(e)
        return {'type': str(type(e).__name__), 'message': str(e)}, 500


@app.route('/records/send', methods=['GET'])
def send():
    try:
        print(request.form)
        print(config['ENV']['EXT_DATA_DIR'], request.form['filename'])
        resp = send_from_directory(config['ENV']['EXT_DATA_DIR'], request.form['filename'])
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
    return resp


# Devices API


@app.route('/raspberry', methods=['GET'])
def raspberries_list():
    rasp_dict = {}
    for raspberry in raspberries:
        rasp_dict[raspberry.no] = {
            'ip': raspberry.ip,
            'no': raspberry.no,
            'devices': raspberry.get_devices()
        }
    return wrap_response(rasp_dict)


@app.route('/microphones', methods=['GET'])
def microphones_list():
    try:
        rasp_map = read_rasp_map()
        microphones = []
        rasp_dict = {}
        for rasp_ip in rasp_map:
            raspberry = rasp_map[rasp_ip]['no']
            cards = rasp_map[rasp_ip]['cards']
            for card in cards:
                mics = cards[card]
                for mic in mics:
                    workplace = mics[mic]['work_place']
                    role = mics[mic]['role']
                    for rasp in raspberries:
                        if rasp.no == raspberry:
                            if card in rasp.details and mic in rasp.details[card]:
                                status = rasp.details[card][mic]['status']
                            else:
                                status = 'no'
                    mic_obj = {}
                    for var in ['raspberry', 'card', 'mic', 'workplace', 'role', 'status']:
                        mic_obj[var] = locals()[var]
                    microphones.append(mic_obj)
            print(microphones)
        resp = wrap_response(microphones)
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
        raise
    return resp
# returns only alive
# def microphones_list():
#     try:
#         with open('mic_map.json', 'r') as map_file:
#             map_ = json.load(map_file)
#         microphones = []
#         rasp_dict = {}
#         for raspberry in raspberries:
#             rasp_dict[raspberry.no] = {
#                 'ip': raspberry.ip,
#                 'no': raspberry.no,
#                 'devices': raspberry.get_devices()
#             }
#         for raspberry in rasp_dict:
#             for card in rasp_dict[raspberry]['devices']:
#                 for mic in rasp_dict[raspberry]['devices'][card]:
#                     workplace = map_[str(raspberry)][str(card)][str(mic)]['workplace']
#                     role = map_[str(raspberry)][str(card)][str(mic)]['role']
#                     mic_obj = {}
#                     for var in ['raspberry', 'card', 'mic', 'workplace', 'role']:
#                         mic_obj[var] = locals()[var]
#                     microphones.append(mic_obj)
#         resp = wrap_response(microphones)
#     except Exception as e:
#         logger.error(e)
#         resp = wrap_response({'error': str(e)})
#     return resp


@app.route('/raspberry/update', methods=['GET'])
def update_rasp():
    global raspberries
    raspberries = get_raspberries()
    return redirect(url_for(microphones_list))


@app.route('/stream/<int:raspberry>/<int:card>/<int:mic>', methods=['GET'])
def stream_mic(raspberry, card, mic):
    #print(raspberries[raspberry].nodes)
    target = None
    for rasp in raspberries:
        if int(rasp.no) == raspberry:
            target = rasp
            break
    return Response(target.nodes[card-1].nodes[mic].stream(), mimetype="audio/wav")


@app.route('/raspberry/all/<command>', methods=['GET', 'POST'])
@app.route('/raspberry/all/<command>/<subcommand>', methods=['GET', 'POST'])
def to_all_raspberries(command, subcommand=None):
    resp = []
    for raspberry in raspberries:
        if request.method == 'GET':
            if command == 'records':
                return wrap_response(raspberry.get_records())
            elif command == 'devices':
                return wrap_response(raspberry.get_devices())
            elif command == 'config':
                return wrap_response(raspberry.get_config())
            elif command == 'parallel_rec' and subcommand == 'stop':
                return wrap_response(raspberry.stop_parallel_record())
        elif request.method == 'POST':
            if command == 'record':
                print(request.form)
                return wrap_response(raspberry.record(request.form['card'], request.form['mic'], request.form['time']))
            if command == 'send':
                return wrap_response(raspberry.send(config['ENV']['EXT_DATA_DIR'], request.form['filename']))
            elif command == 'config':
                return wrap_response(raspberry.set_config(request.json['config']))
            elif command == 'parallel_rec' and (not subcommand or subcommand == 'start'):
                return wrap_response(raspberry.start_parallel_record(request.form['time']))
        else:
            return wrap_response({'error': 'no such command'})
    return wrap_response(resp)


@app.route('/raspberry/<int:no>/<command>', methods=['GET', 'POST'])
@app.route('/raspberry/<int:no>/<command>/<subcommand>', methods=['GET', 'POST'])
def to_raspberry(no, command, subcommand=None):
    logger.debug(f'{no}, {command}, {subcommand}')
    raspberry = None
    for i in raspberries:
        if i.no == no:
            raspberry = i
            break
    if raspberry:
        if request.method == 'GET':
            if command == 'records':
                return wrap_response(raspberry.get_records())
            elif command == 'devices':
                return wrap_response(raspberry.get_devices())
            elif command == 'config':
                return wrap_response(raspberry.get_config())
            elif command == 'parallel_rec' and subcommand == 'stop':
                return wrap_response(raspberry.stop_parallel_record())
        elif request.method == 'POST':
            if command == 'record':
                print(request.form, request.args)
                return wrap_response(raspberry.record(request.form['card'], request.form['mic'], request.form['time']))
            if command == 'send':
                return wrap_response(raspberry.send(config['ENV']['EXT_DATA_DIR'], request.form['filename']))
            elif command == 'config':
                return wrap_response(raspberry.set_config(request.json['config']))
            elif command == 'parallel_rec' and (not subcommand or subcommand == 'start'):
                return wrap_response(raspberry.start_parallel_record(request.form['time']))
        else:
            return wrap_response({'error': 'no such command'})
    else:
        return wrap_response({'error': 'No raspberry with that number'})


if __name__ == '__main__':
    raspberries = get_raspberries()
    app.run(host=config['NETWORK']['WEB_API_IP'], debug=True, port=config['NETWORK']['WEB_API_PORT'])