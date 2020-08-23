# берет все устройства из локальной сети
import os
import json
from raspberry_api import Raspberry
from network_utils import get_active_addresses

from flask import Flask, jsonify, request, abort, send_from_directory, redirect, url_for, Response
from flask_cors import CORS, cross_origin

from audio_logger import get_logger
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


def wrap_response(response):
    resp = jsonify(response)
    resp.headers.add('Access-Control-Allow-Origin', destination)
    return resp


# возвращает список объектов класса Raspberry
def get_raspberries():
    addresses = get_active_addresses()
    raspberries = []
    i = 0
    for ip in addresses:
        logger.debug(f'found ip: {ip}. Trying to connect...')
        if 'raspberries_list' not in os.listdir():
            os.system('touch raspberries_list.txt')
        with open('raspberries_list.txt', 'r+') as list:
            rasp_list = list.read().split('\n')
            if ip not in rasp_list:
                with open('raspberries_list.txt', 'a+') as list:
                    list.write(ip+'\n')
        try:
            raspberries.append(Raspberry(ip, i))
        except Exception as e:
            logger.error(e)
        i += 1
    return raspberries


def get_raspberry_by_ip(ip='127.0.0.1'):
    raspberries = []
    i = 0
    logger.debug(f'found ip: {ip}. Trying to connect...')
    if 'raspberries_list' not in os.listdir():
        os.system('touch raspberries_list.txt')
    with open('raspberries_list.txt', 'r+') as list:
        rasp_list = list.read().split('\n')
        if ip not in rasp_list:
            with open('raspberries_list.txt', 'a+') as list:
                list.write(ip + '\n')
    try:
        raspberries.append(Raspberry(ip, i))
    except Exception as e:
        logger.error(e)
    i += 1
    return raspberries


allowed_extensions = ['wav',]


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


raspberries = get_raspberry_by_ip('127.0.0.1')


@app.route('/microphones', methods=['GET'])
def microphones_list():
    try:
        with open('mic_map.json', 'r') as map_file:
            map_ = json.load(map_file)
        microphones = []
        rasp_dict = {}
        for raspberry in raspberries:
            rasp_dict[raspberry.no] = {
                'ip': raspberry.ip,
                'no': raspberry.no,
                'devices': raspberry.get_devices()
            }
        for raspberry in rasp_dict:
            for card in rasp_dict[raspberry]['devices']:
                for mic in rasp_dict[raspberry]['devices'][card]:
                    workplace = map_[str(raspberry)][str(card)][str(mic)]['workplace']
                    role = map_[str(raspberry)][str(card)][str(mic)]['role']
                    mic_obj = {}
                    for var in ['raspberry', 'card', 'mic', 'workplace', 'role']:
                        mic_obj[var] = locals()[var]
                    microphones.append(mic_obj)
        resp = wrap_response(microphones)
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
    return resp


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


@app.route('/raspberry/update', methods=['GET'])
def update_rasp():
    global raspberries
    raspberries = get_raspberries()
    return redirect(url_for(microphones_list))


@app.route('/stream/<int:raspberry>/<int:card>/<int:mic>', methods=['GET'])
def stream_mic(raspberry, card, mic):
    return Response(raspberries[raspberry].nodes[card].nodes[mic].stream(), mimetype="audio/wav")


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
    app.run(host=config['NETWORK']['WEB_API_IP'], debug=True, port=config['NETWORK']['WEB_API_PORT'])