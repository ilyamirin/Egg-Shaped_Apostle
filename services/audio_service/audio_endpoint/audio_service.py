#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
import multiprocessing as mp
import threading

from datetime import datetime
from time import sleep

from audio_logger import get_logger
from config_gen import get_config
config = get_config()

if config.has_section('SETTINGS'):
    if 'DEBUG' in config['SETTINGS'].keys():
        logger = get_logger("audio_service", config['SETTINGS']['DEBUG'])
else:
    logger = get_logger("audio_service", '1')


def get_devices():
    # gets a input devices map in format:
    # {
    #   card_1: [device_1, ..., device_n],
    #   card_2: [device_1, ..., device_n],
    #   ...,
    #   card_n: [device_1, ..., device_n],
    # }
    process = subprocess.Popen(['/usr/bin/arecord -l'], stdout=subprocess.PIPE, shell=True)
    (out, err) = process.communicate()
    if err:
        logger.error(err)
    out = out.decode("utf-8")
    out = out.split('\n')[1:]
    device_map = {}
    for i in out:
        # take the str starting with card...
        if i.startswith('card'):
            # ... and split it by comma, then split result by colon and take the last symbol in pre-colon str
            card, device = [int(j.split(':')[0][-1]) for j in i.split(',')]
            # append device to card's devices list if it exists in map, else create card and add list of devices
            logger.debug(f'found device {device} at card {card}')
            if card in device_map.keys():
                device_map[card].append(device)
            else:
                device_map[card] = [device, ]
    return device_map


def send(file, queue=None):
    try:
        input_file = os.path.join(config["ENV"]["DATA_DIR"], file)
        output_file = os.path.join(config['FILE_SERVER']['DIR'], file)
        dest = f"{config['FILE_SERVER']['USERNAME']}@{config['FILE_SERVER']['IP']}"
        logger.debug(f'Sending {input_file} to {dest}\'s {output_file}...')
        process = subprocess.Popen(["scp", '-i', f"{config['ENV']['RSA_DIR']}", input_file, f"{dest}:{output_file}"])
        (out, err) = process.communicate()
        if out:
            logger.info(out)
        if err:
            logger.error(err)
        files_list = [os.path.join(config["ENV"]["DATA_DIR"], i) for i in os.listdir(config["ENV"]["DATA_DIR"])]
        while len(files_list) > 10:
                file_to_del = files_list[0]
                logger.debug(f'Amount of files exceeded ({len(files_list)}/10). Deleting  {file_to_del}...')
                os.remove(file_to_del)
                files_list = files_list[1:]
        if queue:
            queue.put(input_file)
        return input_file, output_file
    except Exception as e:
        logger.error(e)


def parallel_send(files):
    logger.debug(f'{files} to send')
    sending_processes = []
    q = mp.Queue()
    for file in files:
        try:
            sending_processes.append(mp.Process(target=send, args=(file, q)))
        except Exception as e:
            logger.error(e)
    logger.debug(f'Parallel sendings: {len(sending_processes)}')
    results = []
    for i in sending_processes:
        i.start()
    for i in sending_processes:
        results.append(q.get())
        i.join()
    return results


def record(card, mic, time, file=None, queue=None):
    try:
        if not os.path.exists(config['ENV']['DATA_DIR']):
            logger.debug('can\'t find data dir, trying to create...')
            try:
                os.makedirs(config['ENV']['DATA_DIR'])
            except Exception as e:
                logger.error(e)
        if file:
            file_name = os.path.join(config["ENV"]["DATA_DIR"], file)
        else:
            timestamp = str(datetime.now()).replace(' ', 'T')
            file_name = os.path.join(config["ENV"]["DATA_DIR"],
                                     f'{config["ENV"]["DEV_NO"]}_{card}_{mic}_{timestamp}.wav')
        logger.debug(f'recording {file} (card: {card}, mic: {mic}, time: {time})')
        process = subprocess.Popen([f'/usr/bin/arecord -f cd -D plughw:{card},{mic} -c 1 -d {time} {file_name}'],
                                   stdout=subprocess.PIPE,
                                   shell=True)
        (out, err) = process.communicate()
        if out:
            logger.info(out)
        if err:
            logger.error(err)
        if queue:
            queue.put(file)
        return file_name
    except Exception as e:
        logger.error(e)


def parallel_record(cards, time=None):

    if not time:
        time = int(config['SETTINGS']['RECORD_DUR'])

    recording_processes = []
    q = mp.Queue()
    for card in cards:
        for mic in cards[card]:
            timestamp = str(datetime.now()).replace(' ', 'T')
            try:
                recording_processes.append(
                    mp.Process(target=record, args=(card, mic, time, f'{config["ENV"]["DEV_NO"]}_{card}_{mic}_{timestamp}.wav', q)))
            except Exception as e:
                logger.error(e)
    logger.debug(f'Parallel records: {len(recording_processes)}')
    results = []
    for i in recording_processes:
        i.start()
    for i in recording_processes:
        results.append(q.get())
        i.join()
    return results


def record_by_work_time(cards, time=None):
    global stop_recording_flag
    # takes the dict as described in get_devices, counts time and starts to record in working hours
    start_hour = datetime.time(datetime.strptime(config["SETTINGS"]["START_HOUR"], '%H:%M'))
    end_hour = datetime.time(datetime.strptime(config["SETTINGS"]["END_HOUR"], '%H:%M'))
    logger.info(f'start record by time between {config["SETTINGS"]["START_HOUR"]} and {config["SETTINGS"]["END_HOUR"]}...')
    while True:
        if stop_recording_flag: break
        # if keyboard.is_pressed('space'): break
        date_now = datetime.date(datetime.now())
        start_datetime = datetime.combine(date_now, start_hour)
        end_datetime = datetime.combine(date_now, end_hour)
        start_delta = datetime.now().timestamp() - start_datetime.timestamp()
        end_delta = datetime.now().timestamp() - end_datetime.timestamp()
        if start_delta > 0 > end_delta:
            logger.debug(f'Working hours, start recording...')
            results = parallel_record(cards, time)
            parallel_send(results)
        else:
            logger.debug(f'Not working hours, sleeping...')
            sleep(10)


def get_files_list():
    files_list = os.listdir(config["ENV"]["DATA_DIR"])
    return files_list


class AnotherProcessError(Exception):
    def __init__(self, message):
        self.message = message


stop_recording_flag = False
standalone_recording = False


def start_standalone_recording(time=None):
    if not time:
        time = int(config['SETTINGS']['RECORD_DUR'])
    global standalone_recording
    if standalone_recording:
        raise AnotherProcessError('There are another process recording')
    try:
        devices = get_devices()
        print(devices)
        recording_thread = threading.Thread(target=record_by_work_time, args=[devices, time])
        recording_thread.start()
        standalone_recording = True
        return standalone_recording
    except Exception as e:
        return logger.error(e)


def stop_standalone_recording():
    global stop_recording_flag
    stop_recording_flag = True
    logger.debug('Process will finish with last recording done')
    return 'Process will finish when last recording is done'


if __name__ == '__main__':
    start_standalone_recording()

