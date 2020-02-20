from pydub import AudioSegment
import wave

DATA_DIR = r'../../../../data/'
file = AudioSegment.from_wav(DATA_DIR+r'main_microphone_2020-02-20 15. 29. 57.369451.wav')
file = file.set_frame_rate(48000)
file = file.set_channels(2)
file.export('file.wav', format='wav', bitrate=16)
print(help(file.set_channels))
