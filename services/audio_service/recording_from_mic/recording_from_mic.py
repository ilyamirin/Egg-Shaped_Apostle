import keyboard
import pyaudio
import wave

CHUNK = 1024

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
# RECORD_SECONDS = 5   #длительность проигрывания
WAVE_OUTPUT_FILENAME = "output_test.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)): #на случай записи конкретной длительности
while True:
    try:
        if keyboard.is_pressed('q'):
            print('You Pressed A Key!')
            break  # finishing the loop
        data = stream.read(CHUNK)
        frames.append(data)
    except:
        break

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()