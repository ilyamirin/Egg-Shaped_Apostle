from datetime import datetime
from elasticsearch import Elasticsearch
import json
import requests as rq
es = Elasticsearch()
from datetime import datetime

from config_gen import get_config
config = get_config()

# параметры сервера ElasticSearch

es_api = f"http://{config['NETWORK']['ES_IP']}:{config['NETWORK']['ES_PORT']}/"

# название индекса, с которым работаем
# заголовки http-реквестов, пока только указание типа контента
headers = {
        'Content-Type': 'application/json'
    }


# запись документа в индекс
def write(work_place, role, date_time, text):
    params = {
    }
    analyzed_text = analyze(text)
    data = {
        'work_place': work_place,
        'role': role,
        'date_time': date_time,
        'text': text,
        'analyzed_text': analyzed_text
    }
    res = rq.post(es_api+f"{config['SETTINGS']['ES_INDEX']}/_doc/", headers=headers, params=params, data=data).json()
    return res


# проанализированное представление записи
def analyze(text):
    # для дебага ставь pretty="true", убирай .json() с res = ....json() и возвращай res.text
    params = {"pretty": "true",}
    data = json.dumps({'text': text})
    res = rq.post(es_api+'rebuilt_russian/_analyze', headers=headers, params=params, data=data).json()
    # clear response from unused data
    # print(res)
    return " ".join([i['token'] for i in res['tokens']])


def full_text_search(work_places=[1,], role=1, date_time_start=None, date_time_end=None, query='', top=5):
    work_places = [int(i) for i in work_places]
    role = int(role)
    path_params = f"{config['SETTINGS']['ES_INDEX']}/_search/"
    if date_time_start:
        date_time_start = datetime.strptime(date_time_start, '%Y-%m-%dT%H:%M:%S.%fZ')
    if date_time_end:
        date_time_end = datetime.strptime(date_time_end, '%Y-%m-%dT%H:%M:%S.%fZ')
    # для дебага ставь pretty="true", убирай .json() с res = ....json() и возвращай res.text
    # print(analyze(query))
    params = {
        "pretty": "false",
        '_source': 'true'
        #"analyzer": "rebuilt_russian"
    }
    data = json.dumps(
        {'query': {
            'bool': {
                'must':
                    [
                        {'match':
                             {'analyzed_text': analyze(query)},
                         },
                    ],
                #'should': [{'match': i} for i in work_place]
            }
        }

         }
    )

    res = rq.post(es_api+path_params, headers=headers, params=params, data=data).json()
    # TODO сделать фильтрацию
    # clear response from unused data
    if res != {}:
        results = []
        for i in res['hits']['hits']:
            result = i['_source']
            result['id'] = i['_id']
            result['date_time'] = result['date_time'][:-1] if result['date_time'].endswith('Z') else result['date_time']
            result['date_time'] = datetime.strptime(result['date_time'], '%Y-%m-%dT%H:%M:%S.%f')
            if result['work_place'] in work_places and\
                    (role == -1 or result['role'] == role) and\
                    ((not date_time_start) or (result['date_time'] > date_time_start)) and\
                    ((not date_time_end) or (result['date_time'] < date_time_end)):
                results.append(result)
    else: results = []
    return results


def return_by_id(id):
    return es.search(index=config['SETTINGS']['ES_INDEX'], body={'query': {'match': {'_id': id}}})

# print(full_text_search(work_places=[1,], date_time_end='2020-03-25T20:00:00.000Z', role=-1, query='привет'))
#print(return_by_id('lbxPDXEBgHmjTYGDLXch'))
#_analyze?pretty&analyzer=standard&text=%D0%92%D0%B5%D1%81%D0%B5%D0%BB%D1%8B%D0%B5%20%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D0%B8%20%D0%BF%D1%80%D0%BE%20%D0%BA%D0%BE%D1%82%D1%8F%D1%82"
#print(rq.get(server_address+'_analyze', params=params))
'''
data = {
    'analyzer': 'russian',
    'text': 'маму'
}
#request = rq.get('http://'+server_address+'/_analyze', headers=headers, data=data)
#print(request.headers.items())
headers = {
    'Content-Type': 'application/json'
}
request = rq.put('http://localhost:9200/russian_analyzer', headers=headers, data=json.dumps(
{
  "settings": {
    "analysis": {
      "filter": {
        "russian_stop": {
          "type":       "stop",
          "stopwords":  "_russian_"
        },
        "russian_stemmer": {
          "type":       "stemmer",
          "language":   "russian"
        }
      },
      "analyzer": {
        "rebuilt_russian": {
          "tokenizer":  "standard",
          "filter": [
            "lowercase",
            "decimal_digit",
            "russian_stop",
            #"russian_normalization",
            "russian_keywords",
            "russian_stemmer"
          ]
        }
      }
    }
  }
}))
print(rq.get('http://localhost:9200/russian_analyzer', headers=headers, data=data).text)
data = json.dumps(
    {
        #'analyzer': 'russian_analyzer',
        'text': 'маму мыла 1 рама'
    }
)
request = rq.get('http://localhost:9200/russian_analyzer/_analyze?pretty', headers=headers, data=data)
print(request.text)'''