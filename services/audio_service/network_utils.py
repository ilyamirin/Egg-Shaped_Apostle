import os
import threading
import socket
from audio_logger import get_logger

logger = get_logger("network_utils", '1')


def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Создаем сокет (UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Настраиваем сокет на BROADCAST вещание.
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]


def scan_ip(ip, addr_list):
    my_ip = get_my_ip()
    net_split = my_ip.split('.')
    net = '.'.join(net_split[:-1])+'.'
    addr = net + str(ip)
    command = "ping -c 1 " + addr
    response = os.popen(command)
    data = response.readlines()

    for line in data:
        if 'ttl' in line:
            addr_list.append(addr)
            break


def scan_pool(addr_list, start_point=2, end_point=254):
    for ip in range(start_point, end_point):
        thread = threading.Thread(target=scan_ip, args=[ip, addr_list])
        thread.start()

    thread.join()


def get_active_addresses():
    addr_list = []
    scan_pool(addr_list)
    addr_list = addr_list # .remove(get_my_ip())
    if not addr_list:
        logger.warning('no ip found while scanning. Check connection.')
        return []
    return addr_list