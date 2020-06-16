#API

####аудиозаписи, устройства Raspberry


## - отправка списка аудиозаписей, находящихся в хранилище:
#### Запрос:
```
GET /records
```
#### Ответ:
```
[filename1, filename2, filename3]
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
```buildoutcfg
/rasbperry/<номер распберри>/<API audio_endpoint>
```


TODO:
- открытие стрима с определенного микрофона

# старт:
Запускаем audio_service.py
```
python3 audio_service.py
```