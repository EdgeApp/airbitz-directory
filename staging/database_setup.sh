#!/bin/sh

DB=airbitz_directory
USER=airbitz
PASS=airbitz

dropdb $DB
dropdb template_postgis
psql -c 'drop role airbitz';

createdb template_postgis
psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql 
psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;"
psql -d template_postgis -c "GRANT ALL ON geography_columns TO PUBLIC;"
psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"

psql -c "create role $USER with login password '$PASS'";
createdb $DB -T template_postgis
psql -d $DB -c "grant all privileges on database $DB to $USER";


