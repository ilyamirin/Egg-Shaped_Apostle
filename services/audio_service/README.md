#API

####аудиозаписи, устройства Raspberry
запуск записи
```curl -d "card=0&mic=0&time=10" -X POST 'http://127.0.0.1:5722/raspberry/0/record'```

## - отправка списка аудиозаписей, находящихся в хранилище:
#### Запрос:
```
GET /records
```
#### Ответ:
```
[filename1, filename2, filename3]
```
### curl:
```
curl -X GET 127.0.0.1:5722/records
```
## - отправка аудиозаписи по имени файла
#### Запрос:
```
GET /records/send?filename=<имя файла>
```
curl:
```
curl -d '{"filename":"0_0_0_2020-05-22T11:04:18.980712.wav"}' -X GETT 127.0.0.1:5721/send
```
#### Ответ:
```
{'response': 'file sended'}
```

## - оправка списка подключенных устройств 
#### Запрос:
```
GET /rasberry
```
curl:
```
curl -X GET 'http://127.0.0.1:5722/raspberry'
```
#### Ответ:

```
{"0":{"devices":{"0":[0]},"ip":"127.0.0.1","no":0}}
```

## Подключение к определенной raspberry:
```
/rasbperry/<номер распберри>/<API audio_endpoint>
```

## Запуск параллельной записи:
```
/rasbperry/<номер распберри>/<API audio_endpoint>
```

TODO:
- открытие стрима с определенного микрофона

# старт:
Запускаем audio_service.py
```
python3 audio_service.py
```

Для настройки сети:
здесь eth1=<интерфейс к сети raspberry>, eth0=<интерфейс к интернету на сервере>. Проверь ifconfig

Сервер:
sudo apt install isc-dhcp-server
INTERFACES="eth1"
sudo nano /etc/dhcp/dhcpd.conf
```
option domain-name-servers 8.8.8.8, 8.8.4.4;
authoritative;

subnet 192.168.0.0 netmask 255.255.255.0 {
  range 192.168.0.2 192.168.0.254;
  option domain-name-servers 8.8.8.8, 8.8.4.4;
  option subnet-mask 255.255.255.0;
  option routers 192.168.0.1;
  default-lease-time -1;
  max-lease-time -1;
}
```
sudo iptables -A FORWARD -o eth0 -i eth1 -s 192.168.0.0/24 -m conntrack --ctstate NEW -j ACCEPT
sudo iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -t nat -F POSTROUTING
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

