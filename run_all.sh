#!/bin/bash
sh run_server_front.sh & python3 services/fts_service/fts_service.py  & python3 run_record_and_recognition.py
