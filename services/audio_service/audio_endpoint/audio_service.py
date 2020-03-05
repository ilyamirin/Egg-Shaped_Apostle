import subprocess
import multiprocessing as mp
from datetime import datetime
import paramiko
import configparser
from time import sleep
from os import remove, listdir


config = configparser.ConfigParser()
config.read('config.ini')
#keyring.set_password('audio_service', config['FILE_SERVER']['USERNAME'], #####)
START_HOUR = datetime.time(datetime.strptime('02:00', '%H:%M'))
END_HOUR = datetime.time(datetime.strptime('08:00', '%H:%M'))

files_list = [config["ENV"]["DATA_DIR"]+i for i in listdir(config["ENV"]["DATA_DIR"])]

def send_to_file_server(input_file, output_file):
    global files_list

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(config['FILE_SERVER']['IP'], port=int(config['FILE_SERVER']['PORT']), username=config['FILE_SERVER']['USERNAME'], key_filename='/home/pi/.ssh/id_rsa')
    sftp = ssh.open_sftp()
    sftp.put(input_file, output_file)

    files_list.append(input_file)
    if len(files_list) > 10:
        remove(files_list[0])
        files_list = files_list[1:]


def record(q, card, mic, time, file):
    subprocess.call([r'/usr/bin/arecord', '-f', 'cd', '-D' f'plughw:{card},{mic}', '-c', '1', '-d', f'{time}', f'{config["ENV"]["DATA_DIR"]+file}'])
    q.put(file)


def parallel_record(cards):
    recording_processes = []
    q = mp.Queue()
    for card in cards:
        for mic in cards[card]:
            timestamp = str(datetime.now()).replace(' ', 'T')
            recording_processes.append(
                mp.Process(target=record, args=(q, card, mic, 3600, f'{card}_{mic}_{timestamp}.wav')))

    results = []

    for i in recording_processes:
        i.start()

    for i in recording_processes:
        results.append(q.get())

    for i in recording_processes:
        i.join()

    return results


def record_by_work_time(cards):
    while True:
        date_now = datetime.date(datetime.now())
        start_datetime = datetime.combine(date_now, START_HOUR)
        end_datetime = datetime.combine(date_now, END_HOUR)
        start_delta = datetime.now().timestamp() - start_datetime.timestamp()
        end_delta  = datetime.now().timestamp() - end_datetime.timestamp()
        if start_delta > 0 and end_delta < 0:
            results = parallel_record(cards)
            for file in results:
                send_to_file_server(config["ENV"]["DATA_DIR"]+file, config['FILE_SERVER']['DIR']+file)
        else:
            sleep(10)


cards = {1: [0,], 2: [0,]}

record_by_work_time(cards)


def get_devices():
    subprocess.call([r'/usr/bin/aplay', '-l'])

print(get_devices())

