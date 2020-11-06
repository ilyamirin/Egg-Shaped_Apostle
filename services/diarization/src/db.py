import os
import sqlite3
import json

from config_gen import get_config
config = get_config()

db_name = os.path.join(config['ENV']['ROOT_ABS_PATH'], config['ENV']['DIAR_DB_NAME'])

if not config['ENV']['DIAR_DB_NAME'] in  os.listdir(config['ENV']['ROOT_ABS_PATH']):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE diarized (name text,  annotation json)''')
    conn.commit()
    conn.close()


def create_record(filename, annotation):
    filename = os.path.basename(filename)
    annot_json = json.dumps(annotation)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO diarized (name, annotation) VALUES (?, ?)", [filename, annot_json])
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


def get_annotation_by_filename(filename):
    filename = os.path.basename(filename)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT annotation FROM diarized WHERE name = ?;', [filename])
    results = json.loads(cursor.fetchone()[0])
    conn.close()
    return results


def get_list_of_diarized():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM diarized;')
    results = [i[0] for i in cursor.fetchall()]
    conn.close()
    return results


def check_if_exists_by_name(filename):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(annotation) FROM diarized WHERE name = ?;', [filename])
    result = int(cursor.fetchone()[0])
    conn.close()
    return True if result else False

