import json
import subprocess
import threading
from requests.exceptions import ConnectionError

from raspberry_api import Raspberry
from network_utils import get_active_addresses
from config_gen import get_config
from audio_logger import get_logger
config = get_config()
logger = get_logger('mic_mapper', config['SETTINGS']['DEBUG'])


def get_raspberries_by_scanning():
    _raspberries_ = []
    ips = get_active_addresses()
    for ip in ips:
        try:
            _raspberries_.append(Raspberry(ip))
        except ConnectionError:
            logger.debug(f'no service on {ip}, skipping...')
        except Exception as e:
            logger.error(e)
    return _raspberries_


def read_rasp_map() -> dict:
    rasp_map = {}
    try:
        with open('raspberries.json', 'r') as rasp_map_file:
            rasp_map = json.load(rasp_map_file)
    except json.decoder.JSONDecodeError:
        logger.debug('there is no raspberries declared')
    except FileNotFoundError:
        logger.debug('no raspberries.json in directory')
    except Exception as e:
        logger.error(e)
    return rasp_map


def add_raspberry_to_file(raspberry: Raspberry):
    rasp_map = read_rasp_map()
    if raspberry.ip not in rasp_map.keys():
        rasp_map[raspberry.ip] = {
            'no': raspberry.no,
            'cards': {}
        }
        for card in raspberry.nodes:
            rasp_map[raspberry.ip]['cards'][card.no] = {}
            for mic in card.nodes:
                rasp_map[raspberry.ip]['cards'][card.no][mic.no] = {
                    'work_place': None,
                    'role': None
                }
    with open('raspberries.json', 'w+') as rasp_map_file:
        json.dump(rasp_map, rasp_map_file)


raspberries = get_raspberries_by_scanning()
raspberries_dict = {rasp.no: rasp for rasp in raspberries}


for i in raspberries:
    add_raspberry_to_file(i)

listen_flag = False


def wait_for_key():
    global listen_flag
    input()
    listen_flag = False


# TODO СДЕЛАЙ DICT ВМЕСТО LIST В Raspberry.nodes etc.
def listen(rasp_no: int, card_no: int, mic_no: int):
    global listen_flag
    listen_flag = True
    print(r'* start listening. Press any key to stop')
    stream = raspberries_dict[rasp_no].cards[card_no].mics[mic_no].stream()
    listening = subprocess.Popen(['aplay'], stdin=subprocess.PIPE)
    a = threading.Thread(target=wait_for_key)
    a.start()
    for i in stream.iter_content():
        if not listen_flag:
            break
        listening.stdin.write(i)
    return True


def check_unfilled_fields():
    unfilled = []
    rasp_map = read_rasp_map()
    for rasp in rasp_map:
        cards = rasp_map[rasp]['cards']
        for card in cards:
            mics = cards[card]
            for mic in mics:
                if not mics[mic]['work_place'] or not mics[mic]['role']:
                    unfilled.append([rasp, card, mic])
    return unfilled


def print_devices():
    rasp_map = read_rasp_map()
    print('В raspberries.json определены следуюшие устройства:')
    for rasp in rasp_map:
        print(f'Raspberry Pi с ip-адресом {rasp} и номером {rasp_map[rasp]["no"]} имеет следующие карты:')
        cards = rasp_map[rasp]['cards']
        for card in cards:
            print(f'\tКарта с индексом {card} имеет следующие микрофоны:')
            mics = cards[card]
            for mic in mics:
                place = f"указано рабочее место {mics[mic]['work_place']}"\
                    if mics[mic]['work_place'] else 'не указано рабочее место'
                role = f"указана роль {mics[mic]['role']}" if mics[mic]['role'] else 'не указана роль'
                print(f'\t\tdeДля микрофона с индексом {mic} {place}, {role}.')


def define_mic(rasp_no, card, mic, work_place, role):
    rasp_map = read_rasp_map()
    for rasp in rasp_map:
        if rasp_map[rasp]['no'] == rasp_no:
            mic = rasp_map[rasp]['cards'][card][mic]
            mic['work_place'] = work_place
            mic['role'] = role
            with open('raspberries.json', 'w+') as rasp_map_file:
                json.dump(rasp_map, rasp_map_file)
            print('Значения заданы')


def ui():
    print('\n'
          '\n'
          '\n'
          'Чтобы показать список устройств, введите "devices";\n'
          '\n'
          'Чтобы прослушать устройство, введите "listen l n m", где '
          '"l" — индекс raspberry,\n'
          '"n" — индекс аудиокарты,\n'
          '"m" — индекс устройства ввода.\n'
          '\n'
          'Чтобы задать рабочее место и роль микрофону, введите "define l n m place, role", где'
          '"l" — индекс raspberry,\n'
          '"n" — индекс аудиокарты,\n'
          '"m" — индекс устройства ввода,\n'
          'place — число, обозначающее рабочее место,\n'
          'role — число, обозначающее роль говорящего (0 — оператор, 1 — клиент)\n'
          )

    inp = input().split()
          #'"t" — время прослушивания в секундах;\n'

    if len(inp) < 1:
        ui()
    else:
        try:
            command, *attrib = inp
            if command == 'devices': print_devices()
            elif command == 'listen': listen(attrib[0], attrib[1], attrib[2])
            elif command == 'define': define_mic(attrib[0],
                                                 attrib[1],
                                                 attrib[2],
                                                 attrib[3],
                                                 attrib[4],)
            elif command == 'exit': return True
            else: print('Команда не распознана')
        except Exception as e:
            print('ошибка:', str(e))
    return ui()


if __name__ == "__main__":
    ui()