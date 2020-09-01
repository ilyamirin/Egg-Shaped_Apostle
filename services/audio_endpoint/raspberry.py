#!/usr/bin/env python3
import os
import threading
import wave
from subprocess import Popen, PIPE
from requests import post
from time import sleep

from audio_logger import get_logger
from config_gen import get_config
from datetime import datetime, timedelta


config = get_config()

if config.has_section('SETTINGS') and 'DEBUG' in config['SETTINGS'].keys():
    logger = get_logger(__name__, config['SETTINGS']['DEBUG'])
else:
    logger = get_logger(__name__, '1')


class Tree:
    def __init__(self):
        self.nodes = []

    def add_node(self, node_wannabe):
        for node in self.nodes:
            if node.no == node_wannabe.no:
                node.nodes.append(*node_wannabe.nodes)
                return self
        self.nodes.append(node_wannabe)
        return self


class Raspberry(Tree):
    def __init__(self, no=config['ENV']['DEV_NO']):
        super().__init__()
        self.no = no
        devices = self.get_devices()
        for card_no in devices:
            card = Card(self, card_no)
            self.add_node(card)
            for mic_no in devices[card_no]:
                card.add_node(Microphone(card, mic_no))
        # check data_dir
        if not os.path.exists(config['ENV']['DATA_DIR']):
            logger.debug('can\'t find data dir, trying to create...')
            try:
                os.makedirs(config['ENV']['DATA_DIR'])
            except Exception as e:
                logger.error(e)
        self.cards = {node.no: node for node in self.nodes}
        for node in self.nodes:
            node.mics = {node.no: node for node in node.nodes}
        self.recording_flag = False
        self.sending_flag = False

    @staticmethod
    def get_devices():
        """
        gets a input devices map in format:
        {
          card_1: [device_1, ..., device_n],
          card_2: [device_1, ..., device_n],
          ...,
          card_n: [device_1, ..., device_n],
        }
        """
        process = Popen(['/usr/bin/arecord -l'], stdout=PIPE, shell=True)
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

    @staticmethod
    def get_files_list():
        files_list = [i for i in os.listdir(config["ENV"]["DATA_DIR"]) if not i.endswith('_not_ready')]
        return files_list

    def parallel_record(self, time):
        threads = []
        for card in self.nodes:
            for mic in card.nodes:
                threads.append(threading.Thread(target=mic.record, args=[int(time) if time else None]))
        for thread in threads:
            thread.start()
        sleep(1)
        for thread in threads:
            thread.join()

    def record_by_work_time(self, time=None):
        start_hour = datetime.time(datetime.strptime(config["SETTINGS"]["START_HOUR"], '%H:%M'))
        end_hour = datetime.time(datetime.strptime(config["SETTINGS"]["END_HOUR"], '%H:%M'))
        logger.info(f'start record by time between {config["SETTINGS"]["START_HOUR"]}\
         and {config["SETTINGS"]["END_HOUR"]}...')
        while self.recording_flag:
            date_now = datetime.date(datetime.now())
            start_datetime = datetime.combine(date_now, start_hour)
            end_datetime = datetime.combine(date_now, end_hour)
            start_delta = datetime.now().timestamp() - start_datetime.timestamp()
            end_delta = datetime.now().timestamp() - end_datetime.timestamp()
            if start_delta > 0 > end_delta:
                logger.debug(f'Working hours, recording...')
                self.parallel_record(time)
            else:
                logger.debug(f'Not working hours, sleeping...')
                sleep(10)

    def send_file(self, file_name):
        """Sends file by http protocol, tries to send it by scp if fails"""
        try:
            logger.debug(f'Sending file {file_name} by http...')
            self.send_file_http(file_name)
        except Exception as e:
            logger.error(f'{e}. Sending file {file_name} by scp...')
            self.send_scp(file_name)

    @staticmethod
    def send_file_http(file_name,
                       dest_ip=config['FILE_SERVER']['web_api_ip'],
                       dest_port=config['FILE_SERVER']['web_api_port']):
        """Sends file by http protocol"""
        headers = {
            'content-type': 'audio/vnd.wave'
        }
        try:
            data = open(os.path.join(config['ENV']['DATA_DIR'], file_name), 'rb')
            response = post(f'http://{dest_ip}:{dest_port}/record/{file_name}', headers=headers, data=data)
            response.raise_for_status()
            with open('sent.txt', 'a+') as sent:
                sent.write(file_name + '\n')
            return response.json()
        except Exception as e:
            logger.error(e)
            raise

    @staticmethod
    def send_scp(file_name):
        """Sends file by scp. RSA authentication between server and client is needed"""
        try:
            input_file = os.path.join(config["ENV"]["DATA_DIR"], file_name)
            output_file = os.path.join(config['FILE_SERVER']['DIR'], file_name)
            dest = f"{config['FILE_SERVER']['USERNAME']}@{config['FILE_SERVER']['IP']}"
            logger.debug(f'Sending {input_file} to {dest}\'s {output_file}...')
            process = Popen(["scp", '-i', f"{config['ENV']['RSA_DIR']}", input_file, f"{dest}:{output_file}"],
                            stderr=PIPE,
                            stdout=PIPE)
            (out, err) = process.communicate()
            if out:
                logger.info(out)
            if err:
                logger.error(err)
            with open('sent.txt', 'a+') as sent:
                sent.write(file_name + '\n')
            return input_file
        except Exception as e:
            logger.error(e)

    def parallel_send(self, files):
        """Sends list of files and check local storage"""
        logger.debug(f'{files} to send')
        for file in files:
            self.send_file(file)
        files_list = [os.path.join(config["ENV"]["DATA_DIR"], i) for i in os.listdir(config["ENV"]["DATA_DIR"])]
        files_list.sort(key=lambda x: os.path.getmtime(x), reverse=False)
        while len(files_list) > 10:
            file_to_del = files_list[0]
            logger.debug(f'Amount of files exceeded ({len(files_list)}/10). Deleting  {file_to_del}...')
            os.remove(file_to_del)
            files_list = files_list[1:]

    @staticmethod
    def get_sent_files():
        if 'sent.txt' in os.listdir('./'):  # проверяем, есть ли список уже отправленных файлов
            with open('sent.txt', 'r') as sent:
                sent_files = sent.read().split('\n')  # читаем, если есть
        else:
            with open('sent.txt', 'w') as sent:
                sent.close()
            sent_files = []
        return sent_files

    # получаем дополнение мн-ва распознанных файлов ко всем, set быстрее в таких операциях
    def get_new_records(self):
        old_records = set(self.get_sent_files())
        try:
            records = set(self.get_files_list())
        except Exception as e:
            records = old_records
            logger.error(e)
        return records - old_records

    def send_by_adding(self):
        while self.sending_flag:
            files = self.get_new_records()
            if files:
                self.parallel_send(files)
            else:
                sleep(1)


