#1. передаем файлы через scp
- audio_logger.py,
- audio_service.py,
- config_gen.py,
- expect_5.45.4-2+b1_armhf.deb,
- ssh_connect.py,
- ssh_connection.sh

#2. подключаемся к распберри через ssh, запускаем  deploy.py со следующими параметрами (указаны по дефолту):
- -n/--device 0
- -a/--ip 127.0.0.1
- -f/--port 22
- -u/--username sde
- -p/--password sde
- -d/--debug 1
- -s/--dir /home/sde/
- -t/--rec_dur 30
- -m/--start_time 09:00
- -e/--end_time 19:00
```
sudo python3 deploy.py \
-n 0 \
-a 192.169.0.1 \
-f 22 \
-u user \
-p Fefu2019 \
-d 1 \
-s /media/user/data/ \
-t 3600 \
-m 09:00 \
-n 19:00
```