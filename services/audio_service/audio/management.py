# coding=utf-8
import configparser
import keyboard
import sounddevice as sd
from datetime import datetime

config = configparser.ConfigParser()

def ui():
    print('Чтобы показать список устройств, введите "devices"\n'
          'Чтобы прослушать устройство, введите "listen n c t", где "n" — индекс устройства,'
          '"c" — количество каналов, "t" — время прослушивания в секундах\n'
          'Чтобы записать аудио с устройства, введите "record n name", где "n" — индекс устройства,'
          '"name" — имя файла без расширения. По умолчанию "unnamed"\n'
          'Чтобы задать определенным индексам префиксы для записи, введите "bind"\n'
          'Чтобы выйти, введите "exit"\n')
    inp = input().split()
    if len(inp) < 1:
        ui()
    else:
        command, *attrib = inp
        if command == 'devices':
            print('Доступны следующие устройства ввода/вывода аудио:')
            print(sd.query_devices())
        elif command == 'listen':
            sp = Speaker()
            sp.start_stream_from_mic(inp_device_ind=int(attrib[0]), channels=int(attrib[1]), listen_time=int(attrib[2]))
        elif command == 'record':
            if attrib[0] in config['prefixes_of_microphones'].keys():
                name = config['prefixes_of_microphones'][attrib[0]]+'_'+attrib[1]
            else: name = attrib[1]
            stop_by_key('space', inp_device_ind=int(attrib[0]), name=name)
        elif command == 'bind':
            print('введите префикс в формате "n prefix", где n — индекс,'
                  ' prefix — префикс для записи с определенного индекса')
            index, prefix = input().split()
            if not 'prefixes_of_microphones' in config.keys():
                config['prefixes_of_microphones'] = {}
            config['prefixes_of_microphones'][index] = prefix
            config.write(open('config.ini', 'w'))
        elif command == 'exit':
            return True
        else:
            print('Команда не распознана')
    return ui()

# print(get_all_host_api_devices())
# stop_by_key - остановка записи по нажатию клавиши. key - клавиша, WAVE_OUTPUT_FILENAME - название файла


def stop_by_key(key='space', mic_settings={}, **kwargs):
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


def stop_by_time(key='space', **kwargs):
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

if __name__ == '__main__':
    from devices_wrapper import Microphone, AudioFile, Speaker
    config.read_file(open('config.ini'))
    #ui()
else:
    from audio.devices_wrapper import Microphone, AudioFile, Speaker
    config.read_file(open('./audio/config.ini'))


stop_by_key(name='mic1', mic_settings={'inp_device_ind': 1, 'channels': 2, 'rate': 48000})