import requests
import json

from config_gen import get_config
config = get_config()


audio_service_api = f'http://{config["NETWORK"]["AUDIO_SERVICE_IP"]}:{config["NETWORK"]["AUDIO_SERVICE_PORT"]}'


def download_record(filename):
    r = requests.get(audio_service_api+'/records/send', data={'filename': filename})
    return r.content