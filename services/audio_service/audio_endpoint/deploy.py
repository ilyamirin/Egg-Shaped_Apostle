#!/usr/bin/env python3
# #2. подключаемся к распберри через ssh
# - выполняем config_gen с параметрами:
#
#   ```sudo python3 config_gen.py ```
# - выполняем установку expect
#
#   ```sudo dpkg -i expect_5.45.4-2+b1_armhf.deb```
# - выполняем передачу ssh-ключа
#
#   ```sudo ssh_connect.py USERNAME=user IP=127.0.0.1 PASSWORD```
# - запускаем audio_service.py
#
#   ```sudo python3 audio_service.py```

import sys, os
import argparse
import subprocess

pathname = os.path.dirname(sys.argv[0])
path = os.path.abspath(pathname)

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--device', default='0')
parser.add_argument('-a', '--ip', default='127.0.0.1')
parser.add_argument('-f', '--port', default='22')
parser.add_argument('-u', '--username', default='sde')
parser.add_argument('-p', '--password', default='sde')
parser.add_argument('-d', '--debug', default='0')
parser.add_argument('-s', '--dir', default='/home/sde/')
parser.add_argument('-t', '--rec_dur', default='30')
parser.add_argument('-m', '--start_time', default='09:00')
parser.add_argument('-e', '--end_time', default='19:00')
namespace = parser.parse_args(sys.argv[1:])

package_expect = 'expect_5.45.4-2+b1_armhf.deb'
if package_expect in os.listdir('.'):
    subprocess.call(f'sudo dpkg -i {path+"/"+package_expect}', shell=True)
    subprocess.call(f'sudo python3 ssh_connect.py {namespace.username} {namespace.ip} {namespace.password}', shell=True)
    subprocess.call(f'sudo python3 audio_service.py', shell=True)
else:
    print('No expect package found.')
