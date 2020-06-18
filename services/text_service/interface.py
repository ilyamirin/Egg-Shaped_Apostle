import requests
import json

from config_gen import get_config
config = get_config()


audio_service_api = f'http://{config["NETWORK"]["AUDIO_SERVICE_IP"]}:{config["NETWORK"]["AUDIO_SERVICE_PORT"]}'
storage_service_api = f'http://{config["NETWORK"]["STORAGE_SERVICE_IP"]}:{config["NETWORK"]["STORAGE_SERVICE_PORT"]}'
stt_api = f'http://{config["NETWORK"]["STT_DEEPSPEECH_IP"]}:{config["NETWORK"]["STT_DEEPSPEECH_PORT"]}'


# audio_service API
def get_list_of_records():
    return requests.get(audio_service_api+'/records').json()


def get_raspberries():
    r = requests.get(audio_service_api + '/raspberry')
    return r.json()


def download_record(filename):
    r = requests.get(audio_service_api+'/records/send', data={'filename': filename})
    return r.content


# storage_service API
# принимает work_place, role, date_time, text
def record_create(work_place, role, datetime, text):
    headers = {
        'Content-Type': 'application/json'
    }
    data = json.dumps({
        'work_place': work_place,
        'role': role,
        'date_time': datetime,
        'text': text
    })
    r = requests.post(storage_service_api+'/record/create',
                      data=data,
                      headers=headers)
    return r.content


def stt_deepspeech(file):
    files = {
        'audio': ('audio', file, 'multipart/form-data')
    }
    r = requests.post(stt_api+'/transcribe', files=files)
    return r.json()