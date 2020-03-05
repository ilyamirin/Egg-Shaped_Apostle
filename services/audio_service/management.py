import socket
import pyaudio
import os
import keyboard
from datetime import datetime
import configparser
import paramiko

from devices_wrapper import Microphone, AudioFile, Speaker
import config

config = configparser.ConfigParser()
print('Reading configuration file...', end='')
config.read('config.ini')
print('OK')
data_chunk = 1024
SERVICE_DATA_PATH = config['ENV']['SERVICE_DATA_PATH']

def ui():
    print('Чтобы показать список устройств, введите "devices";\n'
          'Чтобы прослушать устройство, введите "listen n s t", где "n" — индекс устройства ввода,'
          '"s" — индекс устройства вывода,'
          '"t" — время прослушивания в секундах;\n'
          'Чтобы записать аудио с устройства, введите "record n name", где "n" — индекс устройства,'
          '"name" — имя файла без расширения. По умолчанию "unnamed";\n'
          'Чтобы задать определенным индексам префиксы для записи, введите "bind";\n'
          'Чтобы запустить сервер потоковой передачи аудио, введите "stream n", где "n" — индекс устройства ввода;\n'
          'Чтобы выйти, введите "exit".\n')
    inp = input().split()
    if len(inp) < 1:
        ui()
    else:
        command, *attrib = inp
        if command == 'devices':
            print('Доступны следующие устройства ввода/вывода аудио:')
            print_devices()

        elif command == 'listen':
            sp = Speaker(output_device_ind=int(attrib[1]))
            sp.start_stream_from_mic(inp_device_ind=int(attrib[0]), listen_time=int(attrib[2]))

        elif command == 'record':
            if 'prefixes_of_microphones' in config.keys() and attrib[0] in config['prefixes_of_microphones'].keys():
                name = config['prefixes_of_microphones'][attrib[0]]+'_'+attrib[1]
            else: name = attrib[1]
            record_stop_by_key('space', inp_device_ind=int(attrib[0]), output_path=SERVICE_DATA_PATH, name=name)

        elif command == 'bind':
            print('введите префикс в формате "n prefix", где n — индекс,'
                  ' prefix — префикс для записи с определенного индекса')
            index, prefix = input().split()
            bind(index, prefix)

        elif command == 'stream':
            stream_audio_trough_socket(inp_device_ind=int(attrib[0]))

        elif command == 'exit':
            return True
        else:
            print('Команда не распознана')
    return ui()


def record_stop_by_key(key='space', mic_settings={}, **kwargs):
    file = AudioFile(**kwargs)
    print(f'* start recording. Press {key} to stop...')
    file.start_record_from_mic(**mic_settings)
    while True:
        data = file.mic.stream.read(file.chunk)
        file.frames.append(data)
        if keyboard.is_pressed(key):
            print('Recording stopped...')
            data = file.mic.stream.read(file.chunk)
            # data = file.mic.stream.read()
            file.frames.append(data)
            break
    print("* done recording")
    file.mic.close_stream()
    file.save_file()
    print(f'Saved to file {file.name}.wav')


def bind(index, prefix):
    if not 'prefixes_of_microphones' in config.keys():
        config['prefixes_of_microphones'] = {}
    config['prefixes_of_microphones'][index] = prefix
    config.write(open('config.ini', 'w'))


def stream_audio_trough_socket(key='space', inp_device_ind=None):

    print('Reading server network configuration...', end='')
    s_ip = config['NETWORK']['SERVER_IP']
    s_port = int(config['NETWORK']['SERVER_PORT'])
    s_addr = (s_ip, s_port)
    print('OK')

    print('Creating socket...')
    s = socket.socket()
    s.bind(s_addr)
    print(f'Socket successfully created at {s_ip}:{s_port}.')
    print('listening incoming connections...')
    s.listen(1)
    mic = Microphone(inp_device_ind=inp_device_ind)
    mic.open_stream()
    conn, addr = s.accept()
    print(f'Incoming connection from {addr[0]}:{addr[1]}. Press {key} to stop listening...')
    while True:
        if keyboard.is_pressed(key): break
        data = mic.stream.read(data_chunk)
        try:
            conn.send(data)
        except:
            conn.close()
            s.close()
            stream_audio_trough_socket()
    conn.close()
    s.close()

def print_devices():
    p = pyaudio.PyAudio()
    host_api_info = p.get_default_host_api_info()
    for id in range(host_api_info['deviceCount']):
        device_info = p.get_device_info_by_host_api_device_index(host_api_info['index'], id)
        fields = ['index', 'name', 'maxInputChannels', 'maxOutputChannels', 'defaultSampleRate']
        for field in fields:
            print(f"{field}: {device_info[field]};")
        print('\n')


if __name__ == '__main__':
    ui()