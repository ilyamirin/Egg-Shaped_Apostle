#!/usr/bin/env python
# -*- coding: utf-8 -*-
# creates config.ini and sets default settings if not exists
__author__ = "Paul Maksimov"
__copyright__ = "Copyright 2020, The Egg-Shaped Apostle Project"
__version__ = "1.0.0"
__maintainer__ = "Paul Maksimov"
__email__ = "work.xenus@gmail.com"
__status__ = "Production"
import psycopg2
import keyring
from logger import get_logger
from config_gen import get_config

# keyring.set_password(service_name='postgreSQL', username='text_service', password='#####')
config = get_config()
if config.has_section('SETTINGS') and 'DEBUG' in config['SETTINGS'].keys():
    logger = get_logger("storage_service", config['SETTINGS']['DEBUG'])
else:
    logger = get_logger("storage_service", '1')


def __execute(query):
    try:
        conn = psycopg2.connect(
            host=config['PG']['SERVER_IP'],
            port=config['PG']['SERVER_PORT'],
            dbname=config['PG']['DB_NAME'],
            user=config['PG']['USER'],
            password=keyring.get_password('postgreSQL', config['PG']['USER']),
        )
        cursor = conn.cursor()
        cursor.execute(query)
        try:
            result = cursor.fetchall()
        except psycopg2.ProgrammingError as e:
            result = 'true'
        cursor.close()
        conn.close()
        logger.debug(f'upon "{query}" returns {len(result)} rows')
        return result
    except Exception as e:
        logger.error(e)
        return e


def record_create(work_place, role, date_time, text):
    return __execute(f"insert into text (work_place, role, date_time,  text, tsvector) \
        VALUES ({work_place}, {role}, '{date_time}','{text}', (SELECT to_tsvector('russian', '{text}')));\
        COMMIT;")


def record_read(record_id):
    return __execute(f"SELECT * FROM text WHERE id = {record_id};")


def table_read():
    return __execute("SELECT * FROM text")


def full_text_search(work_place=None, role=None, date_time_start='2020-02-01', date_time_end='2999-02-28', query='', top=5):
    filter_ = ''
    filter_work_place = f"text.work_place = '{work_place}' AND "
    filter_role = f"text.role = '{role}' AND "
    if work_place is not None and role is not None:
        filter_ = filter_work_place + filter_role
    elif work_place is not None:
        filter_ = filter_work_place
    elif role is not None:
        filter_ = filter_role
    # print(work_place, role, date_time_start, date_time_end, query, top)
    query = f"SELECT id, work_place, role, date_time, text FROM text "\
            f"WHERE {filter_}" \
            f"(text.date_time BETWEEN to_timestamp('{date_time_start}','YYYY-MM-DD HH24:MI:SS.SSS') AND to_timestamp('{date_time_end}','YYYY-MM-DD HH24:MI:SS.SSS')) "\
            f"ORDER BY ts_rank(tsvector, plainto_tsquery('russian','{query}'))  DESC "\
            f"limit {top};"
    return __execute(query)


def filter_by(work_place=None, role=None, date_time_start='2020-02-01', date_time_end='2999-02-28'):
    print(work_place, role, date_time_start, date_time_end)
    filter_ = ''
    filter_work_place = f"text.work_place = '{work_place}' AND "
    filter_role = f"text.role = '{role}' AND "
    if work_place is not None and role is not None:
        filter_ = filter_work_place + filter_role
    elif work_place is not None:
        filter_ = filter_work_place
    elif role is not None:
        filter_ = filter_role
    # print(work_place, role, date_time_start, date_time_end, query, top)
    query = f"SELECT id, work_place, role, date_time, text FROM text " \
            f"WHERE {filter_}" \
            f"(text.date_time BETWEEN to_timestamp('{date_time_start}','YYYY-MM-DD HH24:MI:SS.SSS') AND to_timestamp('{date_time_end}','YYYY-MM-DD HH24:MI:SS.SSS')) "
    return __execute(query)


# for i in table_read():
#     print(i)
# # print(full_text_search(query='здорова бандиты'))
# for i in filter_by(1):
#     print(i)

