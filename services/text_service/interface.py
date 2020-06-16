import requests

from config_gen import get_config
config = get_config()


audio_service_api = f'http://{config["NETWORK"]["AUDIO_SERVICE_IP"]}:{config["NETWORK"]["AUDIO_SERVICE_PORT"]}'


# audio_service API
def get_list_of_records():
    return requests.get(audio_service_api+'/records').json()


def get_raspberries():
    r = requests.get(audio_service_api + '/raspberry')
    return r.json()


def download_record(filename):
    r = requests.get(audio_service_api+'/records/send', data={'filename': filename})
    return r.content
