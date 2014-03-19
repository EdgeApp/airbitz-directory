#!/bin/bash
echo "Stopping gunicorn_django processes"
killall gunicorn_django
echo "Processes stopped."

source $HOME/breadsticks/ENV/bin/activate
if [[ -e /etc/profile.d/environment_vars.sh ]]; then
    source /etc/profile.d/environment_vars.sh
fi

LOGFILE=/tmp/gunicorn.log
NUM_WORKERS=4
echo ""
echo "Starting gunicorn"
gunicorn_django --daemon -w $NUM_WORKERS --log-file=$LOGFILE 2>>$LOGFILE
echo "Gunicorn started. Logs can be found at $LOGFILE"
