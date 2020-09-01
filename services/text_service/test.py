from interface import *
from pydub import AudioSegment
import requests
# from speech_recognition.yandex_speech_kit_recognition import yandex_speech_kit_realtime_recognition as recognizer
from speech_recognition.kaldi import kaldi_recognition as recognizer


def recognize(record):
    audio = download_record(record)
    if True:#config['SETTINGS']['RECOGNIZER'] == 'kaldi':
        with open('audio_recognize.wav', 'wb+') as file:
            file.write(audio)
            file.close()
            text = recognizer.recognize_audio(config['ENV']['ROOT_ABS_PATH'], '/audio_recognize.wav')
    else:  # config['SETTINGS']['RECOGNIZER'] == 'yandex':
        text = recognizer.recognize_audio(audio)['result']
    with open('recognized.txt', 'a+') as recognized_files:
        recognized_files.write(record + '\n')
    return text




print(recognize('test.wav'))
# audio = download_record('test.wav')
# with open('audio_recognize.wav', 'wb+') as file:
#     file.write(audio)
#     file.close()
# audio = AudioSegment.from_wav('audio_recognize.wav')
# audio = audio.set_frame_rate(16000)
# audio.export('audio_recognize_16k.wav', format='wav', bitrate=16)
# with open('audio_recognize_16k.wav', 'rb') as file:
#     print(stt_deepspeech(file.read()))