import psycopg2
import keyring
from datetime import datetime
#keyring.set_password(service_name='postgreSQL', username='text_service', password='######')
#cursor.execute("DROP table text;")
#cursor.execute("CREATE TABLE text (id bigserial PRIMARY KEY, work_place int, date_time timestamp without time zone, text text);")

PG_DB_NAME = 'text'
PG_USER = 'text_service'
PG_SERVER_HOST = 'localhost'
PG_SERVER_PORT = '5432'


def full_text_search(work_place=None, role=None, date_time_start='2020-02-01', date_time_end='2020-02-28', query='', top=5):
    date_time_start = date_time_start.replace('T', ' ')
    date_time_end = date_time_end.replace('T', ' ')
    conn = psycopg2.connect(
        host=PG_SERVER_HOST,
        port=PG_SERVER_PORT,
        dbname=PG_DB_NAME,
        user=PG_USER,
        password=keyring.get_password('postgreSQL', 'text_service'),
    )



    cursor = conn.cursor()
    filter = ''
    filter_work_place = f"text.work_place = '{work_place}' AND "
    filter_role = f"text.role = '{role}' AND "
    if work_place is not None and role is not None:
        filter = filter_work_place + filter_role
    elif work_place is not None:
        filter = filter_work_place
    elif role is not None:
        filter = filter_role
    print(work_place, role, date_time_start, date_time_end, query, top)
    query = f"SELECT id, work_place, role, date_time, text FROM text "\
            f"WHERE {filter}" \
            f"(text.date_time BETWEEN to_timestamp('{date_time_start}','YYYY-MM-DD HH24:MI:SS.SSS') AND to_timestamp('{date_time_end}','YYYY-MM-DD HH24:MI:SS.SSS')) "\
            f"ORDER BY ts_rank(tsvector,plainto_tsquery('{query}'))  DESC "\
            f"limit {top};"
    cursor.execute(query)
    return cursor.fetchall()
    cursor.close()
    conn.close()

def check_table():
    conn = psycopg2.connect(
        host=PG_SERVER_HOST,
        port=PG_SERVER_PORT,
        dbname=PG_DB_NAME,
        user=PG_USER,
        password=keyring.get_password('postgreSQL', 'text_service'),
    )
    cursor = conn.cursor()


    cursor.execute("SELECT * FROM text;")
    print(cursor.fetchall())
    cursor.close()
    conn.close()

#print(full_text_search(date_time_start='2020-02-13T14:00:00.000Z', date_time_end='2020-02-28T20:00:00.000Z', query='привет'))

#check_table()