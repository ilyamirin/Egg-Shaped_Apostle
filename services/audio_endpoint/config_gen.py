# creates config.ini and sets default settings if not exists
import sys, os
import configparser
import argparse

pathname = os.path.dirname(sys.argv[0])
path = os.path.abspath(pathname)

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--device', default='0')
parser.add_argument('-a', '--ip', default='127.0.0.1')
parser.add_argument('-f', '--port', default='22')
parser.add_argument('-u', '--username', default='sde')
parser.add_argument('-d', '--debug', default='1')
parser.add_argument('-s', '--dir', default='/home/sde/')
parser.add_argument('-t', '--rec_dur', default='1')
parser.add_argument('-r', '--rec_sr', default='16000')
parser.add_argument('-m', '--start_time', default='00:00')
parser.add_argument('-e', '--endtime', default='23:59')

namespace = parser.parse_args(sys.argv[1:])


def get_config():
    config = configparser.ConfigParser()
    if 'config.ini' in os.listdir('.'):
        config.read('config.ini')
    else:
        config['ENV'] = {
            'HOME_DIR': path,
            'RSA_DIR': f'{path}/id_rsa',
            'DATA_DIR': f'{path}/data/',
            'DEV_NO': namespace.device,
        }

        config['FILE_SERVER'] = {
            'IP': namespace.ip,
            'PORT': namespace.port,
            'WEB_API_IP': '127.0.0.1',
            'WEB_API_PORT': 5722,
            'USERNAME': namespace.username,
            'DIR': namespace.dir,
        }

        config['NETWORK'] = {
            'WEB_API_IP': '127.0.0.1',
            'WEB_API_PORT': 5721,
        }

        config['SETTINGS'] = {
            'DEBUG': namespace.debug,
            'RECORD_DUR': namespace.rec_dur,
            'RECORD_SAMPLING_RATE': namespace.rec_sr,
            'START_HOUR': namespace.start_time,
            'END_HOUR': namespace.endtime,
        }
        with open('config.ini', 'w') as config_file:
            config.write(config_file)
    return config


if __name__ == '__main__':
    config = get_config()