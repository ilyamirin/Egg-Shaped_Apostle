import os
import json
from time import sleep
import threading
from flask import Flask, jsonify, request, abort
from flask_cors import CORS

from interface import *

from config_gen import get_config
from logger import get_logger
config = get_config()
if config.has_section('SETTINGS'):
    if 'DEBUG' in config['SETTINGS'].keys():
        logger = get_logger("text_service", config['SETTINGS']['DEBUG'])
else:
    logger = get_logger("audio_service", '1')

if config['SETTINGS']['RECOGNIZER'] == 'yandex':
    print('yandex Speech Kit is settled as recognizer')
    from speech_recognition.yandex_speech_kit_recognition import yandex_speech_kit_realtime_recognition as recognizer

elif config['SETTINGS']['RECOGNIZER'] == 'kaldi':
    print('Kaldi is settled as recognizer')
    from speech_recognition.kaldi import kaldi_recognition as recognizer

# from services.text_service.postgreSQL_write import write_row
# from fts_service.elasticsearch_full_text_search import write

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
destination = 'localhost:5722'


def get_recognized_files():
    if 'recognized.txt' in os.listdir('./'):  # проверяем, есть ли список уже сконвертированных файлов
        with open('recognized.txt', 'r') as recognized:
            recognized_files = recognized.read().split('\n')  # читаем, если есть
    else:
        with open('recognized.txt', 'w') as recognized:
            recognized.close()
        recognized_files = []
    return recognized_files


# получаем дополнение мн-ва распознанных файлов ко всем, set быстрее в таких операциях
def get_new_records():
    records = set(get_list_of_records())
    old_records = set(get_recognized_files())
    return records - old_records


def wrap_response(response):
    resp = jsonify(response)
    resp.headers.add('Access-Control-Allow-Origin', destination)
    return resp


@app.route('/recognize', methods=['POST'])
def recognize_ext():
    record = request.form['filename']
    audio = download_record(record)
    if config['SETTINGS']['RECOGNIZER'] == 'kaldi':
        with open('audio_recognize.wav', 'wb+') as file:
            file.write(audio)
            file.close()
            text = recognizer.recognize_audio(config['ENV']['ROOT_ABS_PATH'], '/audio_recognize.wav')
    elif config['SETTINGS']['RECOGNIZER'] == 'yandex':
        text = recognizer.recognize_audio(audio)['result']
    with open('recognized.txt', 'a+') as recognized_files:
        recognized_files.write(record+'\n')
    return wrap_response({'response': text})


def recognize(record):
    audio = download_record(record)
    if config['SETTINGS']['RECOGNIZER'] == 'kaldi':
        with open('audio_recognize.wav', 'wb+') as file:
            file.write(audio)
            file.close()
            text = recognizer.recognize_audio(config['ENV']['ROOT_ABS_PATH'], '/audio_recognize.wav')
    else: # config['SETTINGS']['RECOGNIZER'] == 'yandex':
        text = recognizer.recognize_audio(audio)['result']
    with open('recognized.txt', 'a+') as recognized_files:
        recognized_files.write(record+'\n')
    return text


def extract_metadata(filename):
    raspberry, card, device, date = filename[:-4].split('_')  # разбиваем название файла по "_", получаем метаданные расположения
    if 'mic_map.txt' in os.listdir('.'):
        with open('mic_map.txt', 'r') as map_file:
            map = json.load(map_file)
            workplace = map[raspberry][card][device]['workplace']
            role = map[raspberry][card][device]['role']
    else:
        workplace = raspberry
        role = 0
    return workplace, role, date


def main():
    while True:
        new_records = get_new_records()
        if new_records:
            for record in new_records:
                text = recognize(record)
                workplace, role, datetime = extract_metadata(record)
                # write_es(workplace, role, datetime, text)
                write_pg(workplace, role, datetime, text)
        else:
            sleep(1)


if __name__ == '__main__':
    a = threading.Thread(target=main)
    a.start()
    app.run(host='127.0.0.1', port=config['NETWORK']['WEB_API_PORT'])
