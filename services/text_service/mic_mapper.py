from audio_service_client import get_raspberries
import json

map = {}
raspberries = get_raspberries()
for rasp in raspberries:
    map[rasp] = {}
    for card in raspberries[rasp]['devices']:
        map[rasp][card] = {}
        for mic in raspberries[rasp]['devices'][card]:
            map[rasp][card][mic] = {}
            w_r = input(f'введите номер рабочего места W и роль R в формате: W R для\n'
                        f'Raspberry {rasp},\n'
                        f'карты {card},\n'
                        f' микрофона {mic}')
            w, r = w_r.split()
            map[rasp][card][mic]['workplace'] = w
            map[rasp][card][mic]['role'] = r

with open('mic_map.txt', 'w+') as map_file:
    map_file.write(json.dumps(map))
