# берет все устройства из локальной сети
# подключается к ним через SSH
# отправляет на них требование записи
# принимает запись в файл в указанную папку.

from datetime import datetime
from time import sleep
import os

from raspberry import Raspberry
from network_utils import get_active_addresses
from audio_logger import get_logger
from config_gen import get_config
from ssh_connect import no_pass_ssh

logger = get_logger("audio_service", '1')

config = get_config()


def get_raspberries():
    addresses = get_active_addresses()
    raspberries = []
    i = 0
    for ip in addresses:
        if 'raspberries_list' not in os.listdir():
            os.system('touch raspberries_list')
        with open('raspberries_list', 'r+') as list:
            rasp_list = list.read().split('\n')
            if ip not in rasp_list:
                with open('raspberries_list', 'a+') as list:
                    no_pass_ssh(ip, config['RASPBERRY']['USERNAME'], config['RASPBERRY']['PASSWORD'])
                    list.write(ip+'\n')
        raspberries.append(Raspberry(ip, config['RASPBERRY']['USERNAME'], i))
        i += 1
    return raspberries


def record_by_work_time(raspberries):
    # takes the dict as described in get_devices, counts time and starts to record in working hours
    start_hour = datetime.time(datetime.strptime(config["SETTINGS"]["START_HOUR"], '%H:%M'))
    end_hour = datetime.time(datetime.strptime(config["SETTINGS"]["END_HOUR"], '%H:%M'))
    logger.info(f'start record by time between {config["SETTINGS"]["START_HOUR"]} and {config["SETTINGS"]["END_HOUR"]}...')
    while True:
        # if keyboard.is_pressed('space'): break
        date_now = datetime.date(datetime.now())
        start_datetime = datetime.combine(date_now, start_hour)
        end_datetime = datetime.combine(date_now, end_hour)
        start_delta = datetime.now().timestamp() - start_datetime.timestamp()
        end_delta = datetime.now().timestamp() - end_datetime.timestamp()
        if start_delta > 0 > end_delta:
            logger.debug(f'Working hours, start recording...')
            for rasp in raspberries:
                rasp.parallel_record(config['ENV']['DATA_DIR'], config['SETTINGS']['RECORD_DUR'])
        else:
            logger.debug(f'Not working hours, sleeping...')
            sleep(10)


if __name__ == '__main__':
    raspberries = get_raspberries()
    record_by_work_time(raspberries)