import sys
import os
from speech_recognition.kaldi import converter, kaldi_recognition
from postgreSQL_write import write_row
from datetime import datetime

DATA_IN_DIR = r'/home/user/Desktop/projects/Egg-Shaped_Apostle/data/'

if 'converted' in os.listdir(os.getcwd()):
    with open('converted', 'r') as converted:
        converted_files = converted.read().split()
else:
    open('converted', 'w').close()
    converted_files = []
recognizer = kaldi_recognition.Recognizer()

files = [i for i in converter.get_files() if i not in converted_files]

for i in files[:10]:
    converter.convert(i)

with open('converted', 'w') as converted:
    for i in files:
        converted.write(i)

print(files)
print('files converted...')

if 'recognized' in os.listdir(os.getcwd()):
    with open('recognized', 'r') as recognized:
        recognized_files = recognized.read().split()
else:
    open('recognized', 'w').close()
    recognized_files = []


files_to_stt = [i for i in recognizer.get_data_listdir() if i not in recognized_files]


print('recognizing and adding to DB...')
for file in files_to_stt:
    log = ''
    role = file[-1]
    try:
        text = recognizer.recognize(file)['raw_text']
        print(text)
        write_row(1, role, datetime.now(), text)
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