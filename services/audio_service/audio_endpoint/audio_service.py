import subprocess
import ray
from datetime import datetime
import paramiko
import configparser
import keyring

#keyring.set_password('audio_service', 'pi', ########)
config = configparser.ConfigParser()
config.read('config.ini')

ray.init()

@ray.remote
def record(card, mic, time, file):
    subprocess.call([r'/usr/bin/arecord', '-f', 'cd', '-D' f'plughw:{card},{mic}', '-d', f'{time}', f'{config["ENV"]["DATA_DIR"]+file}'])
    return file

def get_devices():
    subprocess.call([r'/usr/bin/aplay', '-l'])

def send_file(input_file, output_file):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(config['FILE_SERVER']['IP'], port=int(config['FILE_SERVER']['PORT']), username=config['FILE_SERVER']['USERNAME'], password=keyring.get_password('audio_service', 'pi'))
    sftp = ssh.open_sftp()
    sftp.put(input_file, output_file)

#print(get_devices())
cards = {2: [0,], 3: [0,]}

def record_work_day(cards):
    while True:
        recording_processes = []

        for card in cards:
            for mic in cards[card]:
                timestamp = str(datetime.now()).replace(' ', 'T')
                recording_processes.append(record.remote(card, mic, 10, f'{card}_{mic}_{timestamp}'))

        for file in ray.get(recording_processes):
            send_file(config["ENV"]["DATA_DIR"]+file, config['FILE_SERVER']['DIR'])