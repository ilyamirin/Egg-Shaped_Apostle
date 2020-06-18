import requests
from config_gen import get_config
from datetime import datetime
import json
config = get_config()
storage_service_api = f"http://{config['NETWORK']['STORAGE_SERVICE_IP']}:{config['NETWORK']['STORAGE_SERVICE_PORT']}"
fts_service_api = f"http://{config['NETWORK']['FTS_SERVICE_IP']}:{config['NETWORK']['FTS_SERVICE_PORT']}"


def get_all_records():
    return requests.get(storage_service_api+'/record').json()


def format_date(date):
    date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
    return datetime.strftime(date, '%Y-%m-%dT%H:%M:%S.%fZ')


def send_record(work_place, role, date_time, text):
    data = {
        'work_place': work_place,
        'role': role,
        'date_time': date_time,
        'text': text
    }
    return requests.post(fts_service_api + '/write', data=data).json()


records = get_all_records()

for record in records[1000]:
    send_record(record[0], record[1], record[2], record[3])


