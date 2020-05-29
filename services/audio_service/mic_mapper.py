from audio_service import get_raspberries
import json

map = {}
raspberries = get_raspberries()
for rasp in raspberries:
    map[rasp.no] = {}
    for card in rasp.nodes:
        map[rasp.no][card.no] = {}
        for mic in card.nodes:
            map[rasp.no][card.no][mic.no] = {}
            while True:
                mic.listen(30)
                repeat = input('Введите Y, чтобы отметить микрофон и N, чтобы прослушать еще раз')
                if repeat.lower() == 'y':
                    w_r = input('введите номер рабочего места W и роль R в формате: W R')
                    w, r = w_r.split()
                    map[rasp.no][card.no][mic.no]['workplace'] = w
                    map[rasp.no][card.no][mic.no]['role'] = r
                    break

with open('mic_map.txt', 'w+') as map_file:
    map_file.write(json.dumps(map))