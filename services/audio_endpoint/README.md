# API

#### аудиозаписи, устройства Raspberry

## - отправка запроса на запись:

#### Запрос:
```
POST /<номер карты>/<номер микрофона>/record/?time=<время записи в секундах (необязательно, возьмет стандартное по серверу)>&file=<имя_файла (необязательно)>
```
curl:
```
curl -X POST '127.0.0.1:5721/0/0/record?time=10&file=test_not_ready'
```
#### Ответ:
```
{"response":"ok"}
```

## - отправка списка аудиозаписей, находящихся в хранилище:
#### Запрос:
```
GET /records
```
#### Ответ:
```
[filename1, filename2, filename3]
```
curl:
```
curl -X GET '127.0.0.1:5721/records'
```
#### Начало и остановка параллельной записи:
```
POST /parallel_rec/start?time=10
GET /parallel_rec/stop
```
#### Ответ:

```
{'response': 'true'}
```
####curl:
```
curl -d "time=10" -X POST 127.0.0.1:5721/parallel_rec/start
```

## - отправка аудиозаписи по имени файла (будет изменено в дальнейшем)
#### Запрос:
```
POST /send?filename=<имя файла>
```
curl:
```
curl -X POST '127.0.0.1:5721/send?filename=0_0_0_2020-08-23T22:05:35.511531.wav'
```
#### Ответ:
```
{'response': f'file {file} was sended to {outputfile} in main storage server'}
```

## - отправка списка подключенных устройств 
#### Запрос:
```
GET /devices
```
curl:
```
curl -X GET 127.0.0.1:5721/devices
```
#### Ответ:

```
{
    card_1: [device_1, ..., device_n],
    card_2: [device_1, ..., device_n],
    ...,
    card_n: [device_1, ..., device_n],
    }
```

## - отправка и редактирование конфигурации
#### Запрос на получение конфигурации:
```
GET /config
```
#### Ответ:

```
text файла конфигурации
```
#### Отправка конфигурации:
```
POST /config?config=<текст файла конфигурации>
```
#### Ответ:

```
{'response': 'successful overwriting of config.ini'}
```

TODO:
- Запись в стендалоун-режиме
- открытие стрима с определенного микрофона
- получение и редактирование карты рабочих мест


# Перед стартом:

## Для распберри:
### 1) в ~/:
```
git clone https://github.com/ilyamirin/Egg-Shaped_Apostle.
```
### 2) Заходим в ~/Egg-shaped_Apostle/services/endpoint_service
### 3) Настраиваем ключи для доступа по scp на случай падения audio_service на сервере:
```
ssh-keygen
./id_rsa
ENTER
ENTER
ssh-copy-id sde@192.168.0.1
chmod 0700 id_rsa id_rsa.pub
```
### 4) Запускаем python3 config_gen.py со следующими параметрами
```
python3 config_gen.py -u User -d 1 -s /User/media/data/ -t 3600 -m 09:00 -e 19:00
```
### 5) Меняем конфигурацию по необходимости
```
nano config.ini
```

#### 1. Открываем терминал и устанавливаем текущую папку как рабочую (или пользуемся GUI, правой кнопкой мыши по папке и "открыть в терминале")
```
cd /home/sde/Desktop/projects/Egg-Shaped_Apostle/services/audio_service/
```
#### 1. запускаем python3 config_gen.py со следующими параметрами (указаны по умолчанию):
- -u/--username sde
- -p/--password sde
- -d/--debug 1
- -s/--dir /home/sde/
- -t/--rec_dur 30
- -m/--start_time 09:00
- -e/--end_time 19:00
т.е., например,
```buildoutcfg
python3 config_gen.py -u pi - p raspberry -d 1 -t 10 -m 09:00 -e 19:00
```
# Старт:
Как только появился файл config.ini,
```buildoutcfg
python3 audio_service.py
```

pyaudio:
```
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo -H python3 -m pip install pyaudio
```
