#!/bin/bash

file=$1
db=airbitz_directory
cwd=$(pwd)

sudo su - postgres <<EOF
dropdb $db
createdb $db 
pg_restore -F c -d $db $cwd/$file
psql -d $db -c "grant all privileges on database $db to airbitz";
EOF

