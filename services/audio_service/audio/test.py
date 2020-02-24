import keyboard
from devices_wrapper import AudioFile


def stop_by_key(key='space', mic_settings={}, **kwargs):
    file = AudioFile(**kwargs)
    print(f'* start recording. Press {key} to stop...')
    file.start_record_from_mic(**mic_settings)
    while True:
        data = file.mic.stream.read(file.chunk)
        file.frames.append(data)
        if keyboard.is_pressed(key):
            print('Recording stopped...')
            data = file.mic.stream.read(file.chunk)
            # data = file.mic.stream.read()
            file.frames.append(data)
            break
    print("* done recording")
    file.mic.close_stream()
    file.save_file()
    print(f'Saved to file {file.name}.wav')


stop_by_key(name='mic2', key='i', mic_settings={'inp_device_ind': 2, 'channels': 1, 'rate': 96000})