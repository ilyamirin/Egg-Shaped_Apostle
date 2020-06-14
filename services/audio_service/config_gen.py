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
            'EXT_DATA_DIR': '/home/sde'
        }
        with open('config.ini', 'w') as config_file:
            config.write(config_file)
    return config


get_config()