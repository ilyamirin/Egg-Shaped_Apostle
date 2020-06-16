CREATE TABLE text (id bigserial PRIMARY KEY, work_place int, role text, date_time timestamp without time zone, text text, tsvector tsvector);
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE text TO administrators;
GRANT SELECT, INSERT ON TABLE text TO services;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO services;