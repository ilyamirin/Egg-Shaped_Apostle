from datetime import datetime
import configparser
import subprocess
from audio_service import get_raspberries

config = configparser.ConfigParser()
print('Reading configuration file...', end='\n')
config.read('config.ini')
print('OK')

raspberries = get_raspberries()


def ui():

    print('Чтобы показать список устройств, введите "devices";\n'
          'Чтобы прослушать устройство, введите "listen l n m", где'
          '"l" — индекс raspberry,'
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


def listen(rasp, card, mic):
    print(r'* start listening. Press "enter" to stop')
    stream = raspberries[rasp].nodes[card].nodes[mic].stream()
    listening = subprocess.Popen(['aplay'], stdin=subprocess.PIPE)
    for i in stream.iter_content(raw=True):
        listening.stdin.write(i)
    return True


def record_by_time(card=0, mic=0, time=10):
    file_name = f'{config["ENV"]["EXT_DATA_DIR"]}0_0_0_{str(datetime.now()).replace(" ", "T")}.wav'
    print(f'* start recording. Please, say something in {time} seconds...')
    subprocess.call(
        [r'/usr/bin/arecord', '-f', 'cd', '-D' f'plughw:{card},{mic}', '-c', '1', '-d', f'{time}',
         file_name])
    print("* done recording")
    print(f'Saved to file {file_name}')


# if __name__ == '__main__':
#     ui()
listen(0, 0, 0)