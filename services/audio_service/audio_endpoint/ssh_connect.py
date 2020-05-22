#!/usr/bin/env python3
import subprocess
import sys, os

user, ip, password = sys.argv[1:4]

pathname = os.path.dirname(sys.argv[0])
path = os.path.abspath(pathname)

if 'id_rsa' not in os.listdir('.'):
    subprocess.Popen([f'ssh-keygen -b 2048 -t rsa -f {path}/id_rsa -q -N ""', ' <<< y >/dev/null'], shell=True)


def exec_with_pass(script):
    script = f'expect {path}/ssh_connection.sh {password} ssh {user}@{ip} '+script
    subprocess.Popen(script, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

create_dir = f'mkdir -p .ssh'
add_key = f'cat {path}/id_rsa.pub | ssh {user}@{ip} "cat >> .ssh/authorized_keys"'
exec_with_pass(create_dir)
exec_with_pass(add_key)
print('SSH key added.')

