import psycopg2
import keyring
#keyring.set_password(service_name='postgreSQL', username='text_service', password='######')
#cursor.execute("DROP table text;")
#cursor.execute("CREATE TABLE text (id bigserial PRIMARY KEY, work_place int, date_time timestamp without time zone, text text);")

PG_DB_NAME = 'text'
PG_USER = 'text_service'
PG_SERVER_HOST = 'localhost'
PG_SERVER_PORT = '5432'

def write_row(work_place, role, text):
    conn = psycopg2.connect(
        host=PG_SERVER_HOST,
        port=PG_SERVER_PORT,
        dbname=PG_DB_NAME,
        user=PG_USER,
        password=keyring.get_password('postgreSQL', 'text_service'),
    )
    cursor = conn.cursor()
    cursor.execute(f"insert into text (work_place, role, date_time, text) VALUES ({work_place}, {role} 'now', '{text}'); COMMIT;")
    cursor.execute("SELECT * FROM text;")
    #print(cursor.fetchall())
    #cursor.close()
    conn.close()

#write_row(1, 'wow that sucks')


'''class connection(psycopg2.connect):
    def __init__(self):
        # noinspection PyArgumentList
        self.cursor = super(
                        
                        ).cursor()
    
    def select_all_rows(self):
        self.cursor.execute("SELECT * FROM text;")
        print(self.cursor.fetchall())
        self.cursor.close()
    
    def add_row(self, work_place, text):
        self.
        self.commit()
    
    def commit(self):
        self.cursor.execute("COMMIT;")
    self.cursor.close()
    self.close()
    
cursor.execute()
cursor.execute("COMMIT;")

cursor = conn.cursor()
cursor.execute("SELECT * FROM text;")
print(cursor.fetchall())
cursor.close()
conn.close()'''