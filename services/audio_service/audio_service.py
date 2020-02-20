import os
import sys
import configparser
os.chdir(os.getcwd()+'/audio/')
sys.path.append(os.getcwd())
from datetime import datetime

config = configparser.ConfigParser()
config.read_file(open('config.ini'))

import devices_wrapper
import management

DATA_DIR = '..\\..\\..\\data\\'
input_device_index = 1
if str(input_device_index) in config['prefixes_of_microphones'].keys():
    name = config['prefixes_of_microphones'][str(input_device_index)]
else:
    name = str(input_device_index)
name = name + '_' + str(datetime.now()).replace(':', '. ')
management.stop_by_key(output_path=DATA_DIR, name=name)