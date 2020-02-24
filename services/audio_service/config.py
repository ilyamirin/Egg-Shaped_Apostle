import os
import configparser

config = configparser.ConfigParser()


def find_file(filename):
    for root, dirnames, filenames in os.walk('.'):
        if filename in filenames:
            return root
    return False


if not 'config.ini' in os.listdir('.'):
    config['NETWORK'] = {
        'SERVER_IP': '127.0.0.1',
        'SERVER_PORT': 12345,
    }
    config['ENV'] = {
        'ROOT_ABS_PATH': os.getcwd(),
        'SERVER_SCRIPT_PATH': find_file('server.py'),
    }

    with open('config.ini', 'w') as configfile:
        config.write(configfile)