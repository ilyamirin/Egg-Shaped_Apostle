#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests
import subprocess
import threading
from flask import Flask, jsonify, request, send_from_directory, Response

from datetime import datetime
from time import sleep

from raspberry import Raspberry

from audio_logger import get_logger
from config_gen import get_config
config = get_config()

# set logging level
if config.has_section('SETTINGS') and 'DEBUG' in config['SETTINGS'].keys():
    logger = get_logger("audio_service", config['SETTINGS']['DEBUG'])
else:
    logger = get_logger("audio_service", '1')

raspberry = Raspberry()


def send_file(file_name):
    """Sends file by http protocol, tries to send it by scp if fails"""
    try:
        logger.debug(f'Sending file {file_name} by http...')
        send_file_http(file_name)
    except Exception as e:
        logger.error(f'{e}. Sending file {file_name} by scp...')
        send_scp(file_name)


def send_file_http(file_name,
              dest_ip=config['FILE_SERVER']['web_api_ip'],
              dest_port=config['FILE_SERVER']['web_api_port']):
    """Sends file by http protocol"""
    headers = {
        'content-type': 'audio/vnd.wave'
    }
    try:
        data = open(os.path.join(config['ENV']['DATA_DIR'], file_name), 'rb')
        response = requests.post(f'http://{dest_ip}:{dest_port}/record/{file_name}', headers=headers, data=data)
        response.raise_for_status()
        with open('sent.txt', 'a+') as sent:
            sent.write(file_name + '\n')
        return response.json()
    except Exception as e:
        logger.error(e)
        raise


def send_scp(file_name):
    """Sends file by scp. RSA authentication between server and client is needed"""
    try:
        input_file = os.path.join(config["ENV"]["DATA_DIR"], file_name)
        output_file = os.path.join(config['FILE_SERVER']['DIR'], file_name)
        dest = f"{config['FILE_SERVER']['USERNAME']}@{config['FILE_SERVER']['IP']}"
        logger.debug(f'Sending {input_file} to {dest}\'s {output_file}...')
        process = subprocess.Popen(["scp", '-i', f"{config['ENV']['RSA_DIR']}", input_file, f"{dest}:{output_file}"],
                                   stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE)
        (out, err) = process.communicate()
        if out:
            logger.info(out)
        if err:
            logger.error(err)
        with open('sent.txt', 'a+') as sent:
            sent.write(file_name + '\n')
        return input_file
    except Exception as e:
        logger.error(e)


def parallel_send(files):
    """Sends list of files and check local storage"""
    logger.debug(f'{files} to send')
    for file in files:
        send_file(file)
    files_list = [os.path.join(config["ENV"]["DATA_DIR"], i) for i in os.listdir(config["ENV"]["DATA_DIR"])]
    files_list.sort(key=lambda x: os.path.getmtime(x), reverse=False)
    while len(files_list) > 10:
        file_to_del = files_list[0]
        logger.debug(f'Amount of files exceeded ({len(files_list)}/10). Deleting  {file_to_del}...')
        os.remove(file_to_del)
        files_list = files_list[1:]


def parallel_record(time):
    threads = []
    for card in raspberry.nodes:
        for mic in card.nodes:
            threads.append(threading.Thread(target=mic.record, args=[int(time) if time else None]))
    for thread in threads:
        thread.start()
    sleep(1)
    for thread in threads:
        thread.join()


def record_by_work_time(time=None):
    global recording_flag
    start_hour = datetime.time(datetime.strptime(config["SETTINGS"]["START_HOUR"], '%H:%M'))
    end_hour = datetime.time(datetime.strptime(config["SETTINGS"]["END_HOUR"], '%H:%M'))
    logger.info(f'start record by time between {config["SETTINGS"]["START_HOUR"]} and {config["SETTINGS"]["END_HOUR"]}...')
    while recording_flag:
        date_now = datetime.date(datetime.now())
        start_datetime = datetime.combine(date_now, start_hour)
        end_datetime = datetime.combine(date_now, end_hour)
        start_delta = datetime.now().timestamp() - start_datetime.timestamp()
        end_delta = datetime.now().timestamp() - end_datetime.timestamp()
        if start_delta > 0 > end_delta:
            logger.debug(f'Working hours, recording...')
            parallel_record(time)
            #sleep(time if time else int(config['SETTINGS']['RECORD_DUR']))
        else:
            logger.debug(f'Not working hours, sleeping...')
            sleep(10)


def get_sent_files():
    if 'sent.txt' in os.listdir('./'):  # проверяем, есть ли список уже отправленных файлов
        with open('sent.txt', 'r') as sent:
            sent_files = sent.read().split('\n')  # читаем, если есть
    else:
        with open('sent.txt', 'w') as sent:
            sent.close()
        sent_files = []
    return sent_files


# получаем дополнение мн-ва распознанных файлов ко всем, set быстрее в таких операциях
def get_new_records():
    old_records = set(get_sent_files())
    try:
        records = set(raspberry.get_files_list())
    except Exception as e:
        records = old_records
        logger.error(e)
    return records - old_records


def send_by_adding():
    global sending_flag
    while sending_flag:
        files = get_new_records()
        if files:
            parallel_send(files)
        else:
            print('no new files...')
            sleep(1)

# Web API

app = Flask(__name__)


def wrap_response(response):
    resp = jsonify(response)
    return resp


#  card, mic, time, file
@app.route('/record', methods=['POST'])
def start_record():
    try:
        file = raspberry.nodes[int(request.args['card'])].nodes[int(request.args['mic'])].start_record(request.args['time'])
        resp = wrap_response({'response': f'{file}'})
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
    return resp


@app.route('/records', methods=['GET'])
def get_records():
    try:
        resp = wrap_response(raspberry.get_files_list())
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
        resp = wrap_response(raspberry.get_devices())
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


# TODO сделать обход json-объекта с конфигом с заменой
@app.route('/config', methods=['POST'])
def set_config():
    with open('config.ini', 'w') as config_file:
        config_file.write(request.json['config'])
    resp = jsonify({'response': 'ok'})
    return resp


@app.route('/parallel_rec/start', methods=['POST'])
def start_parallel_record():
    global recording_flag, recording
    try:
        recording_flag = True
        recording = threading.Thread(target=record_by_work_time(), args=[int(request.form['time'])])
        recording.start()
        resp = wrap_response({'response': 'ok'})
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
    return resp


@app.route('/parallel_rec/stop', methods=['GET'])
def stop_parallel_record():
    global recording_flag
    try:
        recording_flag = False
        resp = wrap_response({'response': 'ok'})
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
    return resp


stream_flag = False


@app.route('/stream/<int:card>/<int:mic>', methods=['GET'])
def stream_from_mic(card, mic):
    global stream_flag
    stream_flag = True

    def generate():
        while stream_flag:
            yield raspberry.cards[card].mics[mic].buf
    return Response(generate(), mimetype="audio/x-wav")


if __name__ == '__main__':
    recording_flag = True
    sending_flag = True
    recording = threading.Thread(target=record_by_work_time, daemon=True)
    sending = threading.Thread(target=send_by_adding, daemon=True)
    sending.start()
    recording.start()
    app.run(host=config['NETWORK']['WEB_API_IP'], port=config['NETWORK']['WEB_API_PORT'], debug=True)



