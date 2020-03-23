import os
from datetime import datetime
import configparser
import subprocess

config = configparser.ConfigParser()
print('Reading configuration file...', end='\n')

if not 'config.ini' in os.listdir('.'):
    print('Unable to find config file, create one with default settings...')
    config['ENV'] = {
        'ROOT_ABS_PATH': os.getcwd(),
        'EXT_DATA_DIR': '/media/sde/Data/'
    }

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

config.read('config.ini')
print('OK')

def ui():

    print('Чтобы показать список устройств, введите "devices";\n'
          'Чтобы прослушать устройство, введите "listen n m", где'
          '"n" — индекс аудиокарты,'
          '"m" — индекс устройства ввода,\n'
          #'"t" — время прослушивания в секундах;\n'
          
          'Чтобы записать аудио с устройства, введите "record c, n, t", где'
          '"c" — индекс аудиокарты,'
          '"n" — индекс устройства,'
          '"t" — время записи,'
          #'"name" — имя файла без расширения. По умолчанию "unnamed";\n'
          'Чтобы выйти, введите "exit".\n')

    inp = input().split()

    if len(inp) < 1:
        ui()
    else:
        command, *attrib = inp
        if command == 'devices': print_devices()
        elif command == 'listen': listen(attrib[0], attrib[1])
        elif command == 'record': record_by_time(attrib[0], attrib[1], attrib[2])
        elif command == 'exit': return True
        else: print('Команда не распознана')
    return ui()


def print_devices():
    subprocess.call([r'/usr/bin/arecord', '-l'])


def listen(mic_card, mic_dev):
    print(r'* start listening. Press "enter" to stop')
    listening = subprocess.Popen(['/usr/bin/alsaloop', '-C', f'hw:{mic_card},{mic_dev}'])
    input()
    listening.terminate()
    return True


def record_by_time(card=0, mic=0, time=10):
    file_name = f'{config["ENV"]["EXT_DATA_DIR"]}0_0_0_{str(datetime.now()).replace(" ", "T")}.wav'
    print(f'* start recording. Please, say something in {time} seconds...')
    subprocess.call(
        [r'/usr/bin/arecord', '-f', 'cd', '-D' f'plughw:{card},{mic}', '-c', '1', '-d', f'{time}',
         file_name])
    print("* done recording")
    print(f'Saved to file {file_name}')


if __name__ == '__main__':
    ui()