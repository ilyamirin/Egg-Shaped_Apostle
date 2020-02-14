import sys

from speech_recognition.kaldi import converter, kaldi_recognition
from speech_recognition import postgreSQL_write

DATA_IN_DIR = r'/home/user/Desktop/projects/Egg-Shaped_Apostle/data/'

recognizer = kaldi_recognition.Recognizer()

files = converter.get_files()
print(files)

for i in files[:10]:
    converter.convert(i)

'''existing_files = set([i[:-2] for i in recognizer.get_data_listdir()])
unconverted_files = list(files - existing_files)
print(len(unconverted_files))

for i in files[:1000]:
    converter.convert(i)

print('files converted...')

files_to_stt = recognizer.get_data_listdir()

print('recognizing and adding to DB...')
for file in files_to_stt[:50]:
    log = ''
    role = file[-1]
    try:
        text = recognizer.recognize(file)['raw_text']
        postgreSQL_write.write_row(1, role, text)
    except err as err:
        e = sys.exc_info()[0]
        err_text = str(e)+f' on file {file}.\n'
        print(err_text)
        log = log + err_text

with open('log.txt', 'w') as log_file:
    log_file.write(log)

print('Done.')'''