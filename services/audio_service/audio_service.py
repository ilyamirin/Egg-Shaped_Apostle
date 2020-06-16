# берет все устройства из локальной сети
import os
from raspberry_api import Raspberry
from network_utils import get_active_addresses

from flask import Flask, jsonify, request, abort, send_from_directory
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
destination = 'localhost:4200'


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


@app.route('/records', methods=['GET'])
def get_records():
    try:
        return wrap_response([i for i in os.listdir(config['ENV']['EXT_DATA_DIR']) if i.endswith('.wav')])
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
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
print(raspberries)


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


@app.route('/raspberry/<int:no>/<command>', methods=['GET', 'POST'])
@app.route('/raspberry/<int:no>/<command>/<subcommand>', methods=['GET', 'POST'])
def to_raspberry(no, command, subcommand=None):
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
            else:
                return wrap_response({'error': 'no such command'})
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
                return wrap_response({'error' : 'no such command'})
    else: return wrap_response({'error': 'No raspberry with that number'})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=config['NETWORK']['WEB_API_PORT'])