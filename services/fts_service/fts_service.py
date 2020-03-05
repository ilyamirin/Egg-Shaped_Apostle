#!flask/bin/python
from full_text_search import full_text_search
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
#from json import

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/fts', methods=['POST'])
def get_fts_results():

    columns = ['work_place', 'role', 'date_time_start', 'date_time_end', 'query', 'top']

    print(request.json)

    kwargs = {i: request.json[i] for i in columns if i in request.json.keys()}
    results = []

    for i in full_text_search(**kwargs):
        result = {}
        for k, j in enumerate(['id', 'work_place', 'role', 'date_time', 'text']):
            result[j] = i[k]
        results.append(result)

    if results == []:
        results.append({'id':0, 'work_place':0, 'role':0, 'date_time':0, 'text': "Не найдено"})

    resp = jsonify({'search_results': results})
    resp.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:4200')

    print(results)

    return resp

if __name__ == '__main__':
    app.run()
