import sys
import os
from speech_recognition.kaldi import converter, kaldi_recognition
from postgreSQL_write import write_row
from datetime import datetime

#DATA_IN_DIR = r'/home/user/Desktop/projects/Egg-Shaped_Apostle/data/'
DATA_IN_DIR = r'/media/user/data/' #путь, откуда берутся файлы

if 'converted' in os.listdir(os.getcwd()): # проверяем, есть ли список уже сконвертированных файлов
    with open('converted', 'r') as converted:
        converted_files = converted.read().split('\n') # читаем, если есть
else:
    open('converted', 'w').close() # иначе создаем
    converted_files = []
recognizer = kaldi_recognition.Recognizer()

# список файлов на конвертацию,
# с фильтрацией по уже отконвертированным
files = [i for i in converter.get_files() if i not in converted_files]

for i in files:
    converter.split_and_convert(i, 60)
    print(i)

#добавляем отконвретированное в список
with open('converted', 'w') as converted:
    for i in files:
        converted.write(i+'\n')

print(files)
print('files converted...')

#аналогично с конверитрованными, делаем список распознанных
if 'recognized' in os.listdir(os.getcwd()):
    with open('recognized', 'r') as recognized:
        recognized_files = recognized.read().split()
else:
    open('recognized', 'w').close()
    recognized_files = []


files_to_stt = [i for i in recognizer.get_data_listdir() if i not in recognized_files]

mic_map = {
    # карта микрофонов.
    # Первый уровень — номер распберри,
    # второй — номер аудиокарты (он же номер микрофона, так как подключаем через usb-микро, там 1 к 1)
    # по номеру микрофона принимаем список, в котором 1-ый элемент — номер стола, 2-ой — роль (0 - оператор, 1 - клиент)
    0: {
        0: [1, 1],
        1: [2, 0],
        2: [1, 0]},
    1: {
        0: [3, 0],
        1: [3, 1],
        2: [4, 0],
        3: [4, 1]
           }
}


print('recognizing and adding to DB...')
for file in files_to_stt: # бежим по списку файлов на распознавание
    log = ''
    endpoint, card, device, date = file.split('_') #разбиваем название файла по "_", получаем метаданные расположения
    endpoint_data = mic_map[int(endpoint)]
    card_data = endpoint_data[card]
    place = card_data[0]
    role = card_data[1]
    date = date[:-5]
    try: # пытаемся отдать на распознавание
        text = recognizer.recognize(file)['raw_text']
        print(text)
        write_row(place, role, date, text)
        log = log + f'{place}, {role}, {date}, {text}'
    except:
        e = sys.exc_info()[0]
        err_text = str(e)+f' on file {file}.\n'
        print(err_text)
        log = log + err_text

with open('recognized', 'w') as recognized:
    for i in files_to_stt:
        recognized.write(i)

with open('log.txt', 'w') as log_file:
    log_file.write(log)

print('Done.')


'''existing_files = set([i[:-2] for i in recognizer.get_data_listdir()])
unconverted_files = list(files - existing_files)
print(len(unconverted_files))'''

'''for i in unconverted_files[:100]:
    converter.convert(i)

print('files converted...')

files_to_stt = recognizer.get_data_listdir()

print('recognizing and adding to DB...')
for file in files_to_stt[:50]:
    log = ''
    role = file[-1]
    try:
        text = recognizer.recognize(file)['raw_text']
        write_row(1, role, text)
    except err as err:
        e = sys.exc_info()[0]
        err_text = str(e)+f' on file {file}.\n'
        print(err_text)
        log = log + err_text

with open('log.txt', 'w') as log_file:
    log_file.write(log)

print('Done.')'''