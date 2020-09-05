#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import threading
from flask import Flask, jsonify, request, send_from_directory, Response
from time import sleep
from flask_cors import CORS

from raspberry import Raspberry

from audio_logger import get_logger
from config_gen import get_config
config = get_config()

# set logging level
if config.has_section('SETTINGS') and 'DEBUG' in config['SETTINGS'].keys():
    logger = get_logger('audio_service', config['SETTINGS']['DEBUG'])
else:
    logger = get_logger('audio_service', '1')

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
destination = 'http://192.168.0.1:5722'


@app.route('/<int:card>/<int:mic>/record', methods=['POST'])
def start_record(card, mic):
    try:
        record_thread = threading.Thread(target=raspberry.cards[card].mics[mic].record,
                                         args=[int(request.args['time']) if 'time' in request.args else None,
                                               request.args['file'] if 'file' in request.args else None])
        record_thread.start()
        return jsonify({'response': f'ok'})
    except Exception as e:
        logger.error(e)
        raise


@app.route('/records', methods=['GET'])
def get_records():
    try:
        return jsonify(raspberry.get_files_list())
    except Exception as e:
        logger.error(e)
        raise


@app.route('/send', methods=['POST'])
def send():
    try:
        return send_from_directory(config['ENV']['DATA_DIR'], request.args['filename'])
    except Exception as e:
        logger.error(e)
        raise


@app.route('/devices', methods=['GET'])
def get_devices():
    try:
        return jsonify(raspberry.get_devices())
    except Exception as e:
        logger.error(e)
        raise


@app.route('/config', methods=['GET'])
def get_config():
    if 'config.ini' in os.listdir('.'):
        with open('config.ini', 'r') as config:
            resp = jsonify(config.read())
    else:
        resp = jsonify({'error': 'there is no config'})
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
    global recording
    try:
        if raspberry.recording_flag:
            raspberry.recording_flag = False
            sleep(1)
        raspberry.recording_flag = True
        recording = threading.Thread(target=raspberry.record_by_work_time,
                                     args=[int(request.args['time']) if 'time' in request.args else None],
                                     daemon=True)
        recording.start()
        print(raspberry.recording_flag)
        return jsonify({'response': 'ok'})
    except Exception as e:
        logger.error(e)
        raise


@app.route('/parallel_rec/stop', methods=['GET'])
def stop_parallel_record():
    try:
        if raspberry.recording_flag:
            raspberry.recording_flag = False
            sleep(1)
            resp = jsonify({'response': 'ok'})
        else:
            resp = jsonify({'response': 'nothing to stop'})
        return resp
    except Exception as e:
        logger.error(e)
        raise


def gen_header(sample_rate=int(config["SETTINGS"]["RECORD_SAMPLING_RATE"]), bits_per_sample=16, channels=1):
    datasize = 2000*10**3
    o = bytes("RIFF", 'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4, 'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE", 'ascii')                                              # (4byte) File type
    o += bytes("fmt ", 'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4, 'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2, 'little')                                           # (2byte) Format type (1 - PCM)
    o += channels.to_bytes(2, 'little')                                    # (2byte)
    o += sample_rate.to_bytes(4, 'little')                                  # (4byte)
    o += (sample_rate * channels * bits_per_sample // 8).to_bytes(4, 'little')  # (4byte)
    o += (channels * bits_per_sample // 8).to_bytes(2, 'little')               # (2byte)
    o += bits_per_sample.to_bytes(2, 'little')                               # (2byte)
    o += bytes("data", 'ascii')                                              # (4byte) Data Chunk Marker
    o += datasize.to_bytes(4, 'little')                                    # (4byte) Data size in bytes
    return o


def flatten(samples_in, way=0, window=100):
    ''' gets samples and flatten them.
    Way=0 - ascending, way=1 - descending '''
    k = 1 if way else 0
    samples = []
    for i in samples_in:
        samples.append(int(i*k))
        if way:
            k -= k/window
        else:
            k += 1/window
    # print(samples)
    return samples

# experimental
# def cut_ends(pcm_samples):
#     window = 100
#     start = pcm_samples[:window]
#     end = pcm_samples[-window:]
#     pcm_samples_start = flatten(start)
#     pcm_samples_end = flatten(end, 1)
#     pcm_samples = bytearray(pcm_samples_start) + pcm_samples[window:]
#     pcm_samples = pcm_samples[:-window] + bytearray(pcm_samples_end)
#     return pcm_samples


@app.route('/<int:card>/<int:mic>/stream', methods=['GET'])
def stream_from_mic(card, mic):
    global stream_flag
    stream_flag = True
    wav_header = gen_header()
    first_time = True

    def generate():
        nonlocal first_time
        while stream_flag:
            chunk = raspberry.cards[card].mics[mic].read_stream()
            if first_time:
                chunk = wav_header + chunk
                first_time = False
            sleep(1)
            yield chunk

    return Response(generate(), mimetype="audio/wav")


@app.route('/status', methods=['GET'])
def send_status():
    return jsonify(raspberry.get_status())


if __name__ == '__main__':
    raspberry = Raspberry()
    raspberry.recording_flag = True
    raspberry.sending_flag = True
    recording = threading.Thread(target=raspberry.record_by_work_time, daemon=True)
    sending = threading.Thread(target=raspberry.send_by_adding, daemon=True)
    sending.start()
    recording.start()
    app.run(host=config['NETWORK']['WEB_API_IP'], port=config['NETWORK']['WEB_API_PORT'])