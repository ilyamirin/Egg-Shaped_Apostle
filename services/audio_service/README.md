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