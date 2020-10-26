# creates config.ini and sets default settings if not exists
import sys, os
import configparser

pathname = os.path.dirname(sys.argv[0])
path = os.path.abspath(pathname)
root_dir = os.path.abspath(os.path.join(path, '..'))


def get_config():
    config = configparser.ConfigParser()
    if 'config.ini' in os.listdir(root_dir):
        config.read(os.path.join(root_dir, 'config.ini'))
    else:
        config['ENV'] = {
            'ROOT_ABS_PATH': root_dir,
            'EXT_DATA_DIR': os.path.join(root_dir, 'data')
        }
        config['NETWORK'] = {
            'WEB_API_IP': '127.0.0.1',
            'WEB_API_PORT': '5731',
            'STORAGE_SERVICE_IP': '127.0.0.1',
            'STORAGE_SERVICE_PORT': '5730',
            'AUDIO_SERVICE_IP': '127.0.0.1',
            'AUDIO_SERVICE_PORT': '5722',
            'DIARIZATION_SERVICE_IP': '127.0.0.1',
            'DIARIZATION_SERVICE_PORT': '5732',
        }
        config['SETTINGS'] = {
            'DEBUG': True,
        }
        with open(os.path.join(root_dir, 'config.ini'), 'w') as config_file:
            config.write(config_file)
    return config