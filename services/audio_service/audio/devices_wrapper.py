import pyaudio
import wave
from time import time

#Recording_CHUNK = 1024
#Recording_FORMAT = pyaudio.paInt16
#Recording_CHANNELS = 2
#Recording_RATE = 44100
#Recording_FOLDER = r'C:/Users/User/Desktop/projects/Egg-Shaped_Apostle/data/'


class AudioObj(object):
    def __init__(self, chunk=1024, format_=pyaudio.paInt16, channels=2, rate=48000, **kwargs):
        self.p = pyaudio.PyAudio()
        self.chunk = chunk
        self.format_ = format_
        self.channels = channels
        self.rate = rate

    def open_stream(self, **kwargs):
        self.stream = self.p.open(format=self.format_,
                                  rate=self.rate,
                                  channels=self.channels,
                                  frames_per_buffer=self.chunk,
                                  **kwargs)
        return True

    def close_stream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        return True


class Microphone(AudioObj):
    def __init__(self, inp_device_ind=None, **kwargs):
        super().__init__(**kwargs)
        self.inp_dev_ind = inp_device_ind

    def open_stream(self):
        super().open_stream(input=True, input_device_index=self.inp_dev_ind)


class Speaker(AudioObj):
    def __init__(self, output_device_ind=None, **kwargs):
        super().__init__(**kwargs)
        self.output_device_ind = output_device_ind

    def start_stream_from_mic(self, inp_device_ind=None, listen_time=10, **kwargs):
        self.kwargs = kwargs
        self.mic = Microphone(inp_device_ind, **self.kwargs)
        self.mic.open_stream()
        self.open_stream(output=True)

        start_time = time()
        while time() - start_time <= listen_time:
            data = self.mic.stream.read(self.chunk)
            self.stream.write(data)

        self.stop_stream_from_mic()
        return True

    def stop_stream_from_mic(self):
        self.mic.close_stream()
        self.close_stream()
        return True


class AudioFile(AudioObj):

    def __init__(self, output_path=None, name='unnamed', **kwargs):
        super().__init__(**kwargs)
        self.kwargs = kwargs
        self.output_path = output_path
        self.name = name
        self.n_batch = 0
        self.frames_used_flag = False
        self.frames = []

    def start_record_from_mic(self, **kwargs):
        self.mic = Microphone(**kwargs)
        self.mic.open_stream()

    def cut_frames(self):# cut_frames
        self.frames_used_flag = True
        self.save_file()
        self.n_batch += 1
        self.frames = []

    # save_file - сохранение файла в wav с необходимыми свойствами (из глобальных переменных)
    def save_file(self):
        if self.output_path:
            if self.frames_used_flag:
                full_name = self.output_path + self.name + '_' + self.n_batch+".wav"
            else:
                full_name = self.output_path + self.name + ".wav"
        else:
            if self.frames_used_flag:
                full_name = self.name + '_' + self.n_batch+".wav"
            else:
                full_name = self.name + ".wav"
        wf = wave.open(full_name, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.mic.p.get_sample_size(self.format_))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

