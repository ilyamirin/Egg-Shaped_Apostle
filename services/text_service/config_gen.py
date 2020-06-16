# creates config.ini and sets default settings if not exists
import sys
import os
import configparser

pathname = os.path.dirname(sys.argv[0])
path = os.path.abspath(pathname)


def get_config():
    config = configparser.ConfigParser()
    if 'config.ini' in os.listdir('.'):
        config.read('config.ini')
    else:
        config['ENV'] = {
            'ROOT_ABS_PATH': path,
            'DATA_DIR': os.path.join(path, 'data')}
        config['NETWORK'] = {
            'WEB_API_IP': '127.0.0.1',
            'WEB_API_PORT': '5726',
            'AUDIO_SERVICE_IP': '127.0.0.1',
            'AUDIO_SERVICE_PORT': '5722',
            'STORAGE_SERVICE_IP': '127.0.0.1',
            'STORAGE_SERVICE_PORT': '5730',
        }
        config['SETTINGS'] = {
            'DEBUG': 1,
            'RECOGNIZER': 'yandex'
        }
        with open('config.ini', 'w') as config_file:
            config.write(config_file)
    return config


get_config()
