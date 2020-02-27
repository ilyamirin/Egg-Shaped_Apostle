import psycopg2
import keyring
#keyring.set_password(service_name='postgreSQL', username='text_service', password='######')
#cursor.execute("DROP table text;")
#cursor.execute("CREATE TABLE text (id bigserial PRIMARY KEY, work_place int, date_time timestamp without time zone, text text);")

PG_DB_NAME = 'text'
PG_USER = 'text_service'
PG_SERVER_HOST = 'localhost'
PG_SERVER_PORT = '5432'


def full_text_search(work_place, role, date_time_start, date_time_end, query, top=5):
    conn = psycopg2.connect(
        host=PG_SERVER_HOST,
        port=PG_SERVER_PORT,
        dbname=PG_DB_NAME,
        user=PG_USER,
        password=keyring.get_password('postgreSQL', 'text_service'),
    )
    cursor = conn.cursor()
    #cursor.execute(f"SELECT id, text FROM text ORDER BY ts_rank(tsvector,plainto_tsquery('{query}')) DESC;")
    cursor.execute(f"SELECT id, work_place, role, date_time, text FROM text "
                   f"WHERE text.work_place='{work_place}' "
                   f"AND text.role='{role}' "
                   f"AND (text.date_time BETWEEN to_timestamp('{date_time_start}','YYYY-MM-DD HH24:MI:SS') AND to_timestamp('{date_time_end}','YYYY-MM-DD HH24:MI:SS')) "
                   f"ORDER BY ts_rank(tsvector,plainto_tsquery('{query}'))  DESC "
                   f"limit {top};"

                   )
    print(cursor.fetchall())
    cursor.close()
    conn.close()

full_text_search(1,1,'2020-02-04 12:30:22','2020-03-05 12:30:22','скиньте')
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

