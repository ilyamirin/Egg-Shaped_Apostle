#!/usr/bin/env python3
import os
import subprocess
from audio_logger import get_logger
from config_gen import get_config
from datetime import datetime

config = get_config()

if config.has_section('SETTINGS'):
    if 'DEBUG' in config['SETTINGS'].keys():
        logger = get_logger("audio_service", config['SETTINGS']['DEBUG'])
else:
    logger = get_logger("audio_service", '1')


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

    @staticmethod
    def get_files_list():
        files_list = [i for i in os.listdir(config["ENV"]["DATA_DIR"]) if not i.endswith('_not_ready')]
        return files_list

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

    def record(self, time=config['SETTINGS']['RECORD_DUR'], file_name=None):
        try:

            if not file_name:
                timestamp = str(datetime.now()).replace(' ', 'T')
                file_name = os.path.join(config["ENV"]["DATA_DIR"],
                                         f'{config["ENV"]["DEV_NO"]}_{self.card.no}_{self.no}_{timestamp}.wav')
            logger.debug(f'recording {file_name} (card: {self.card.no}, mic: {self.no}, time: {time})')
            process = subprocess.Popen(
                ['/usr/bin/arecord',
                 '-f', 'cd',
                 '-D', f'plughw:{self.card.no},{self.no}',
                 '-c', '1',
                 f'-d {time}',
                 '-N',
                 '-r', f'{config["SETTINGS"]["RECORD_SAMPLING_RATE"]}',
                 f'{file_name}_not_ready'])

            (out, err) = process.communicate()
            if out:
                logger.info(out)
            if err:
                logger.error(err)
            os.rename(f'{file_name}_not_ready', file_name)

        except Exception as e:
            logger.error(e)

    def start_stream(self):

        self.stream = subprocess.Popen(
            [f'/usr/bin/arecord -f cd -D plughw:{self.card},{self.no} -c 1 -N -r {config["SETTINGS"]["RECORD_SAMPLING_RATE"]}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)
        return self.stream.stdin

    def stop_stream(self):
        self.stream.kill()
        del self.stream

#a1 = Raspberry('127.0.0.1', 1)
#a1.nodes[0].nodes[0].record('test', 10)