from devices_wrapper import Microphone, AudioFile, Speaker

sp = Speaker(channels=2, output_device_ind=7, chunk=2048, rate=48000)
sp.start_stream_from_mic(inp_device_ind=13, chunk=2048, channels=1, listen_time=10, rate=48000)