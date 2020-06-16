#!/usr/bin/env python
# -*- coding: utf-8 -*-
# creates config.ini and sets default settings if not exists
__author__ = "Paul Maksimov"
__copyright__ = "Copyright 2020, The Egg-Shaped Apostle Project"
__version__ = "1.0.0"
__maintainer__ = "Paul Maksimov"
__email__ = "work.xenus@gmail.com"
__status__ = "Production"
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
            'EXT_DATA_DIR': os.path.join(path, 'data')
        }
        config['NETWORK'] = {
            'WEB_API_IP': '127.0.0.1',
            'WEB_API_PORT': 5730,
        }
        config['PG'] = {
            'SERVER_IP': '127.0.0.1',
            'SERVER_PORT': '5432',
            'DB_NAME': 'text',
            'TEXT_TABLE_NAME': 'text',
            'USER': 'text_service',
        }
        with open('config.ini', 'w') as config_file:
            config.write(config_file)
    return config
