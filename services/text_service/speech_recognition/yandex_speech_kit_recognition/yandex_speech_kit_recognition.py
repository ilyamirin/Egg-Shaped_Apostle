import requests
import pandas as pd

from json import dumps
from time import sleep
from threading import Thread
from os import listdir, getcwd
from keyring import get_password


api_key = get_password('Yandex_API_key', 'MNIXenus') #u should add your API key by keyring.set_password()
auth = {"Authorization": "Api-Key " + api_key}


def send_file(name_of_file):

    resource = 'https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize'
    obj_link = 'https://storage.yandexcloud.net/audiocdo/'+name_of_file

    params = {
        "config": {
            "specification": {
                "languageCode": "ru-RU",
                "profanityFilter": "true",
                "audioEncoding": "LINEAR16_PCM",
                "sampleRateHertz": "48000",
                "audioChannelCount": "1"
            }
        },
        "audio": {
            "uri": obj_link
        }
    }

    payload = dumps(params)
    try:
        response = requests.post(resource, data=payload, headers = auth).json()
        print(response)
    except:
        response = None
        print('Something wrong with '+name_of_file)
    if type(response) == dict and 'id' in response.keys():
        return response
    else: return None

def check_done(op_id):
    resource_operations = 'https://operation.api.cloud.yandex.net/operations/'
    response = requests.get(resource_operations + op_id, headers=auth).json()
    return response

def make_excel(name_of_file, response):
    chunks = []
    channels = []
    for chunk in response['response']['chunks']:
        chunks.append(chunk['alternatives'][0]['text'])
        channels.append(chunk['channelTag'])
    output = pd.DataFrame({'text': chunks, "channel": channels})
    output.to_excel(name_of_file + '.xlsx')

def recognize(name_of_file):
    response = send_file(name_of_file)
    if response == None:
        print('Something wrong with '+name_of_file)
    else:
        op_id = response['id']
        while True:
            response_rec = check_done(op_id)
            if response_rec['done']:

                make_excel(name_of_file, response_rec)
                print('file '+name_of_file+' has been written')
                break
            sleep(10)

def recognize_all(names):
    threads = []
    for i in names:
        threads.append(Thread(target=recognize, args=(i,))) #Thread read str as enumerable
    for i in threads:
        i.run()