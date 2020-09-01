#!flask/bin/python
#from postgresql_full_text_search import full_text_search # <- он наказанный
import os
from elasticsearch_full_text_search import full_text_search, write
from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
from config_gen import get_config


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
destination = 'http://localhost:4200'
config = get_config()


def wrap_response(response):
    resp = jsonify(response)
    resp.headers.add('Access-Control-Allow-Origin', destination)
    return resp


@app.route('/write', methods=['POST'])
def write_es():

    columns = ['work_place', 'role', 'date_time', 'text']
    print(request.json)
    work_place = request.json['work_place']
    role = request.json['role']
    date_time = request.json['date_time']
    text = request.json['text']
    resp = write(work_place, role, date_time, text)
    resp = jsonify(resp)
    resp.headers.add('Access-Control-Allow-Origin', request.headers['Access-Control-Allow-Origin'])
    return resp


@app.route('/fts', methods=['POST'])
def get_fts_results():
    # TODO решить вопрос с наименованием переменных, в фронте они другие
    columns = ['work_place', 'role', 'date_time_start', 'date_time_end', 'query', 'top']

    results = []
    results_es = full_text_search(
        work_places=request.json['workplaces'],
        date_time_start=request.json['startDate'],
        date_time_end=request.json['endDate'],
        role=request.json['role'],
        query=request.json['text']
    )
    for i in results_es:
        result = {}
        for k, j in enumerate(['id', 'work_place', 'role', 'date_time', 'text']):
            result[j] = i[j]
        results.append(result)

    if not results:
        results.append({'id': 0, 'work_place': 0, 'role': 0, 'date_time': 0, 'text': "Не найдено"})
    print(results)
    resp = wrap_response(results)
    return resp


if __name__ == '__main__':
    app.run(config['NETWORK']['WEB_API_IP'], config['NETWORK']['WEB_API_PORT'], debug=True)