class Card(Tree):
    def __init__(self, raspberry, no):
        super().__init__()
        logger.debug(f'Initialization of Card instance #{no} on Raspberry #{raspberry.no}')
        self.raspberry = raspberry
        self.no = no


# class of microphone
class Microphone:
    def __init__(self, card, no):
        logger.debug(f'Initialization of Microphone instance #{no} on card #{card.no} on Raspberry #{card.raspberry.no}')
        self.raspberry = card.raspberry
        self.card = card
        self.no = no
        self.stream = Popen(
            [f'/usr/bin/arecord -f S16_LE -D plughw:{self.card.no},{self.no}\
             -c 1 -N -r {config["SETTINGS"]["RECORD_SAMPLING_RATE"]}'],
            stdout=PIPE,
            stderr=PIPE,
            shell=True)
        self.last_read_time = None
        self.buf = self.read_stream()

    def read_stream(self):
        if (not self.last_read_time) or (datetime.now() - self.last_read_time).seconds >= 1:
            self.buf = self.stream.stdout.read(int(config["SETTINGS"]["RECORD_SAMPLING_RATE"])*2)
            self.last_read_time = datetime.now()
        return self.buf

    def record(self, time=None, file_name=None):
        try:
            time_rec = 0
            self.record_flag = True
            if not time:
                time = int(config['SETTINGS']['RECORD_DUR'])
            else:
                time = int(time)
            if not file_name:
                timestamp = str(datetime.now()).replace(' ', 'T')
                file_name = os.path.join(config["ENV"]["DATA_DIR"],
                                         f'{config["ENV"]["DEV_NO"]}_{self.card.no}_{self.no}_{timestamp}.wav')
            else:
                print(file_name)
            logger.debug(f'recording {file_name} (card: {self.card.no}, mic: {self.no}, time: {time})')
            with wave.open(file_name + '_not_ready', 'wb') as file:
                file.setnchannels(1)
                file.setsampwidth(2)
                file.setframerate(int(config["SETTINGS"]["RECORD_SAMPLING_RATE"]))
                for _ in range(time):
                    if self.raspberry.recording_flag:
                        file.writeframes(self.read_stream())
                        sleep(1)
                    else:
                        logger.debug(f'recording on card {self.card.no} mic {self.no}  manually stopped')
                        break
            os.rename(f'{file_name}_not_ready', file_name)
        except Exception as e:
            logger.error(e)
        return file_name



# a1 = Raspberry(1)
#a1.nodes[0].nodes[0].record(time=10)
# a1 = Raspberry(1)
# a = a1.nodes[2].nodes[0].start_stream()
# while True:
#     print(a.read(100))