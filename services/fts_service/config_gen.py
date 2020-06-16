# creates config.ini and sets default settings if not exists
import sys, os
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
            'EXT_DATA_DIR': os.path.join(path, 'data')
        }
        config['NETWORK'] = {
            'WEB_API_IP': '127.0.0.1',
            'WEB_API_PORT': 5727,
            'ES_IP': '127.0.0.1',
            'ES_PORT': 9200,

        }
        config['SETTINGS'] = {
            'ES_INDEX': 'testindex1',
        }
        with open('config.ini', 'w') as config_file:
            config.write(config_file)
    return config


get_config()