import pyaudio
import wave
from time import time

#Recording_CHUNK = 1024
#Recording_FORMAT = pyaudio.paInt16
#Recording_CHANNELS = 2
#Recording_RATE = 44100
#Recording_FOLDER = r'C:/Users/User/Desktop/projects/Egg-Shaped_Apostle/data/'


class Audio_obj():
    def __init__(self, chunk=1024, format_=pyaudio.paInt16, channels=2, rate=48000):
        self.p = pyaudio.PyAudio()
        self.chunk = chunk
        self.format_ = format_
        self.channels = channels
        self.rate = rate

    def close_stream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        return True

class Microphone(Audio_obj):

    def __init__(self, inp_device_ind=None, chunk=1024, format_=pyaudio.paInt16, channels=2, rate=48000):
        super().__init__(chunk=chunk, format_=format_, channels=channels, rate=rate)
        self.inp_dev_ind = inp_device_ind


    # open_stream - задает формат для записи (из глабальных переменных) и создает пустой фрейм, в который будет добавляться запись
    def open_stream(self):

        self.stream = self.p.open(format=self.format_,
                                  rate=self.rate,
                                  input_device_index = self.inp_dev_ind,
                                  channels=self.channels,
                                  input=True,
                                  frames_per_buffer=self.chunk)
        return True

    # close_stream - для закрытия записи


    def get_device_info(self):
        return self.p.get_device_info_by_index(self.inp_device_ind)


class Speaker(Audio_obj):

    def __init__(self, output_device_ind=None, chunk=1024, format_=pyaudio.paInt16, channels=2, rate=48000):
        super().__init__(chunk=chunk, format_=format_, channels=channels, rate=rate)
        self.output_device_ind = output_device_ind

    def play_stream_from_mic(self, inp_device_ind=None, listen_time=10):
        self.mic = Microphone(inp_device_ind,
                              chunk=self.chunk,
                              format_=self.format_,
                              channels=self.channels,
                              rate=self.rate,
        )
        self.mic.open_stream()
        self.stream = self.p.open(format=self.format_,
                                  channels=self.channels,
                                  rate=self.rate,
                                  output=True)

        start_time = time()
        while time() - start_time <= listen_time:
            data = self.mic.stream.read(self.chunk)
            self.stream.write(data)

        self.stop_stream_from_mic()
        return True

    def stop_stream_from_mic(self):
        self.play_flag=False
        self.mic.close_stream()
        self.close_stream()
        return True


class Audio_file(Audio_obj):

    def __init__(self, output_path=None, name='unnamed', chunk=1024, format_=pyaudio.paInt16, channels=2, rate=48000):
        super().__init__(chunk=chunk, format_=format_, channels=channels, rate=rate)
        self.output_path = output_path
        self.name = name
        self.n_batch = 0

    def start_record_from_mic(self, inp_device_ind=None):
        self.mic = Microphone(inp_device_ind,
                              chunk=self.chunk,
                              format_=self.format_,
                              #ichannels=self.channels,
                              rate=self.rate,
        )

        self.frames = []
        self.mic.open_stream()

    def cut_frames(self):# cut_frames
        self.save_file(self.name+str(self.n_batch))
        self.n_batch += 1
        self.frames = []

    # save_file - сохранение файла в wav с необходимыми свойствами (из глобальных переменных)
    def save_file(self):
        wf = wave.open(self.name + ".wav", 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.mic.p.get_sample_size(self.format_))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

#sp = Audio_file()
#sp.start_record_from_mic()
#sp.save_file()
#stop_by_key('i', name='test', channels=2)