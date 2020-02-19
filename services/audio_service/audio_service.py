import pyaudio
import wave

p = pyaudio.PyAudio()

class Microphone():
    def __init__(self, inp_device_ind=None):
        self.inp_dev_ind = inp_device_ind

    # open_stream - задает формат для записи (из глабальных переменных) и создает пустой фрейм, в который будет добавляться запись

    def open_stream(self):

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
        self.

    # cut_frames

    def cut_frames(self, WAVE_OUTPUT_FILENAME):
        self.save_file(WAVE_OUTPUT_FILENAME)
        self.frames = []

    # save_file - сохранение файла в wav с необходимыми свойствами (из глобальных переменных)

    def save_file(self, WAVE_OUTPUT_FILENAME):

        wf = wave.open(WAVE_OUTPUT_FILENAME + ".wav", 'wb')
        wf = wf.setnchannels(Recording_CHANNELS)
        wf = wf.setsampwidth(self.p.get_sample_size(Recording_FORMAT))
        wf = wf.setframerate(Recording_RATE)
        wf = wf.writeframes(b''.join(self.frames))
        wf.close()


p.terminate()
#recording = Recording()
#recording.stop_by_key('i', 'test')