import socket
import config
import configparser
from audio.devices_wrapper import Microphone

config = configparser.ConfigParser()
print('Reading configuration file...', end='')

config.read('config.ini')
print('OK')

data_chunk = 1024

def stream_audio():

    print('Reading server network configuration...', end='')
    s_ip = config['NETWORK']['SERVER_IP']
    s_port = int(config['NETWORK']['SERVER_PORT'])
    s_addr = (s_ip, s_port)
    print('OK')

    print('Creating socket...')
    s = socket.socket()
    s.bind(s_addr)
    print(f'Socket successfully created at {s_ip}:{s_port}.')
    print('listening incoming connections...')
    s.listen(1)
    mic = Microphone()
    mic.open_stream()
    conn, addr = s.accept()
    print(f'Incoming connection from {addr[0]}:{addr[1]}.')
    while True:
        data = mic.stream.read(data_chunk)
        try:
            conn.send(data)
        except:
            conn.close()
            s.close()
            stream_audio()

stream_audio()