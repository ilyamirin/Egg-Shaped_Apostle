#!/usr/bin/env python
# -*- coding: utf-8 -*-
# creates config.ini and sets default settings if not exists
__author__ = "Paul Maksimov"
__copyright__ = "Copyright 2020, The Egg-Shaped Apostle Project"
__version__ = "1.0.0"
__maintainer__ = "Paul Maksimov"
__email__ = "work.xenus@gmail.com"
__status__ = "Production"
from flask_web_server import app, wrap_response, request
from postgre_api import *
from logger import get_logger
from config_gen import get_config


config = get_config()
if config.has_section('SETTINGS') and 'DEBUG' in config['SETTINGS'].keys():
    logger = get_logger("storage_service", config['SETTINGS']['DEBUG'])
else: logger = get_logger("storage_service", '1')


@app.route('/record/create', methods=['POST'])
def record_create_q():
    logger.debug(f'got record creation request with form: {request.form}; json: {request.json}')
    try:
        resp = record_create(
            work_place=request.json['work_place'],
            role=request.json['role'],
            date_time=request.json['date_time'],
            text=request.json['text'])
        return wrap_response(resp)
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
    return resp


@app.route('/record', methods=['GET'])
def table_read_q():
    logger.debug(f'got getting all rows request with form: {request.form}; json: {request.json}')
    try:
        resp = table_read()
        return wrap_response(resp)
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
    return resp


@app.route('/record/<int:record_id>', methods=['GET'])
def record_read_q(record_id):
    logger.debug(f'got getting row request with form: {request.form}; json: {request.json}')
    try:
        resp = record_read(record_id)
        return wrap_response(resp)
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
    return resp


@app.route('/fts', methods=['GET'])
def fts_q():
    logger.debug(f'got fts request with form: {request.form}; json: {request.json}')
    try:
        kwargs = request.form
        # print(kwargs)
        resp = full_text_search(**kwargs)
        return wrap_response(resp)
    except Exception as e:
        logger.error(e)
        resp = wrap_response({'error': str(e)})
    return resp


if __name__ == '__main__':
    app.run(host=config['NETWORK']['WEB_API_IP'], port=config['NETWORK']['WEB_API_PORT'])
