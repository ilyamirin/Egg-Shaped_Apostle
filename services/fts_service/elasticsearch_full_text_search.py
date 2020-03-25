from datetime import datetime
from elasticsearch import Elasticsearch
import json
import requests as rq
es = Elasticsearch()

# параметры сервера ElasticSearch
es_server_ip = 'localhost'
es_server_port = 9200
es_server_address = f'http://{es_server_ip}:{es_server_port}/'

# название индекса, с которым работаем
index = 'testindex1'

# заголовки http-реквестов, пока только указание типа контента
headers = {
        'Content-Type': 'application/json'
    }


#проанализированное представление записи
def analyze(text):

    '''
        req = rq.put('http://localhost:9200/rebuilt_russian', headers=headers, data=json.dumps(
            {
                "settings": {
                    "analysis": {
                        "filter": {
                            "russian_stop": {
                                "type": "stop",
                                "stopwords": "_russian_"
                            },
                            "russian_stemmer": {
                                "type": "stemmer",
                                "language": "russian"
                            }
                        },
                        "analyzer": {
                            "rebuilt_russian": {
                                "tokenizer": "standard",
                                "filter": [
                                    "lowercase",
                                    "decimal_digit",
                                    "russian_stop",
                                    # "russian_normalization",
                                    #"russian_keywords",
                                    "russian_stemmer"
                                ]
                            }
                        }
                    }
                }
            }))

        print(req.text)'''

    path_params = f'rebuilt_russian/_analyze'

    # для дебага ставь pretty="true", убирай .json() с res = ....json() и возвращай res.text
    params = {
        "pretty": "true",
    }

    data = json.dumps(
        {'analyzer': 'rebuilt_russian', 'text': text}
    )

    # the next request returns something like that:

    res = rq.post(es_server_address + path_params, headers=headers, params=params, data=data).json()

    # clear response from unused data
    return " ".join([i['token'] for i in res['tokens']])

#print(analyze(""))

# запись документа в индекс
def write(work_place, role, date_time, text):

    path_params = f'{index}/_doc/'

    params = {
    }

    analyzed_text = analyze(text)

    data = json.dumps({
        'work_place': work_place,
        'role': role,
        'date_time': date_time,
        'text': text,
        'analyzed_text': analyzed_text
    })

    res = rq.post(es_server_address+path_params, headers=headers, params=params, data=data).json()

    return res

#print(write(1, 1, '2020-02-28T20:00:00.000Z', 'какого лешего'))
#print(write(1, 1, '2020-02-28T20:00:00.000Z', 'мой режим так сбит'))
#print(write(1, 1, '2020-02-28T20:00:00.000Z', 'слава украине'))
#print(write(1, 1, '2020-02-28T20:00:00.000Z', 'почему эти уроды не сделали нормальный анализатор'))


def full_text_search(work_place=1, role=1, date_time_start='2020-02-01', date_time_end='2020-02-28', query='', top=5):

    path_params = f'{index}/_search/'

    # для дебага ставь pretty="true", убирай .json() с res = ....json() и возвращай res.text
    params = {
        "pretty": "false",
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

    # the next request returns something like that:
    '''    {
            "took": 1,
            "timed_out": false,
            "_shards": {
                "total": 1,
                "successful": 1,
                "skipped": 0,
                "failed": 0
            },
            "hits": {
                "total": {
                    "value": 3,
                    "relation": "eq"
                },
                "max_score": 1.4995451,
                "hits": [
                    {
                        "_index": "testindex1",
                        "_type": "_doc",
                        "_id": "lryjDXEBgHmjTYGD3Xdy",
                        "_score": 1.4995451,
                        "_source": {
                            "work_place": 1,
                            "role": 1,
                            "date_time": "2020-02-28T20:00:00.000Z",
                            "text": "какого лешего"
                        }
                    },
                ]
            }
        }'''

    res = rq.post(es_server_address+path_params, headers=headers, params=params, data=data).json()
    # TODO сделать фильтрацию
    # clear response from unused data
    if res != {}:
        results = []
        for i in res['hits']['hits']:
            result = i['_source']
            result['id'] = i['_id']
            results.append(result)
    return results


#print(full_text_search(work_place=1, role=1, query='урод'))


def return_by_id(id):

    return es.search(index=index, body={'query': {'match': {'_id': id}}})

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