import requests
import psycopg2
import keyring

# keyring.set_password(service_name='postgreSQL', username='text_service', password='#####')


from config_gen import get_config
config = get_config()


audio_service_api = f'http://{config["NETWORK"]["AUDIO_SERVICE_IP"]}:{config["NETWORK"]["AUDIO_SERVICE_PORT"]}'


# audio_service API
def get_list_of_records():
    return requests.get(audio_service_api+'/records').json()


def get_raspberries():
    r = requests.get(audio_service_api + '/raspberry')
    return r.json()


def download_record(filename):
    r = requests.get(audio_service_api+'/records/send', data={'filename': filename})
    return r.content


def write_pg(work_place, role, date_time, text):
    conn = psycopg2.connect(
        host=config['NETWORK']['PG_SERVER_IP'],
        port=config['NETWORK']['PG_SERVER_PORT'],
        dbname=config['NETWORK']['PG_DB_NAME'],
        user=config['NETWORK']['PG_USER'],
        password=keyring.get_password('postgreSQL', config['NETWORK']['PG_USER']),
    )
    cursor = conn.cursor()
    print(work_place, role, date_time, text)
    cursor.execute(
        f"insert into text (work_place, role, date_time,  text, tsvector) VALUES ({work_place}, {role}, '{date_time}','{text}', (SELECT to_tsvector('russian', '{text}'))); COMMIT;")
    # cursor.execute("SELECT * FROM text;")
    # print(cursor.fetchall())
    cursor.close()
    conn.close()