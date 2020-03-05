import socket
import os
import keyboard
import sounddevice as sd
from datetime import datetime
import configparser
import paramiko

from devices_wrapper import Microphone, AudioFile, Speaker
import config

config = configparser.ConfigParser()
print('Reading configuration file...', end='')

config.read('config.ini')
print('OK')

FILE_SERVER_IP = config['NETWORK']['file_server_ip']
FILE_SERVER_PORT = config['NETWORK']['file_server_port']
SERVICE_USERNAME = config['AUTHENTIFICATION']['service_username']

SERVICE_DATA_PATH = config['ENV']['SERVICE_DATA_PATH']

def record_stop_by_time(**kwargs):
    file = AudioFile(**kwargs)
    print('start recording')
    file.start_record_from_mic(**kwargs)
    while True:
        now = datetime.now()
        data = file.mic.stream.read(file.chunk)
        file.frames.append(data)
        if now.hour == 18 and now.minute == 0:
            print('Working day is over!')
            data = file.mic.stream.read(file.chunk)
            file.frames.append(data)
            break
    print("* done recording")
    file.mic.close_stream()
    file.save_file()
    print(f'Saved to file {file.name}.wav')


def send_file(input_file, output_file):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(FILE_SERVER_IP, port=FILE_SERVER_PORT, username=SERVICE_USERNAME, key_filename='id_rsa')
    sftp = ssh.open_sftp()
    sftp.put(input_file, output_file)


#send_file('test.txt', 'test1.txt')