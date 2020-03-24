from datetime import datetime
from elasticsearch import Elasticsearch
import json
import requests as rq
es = Elasticsearch()

index = 'testindex1'
server_ip = 'localhost'
server_port = 9200
server_address = f'{server_ip}:{server_port}'

def write(work_place, role, date_time, text):
    doc = {
        'work_place': work_place,
        'role': role,
        'date_time': date_time,
        'text': text,
    }

    res = es.index(index=index, body=doc)

    return res['result']

#print(write(1, 1, '2020-02-28T20:00:00.000Z', 'какого лешего'))
#print(write(1, 1, '2020-02-28T20:00:00.000Z', 'мой режим так сбит'))
#print(write(1, 1, '2020-02-28T20:00:00.000Z', 'слава украине'))
#print(write(1, 1, '2020-02-28T20:00:00.000Z', 'почему эти уроды не сделали нормальный анализатор'))


def full_text_search(query, work_place=None, role=None, date_time_start=None, date_time_end=None, top=5):

    pre_result =  es.search(index=index, body={'query': {'match': {'text': query}},
                                               'filter': [{'role': role}, {'work_place': work_place}]})

    return pre_result

print(full_text_search('какого', work_place=1, role=1))


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