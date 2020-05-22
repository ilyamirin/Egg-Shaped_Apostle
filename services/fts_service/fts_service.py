#!flask/bin/python
#from postgresql_full_text_search import full_text_search # <- он наказанный
import os
import subprocess
import configparser
from elasticsearch_full_text_search import full_text_search
from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
from datetime import datetime


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

config = configparser.ConfigParser()
print('Reading configuration file...', end='\n')

if not 'config.ini' in os.listdir('.'):
    print('Unable to find config file, create one with default settings...')
    config['ENV'] = {
        'ROOT_ABS_PATH': os.getcwd(),
        'EXT_DATA_DIR': '/home/sde/Desktop/projects/Egg-Shaped_Apostle/data/'
    }

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

config.read('config.ini')
print('OK')

@app.route('/fts', methods=['POST'])
def get_fts_results():

    columns = ['work_place', 'role', 'date_time_start', 'date_time_end', 'query', 'top']

    print(request.json)

    kwargs = {i: request.json[i] for i in columns if i in request.json.keys()}
    results = []

    for i in full_text_search(**kwargs):
        result = {}
        for k, j in enumerate(['id', 'work_place', 'role', 'date_time', 'text']):
            #print(k, j)
            #print(enumerate(['id', 'work_place', 'role', 'date_time', 'text']))
            result[j] = i[j]
        results.append(result)

    if results == []:
        results.append({'id':0, 'work_place': 0, 'role': 0, 'date_time': 0, 'text': "Не найдено"})

    resp = jsonify({'search_results': results})
    resp.headers.add('Access-Control-Allow-Origin', 'http://localhost:4200')

    print(results)

    return resp


@app.route('/record', methods=['POST'])
def record():
    file_name = f'{config["ENV"]["EXT_DATA_DIR"]}0_0_0_{str(datetime.now()).replace(" ", "T")}.wav'
    #if not request.json or not 'title' in request.json:
    #    abort(400)
    print(request.json)
    #if "card" in request.json and "mic" in request.json:
    #    rec_ps = subprocess.Popen(
    #        [r'/usr/bin/arecord', '-f', 'cd', '-D' f'plughw:{request.json["card"]},{request.json["mic"]}', '-c', '1', '-d', f'{request.json["time"]}',
    #         file_name])
    #else:
    rec_ps = subprocess.Popen(
        [r'/usr/bin/arecord', '-f', 'cd', '-D' f'plughw:{0},{0}', '-c', '1', '-d', f'{request.json["time"]}',
         file_name])
    result = rec_ps.wait()
    resp = jsonify({"res": result})
    print(result)
    return resp


if __name__ == '__main__':
    app.run()
#full_text_search(query='какого')