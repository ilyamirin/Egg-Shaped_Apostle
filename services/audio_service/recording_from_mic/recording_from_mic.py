import keyboard
import pyaudio
import wave
import datetime

Recording_CHUNK = 1024
Recording_FORMAT = pyaudio.paInt16
Recording_CHANNELS = 1
Recording_RATE = 48000


class Recording():
    def __init__(self, inp_device_ind):
        self.inp_dev_ind = inp_device_ind

    # open_stream - задает формат для записи (из глабальных переменных) и создает пустой фрейм, в который будет добавляться запись

    def open_stream(self, ):

        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(format=Recording_FORMAT,
                                  rate=Recording_RATE,
                                  input_device_index = self.inp_dev_ind,
                                  channels=Recording_CHANNELS,
                                  input=True,
                                  frames_per_buffer=Recording_CHUNK)

        print("* recording")
        self.frames = []

        return (True)

    # close_stream - для закрытия записи

    def close_stream(self):

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    # save_file - сохранение файла в wav с необходимыми свойствами (из глобальных переменных)

    def save_file(self, WAVE_OUTPUT_FILENAME):

        wf = wave.open(WAVE_OUTPUT_FILENAME + ".wav", 'wb')
        wf.setnchannels(Recording_CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(Recording_FORMAT))
        wf.setframerate(Recording_RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    # cut_frames

    def cut_frames(self, WAVE_OUTPUT_FILENAME):
        self.save_file(WAVE_OUTPUT_FILENAME)
        self.frames = []

    # stop_by_worktime - остановка записи во время окончания рабочего дня. Предполагается что 1 микрофон записывает 1Гб аудио
    # в необходимом формате за 17 часов, соответсвенно их не нужно будет резать и критерием остановки служит конец рабочего дня
    def stop_by_worktime(self, WAVE_OUTPUT_FILENAME):

        self.open_stream()
        while True:
            now = datetime.datetime.now()

            try:
                if now.hour == 18 and now.minute == 0:
                    print('Working day is over!')
                    break
                data = self.stream.read(Recording_CHUNK)
                self.frames.append(data)
            except:
                break

    # stop_by_key - остановка записи по нажатию клавиши. key - клавиша, WAVE_OUTPUT_FILENAME - название файла

    def stop_by_key(self, key, WAVE_OUTPUT_FILENAME):

        self.open_stream()

        while True:
            try:
                if keyboard.is_pressed(key):
                    print('You Pressed A Key!')
                    break
                data = self.stream.read(Recording_CHUNK)
                self.frames.append(data)
            except:
                break

        print("* done recording")
        self.close_stream()
        self.save_file(WAVE_OUTPUT_FILENAME)


