import sys
import os
from services.text_service.speech_recognition.kaldi import kaldi_recognition
#from services.text_service.postgreSQL_write import write_row
from services.fts_service.elasticsearch_full_text_search import write
from datetime import datetime


# DATA_IN_DIR = r'/home/user/Desktop/projects/Egg-Shaped_Apostle/data/'

DATA_IN_DIR = r'/media/sde/Data/'  # путь, откуда берутся файлы
SCRIPT_DIR = '/home/sde/Desktop/projects/Egg-Shaped_Apostle/services/text_service/'


def get_recognized_files():
    if 'recognized.txt' in os.listdir(SCRIPT_DIR):  # проверяем, есть ли список уже сконвертированных файлов
        with open(SCRIPT_DIR+'recognized.txt', 'r') as recognized:
            recognized_files = recognized.read().split('\n')  # читаем, если есть
        recognized.close()
    else:
        with open(SCRIPT_DIR + 'recognized.txt', 'w') as recognized:
            recognized.close()
        recognized_files = []
    return recognized_files


def write_to_log(record):
    with open('log.txt', 'w') as log_file:
        log_file.write(record)


def get_wav_files(DIR):
    return [i for i in os.listdir(DIR) if i.endswith('.wav')]


def add_to_database():
    # список файлов на распознввание
    files = [i for i in get_wav_files(DATA_IN_DIR) if i not in get_recognized_files()]

    mic_map = {
        # карта микрофонов.
        # Первый уровень — номер распберри,
        # второй — номер аудиокарты (он же номер микрофона, так как подключаем через usb-микро, там 1 к 1)
        # по номеру микрофона принимаем список, в котором 1-ый элемент — номер стола, 2-ой — роль (0 - оператор, 1 - клиент)
        0: {
            0: [1, 1],}}
    with open(SCRIPT_DIR+'recognized.txt', 'a+') as recognized:
        for file in files:
            print(file)
            endpoint, card, device, date = file[:-4].split('_')  # разбиваем название файла по "_", получаем метаданные расположения
            endpoint_data = mic_map[int(endpoint)]
            card_data = endpoint_data[int(card)]
            place = card_data[0]
            role = card_data[1]
            date = date[:-5]
            text = kaldi_recognition.recognize(DATA_IN_DIR, file)['raw_text']
            print(text)
            write(work_place = place, role = role, date_time = date, text = text)
            recognized.write(file+'\n')
            write_to_log(f'{place}, {role}, {date}, {text}')
        recognized.close()
    return True
