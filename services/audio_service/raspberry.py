from datetime import datetime
import subprocess
import signal
import os
from audio_logger import get_logger
import multiprocessing as mp

logger = get_logger("rasbperry", '1')


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
    def __init__(self, ip, user, no):
        super().__init__()
        self.ip = ip
        self.user = user
        self.no = no
        self._get_devices()

    def _get_devices(self):
        # gets a input devices map in format:
        # {
        #   card_1: [device_1, ..., device_n],
        #   card_2: [device_1, ..., device_n],
        #   ...,
        #   card_n: [device_1, ..., device_n],
        # }
        process = subprocess.Popen([f'ssh {self.user}@{self.ip} "arecord -l"'], stdout=subprocess.PIPE, shell=True)
        (out, err) = process.communicate()
        if err:
            logger.error(err)
        out = out.decode("utf-8")
        out = out.split('\n')[1:]
        for i in out:
            # take the str starting with card...
            if i.startswith('card'):
                # ... and split it by comma, then split result by colon and take the last symbol in pre-colon str
                card_no, mic_no = [int(j.split(':')[0][-1]) for j in i.split(',')]
                logger.debug(f'found device {mic_no} at card {card_no} on Raspberry #{self.no}')
                card = Card(self, card_no)
                card.add_node(Microphone(card, mic_no))
                self.add_node(card)

    def parallel_record(self, dir, dur):
        recording_processes = []
        for card in self.nodes:
            for mic in card.nodes:
                try:
                    recording_processes.append(mp.Process(target=mic.record, args=(48000, dir, dur)))
                except Exception as e:
                    logger.error(e)
        logger.debug(f'Parallel records: {len(recording_processes)}')
        for i in recording_processes:
            i.start()
        for i in recording_processes:
            i.join()
            i.terminate()


class Card(Tree):
    def __init__(self, raspberry, no):
        super().__init__()
        logger.debug(f'Initialization of Card object #{no} on Raspberry #{raspberry.no}')
        self.raspberry = raspberry
        self.no = no


# class of microphone
class Microphone:
    def __init__(self, card, no):
        logger.debug(f'Initialization of microphone object #{no} on card #{card.no} on Raspberry #{card.raspberry.no}')
        self.raspberry = card.raspberry
        self.card = card
        self.no = no
        self.__role = None
        self.__workplace = None

    # Roles and workplaces are set manually
    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, role):
        self.__role = role

    @property
    def workplace(self):
        return self.__workplace

    @workplace.setter
    def workplace(self, role):
        self.__workplace = role

    def listen(self, duration):
        logger.debug(f'Listening of microphone with #{self.no} on card #{self.card.no} on Raspberry #{self.card.raspberry.no} for {duration} seconds...')
        command = f'ssh {self.raspberry.user}@{self.raspberry.ip} "arecord -f S16_LE  --duration {duration} -c 2 -D hw:{self.card.no},{self.no}" | aplay'
        os.system(command)

    def stream(self, sample_rate, target):
        logger.debug(f'Streaming from microphone with #{self.no} on card #{self.card.no} on Raspberry #{self.card.raspberry.no}...')
        command = f'ssh {self.raspberry.user}@{self.raspberry.ip} "arecord -f S16_LE --rate {sample_rate} -c 2 -D hw:{self.card.no},{self.no}"'
        with open(target, 'w') as target:
            pro = subprocess.run(command, stdout=target, shell=True)

    # def stream(self, sample_rate, target):
    #     logger.debug(f'Streaming from microphone with #{self.no} on card #{self.card.no} on Raspberry #{self.card.raspberry.no}...')
    #     command = f'ssh {self.raspberry.user}@{self.raspberry.ip} "arecord -f S16_LE --rate {sample_rate} -c 2 -D hw:{self.card.no},{self.no}"'
    #     with open(target, 'w') as target:
    #         pro = subprocess.run(command, stdout=target, shell=True)

    def record(self, sample_rate, directory, duration):
        if self.workplace and self.role:
            filename = f'{self.workplace}_{self.role}_{str(datetime.now()).replace(" ", "T")}.wav'
        else:
            filename = f'{self.card.raspberry.no}_{self.card.no}_{self.no}_{str(datetime.now()).replace(" ", "T")}.wav'
        logger.debug(f'Recording {filename} with duration of {duration} seconds from microphone with #{self.no} on card #{self.card.no} on Raspberry #{self.card.raspberry.no}...')
        command = f'ssh {self.raspberry.user}@{self.raspberry.ip} "arecord --duration {duration} -D plughw:{self.card.no},{self.no}" | arecord --duration {duration} --file-type wav {directory}{filename}'
        print(command)
        # process = subprocess.Popen(command, shell=True)
        # process.communicate()
        os.system(command)
        logger.debug(f'Recording {filename} with duration of {duration} seconds from microphone with #{self.no} on card #{self.card.no} on Raspberry #{self.card.raspberry.no} done.')
        return True

# a1 = Raspberry('192.168.0.102', 'pi', 1)
# a1.parallel_record('/media/user/data', 10)
