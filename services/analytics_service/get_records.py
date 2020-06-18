import requests

storage_service_api = 'http://127.0.0.1:5730'
analytics_service_api = 'http://127.0.0.1:5731'


def get_records(work_place, role, date_time_start, date_time_end):
    headers = {
            'Content-Type': 'application/json'
        }
    payload = {
        'work_place': work_place,
        'role': role,
        'date_time_start': date_time_start,
        'date_time_end': date_time_end,
    }
    r = requests.get(analytics_service_api+'/analyse',
                      params=payload,
                      headers=headers).json()
    return r

#
# results = get_records(work_place=1, role=0, date_time_start='2020-02-16', date_time_end='2020-06-20')
#
# print(results)