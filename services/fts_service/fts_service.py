#!flask/bin/python
from full_text_search import full_text_search
from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/fts', methods=['POST'])
def get_fts_results():
    columns = ['work_place', 'role', 'date_time_start', 'date_time_end', 'query', 'top']
    kwargs = {i: request.args.get(i) for i in columns if request.args.get(i)}
    results = []
    for i in full_text_search(**kwargs):
        result = {}
        for k, j in enumerate(['id', 'work_place', 'role', 'date_time', 'text']):
            result[j] = i[k]
        results.append(result)
    return jsonify({'search_results': results})


if __name__ == '__main__':
    app.run(debug=True)