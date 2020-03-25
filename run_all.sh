#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "starting ElasticSearch server..."
gnome-terminal -e "sudo -i service elasticsearch start"
echo "Done."

echo "starting web-interface server..."
gnome-terminal -e "sh $DIR/run_server_front.sh"
echo "Done."

echo "starting text-search server..."
gnome-terminal -e "python3.8 $DIR/services/fts_service/fts_service.py"
echo "Done."

echo "Running cli-interface of recording and recognition..."
gnome-terminal -e "sudo python3.8 run_record_and_recognition.py"
echo "Done."

sleep 10

url='http:localhost:4200'
firefox -new-window $url 
