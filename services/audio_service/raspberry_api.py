from audio_logger import get_logger
import requests

logger = get_logger("rasbperry", '1')
PORT = '5721'


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
    def __init__(self, ip, no):
        super().__init__()
        self.ip = ip
        self.no = no
        self.api = f'http://{self.ip}:{PORT}'
        devices = self.get_devices()
        for card_no in devices:
            card = Card(self, card_no)
            self.add_node(card)
            for mic_no in devices[card_no]:
                card.add_node(Microphone(card, mic_no))

    def get_records(self):
        r = requests.get(self.api+'/records')
        return r.json()

    def send(self, filename):
        r = requests.post(self.api+'/send', data={'filename': filename})
        return r.json()

    def get_devices(self):
        r = requests.get(self.api+'/devices')
        return r.json()

    def get_config(self):
        r = requests.get(self.api+'/config')
        return r.json()

    def set_config(self, config):
        r = requests.post(self.api+'/config', data={'config': config})

    def start_parallel_record(self, time):
        params = {
            'time': time,
        }

        r = requests.post(self.api + '/parallel_rec/start', params=params)
        return r.json()

    def stop_parallel_record(self):
        r = requests.get(self.api + '/parallel_rec/stop')
        return r.json()


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

    def record(self, time, file=None):
        params = {
            'card': self.card.no,
            'mic': self.no,
            'time': time,
            'file': file
        }

        r = requests.post(self.raspberry.api + '/record', params=params)
        return r.json()


a1 = Raspberry('127.0.0.1', 1)