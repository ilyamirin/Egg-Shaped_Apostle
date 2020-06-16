#API

####аудиозаписи, устройства Raspberry

## - отправка запроса на запись:

#### Запрос:
```
POST /record?card=<номер карты>&mic=<номер микрофона>&time=<время записи в секундах>&file=<имя_файла (необязательно)>
```
curl:
```
curl -d "card=0&mic=0&time=10" -X POST 127.0.0.1:5721/record
```
#### Ответ:
```
{"response":"file /home/sde/Desktop/projects/Egg-Shaped_Apostle/services/audio_service/audio_endpoint/data/0_0_0_2020-06-13T00:11:33.273148.wav was recorded"}
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

## - отправка аудиозаписи по имени файла
#### Запрос:
```
POST /send?filename=<имя файла>
```
curl:
```
curl -d "filename=0_0_0_2020-05-22T11:04:18.980712.wav" -X POST 127.0.0.1:5721/send
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
#### 1. Открываем терминал и устанавливаем текущую папку как рабочую (или пользуемся GUI, правой кнопкой мыши по папке и "открыть в терминале")
```buildoutcfg
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