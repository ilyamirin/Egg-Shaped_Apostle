#!/bin/bash
sudo -u postgres bash -c : && RUNAS="sudo -u postgres"
$RUNAS bash<<_
echo "creating administrators role..."
createuser administrators -d -r -P
echo "creating services role..."
createuser services -P
echo "creating text_service role..."
createuser text_service -g services -P

createdb text

psql
\c text

CREATE TABLE text (id bigserial PRIMARY KEY, work_place int, role text, date_time timestamp without time zone, text text);
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE text TO administrators;
GRANT SELECT, INSERT ON TABLE text TO services;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO services;