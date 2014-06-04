#!/bin/sh
#
# EXAMPLE CRON
# */5 * * * * $HOME/airbitz/ENV/airbitz/screencapper.sh > /tmp/screencaps.log 2>&1
#
PATH=$HOME/local/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

echo '--------------------------------------------------'
echo "STARTED: " `date`
echo '--------------------------------------------------'

# make sure to kill any existing processes before creating new ones in case they are stuck
ps -ef | grep 'node\|phantomjs\|screencapper.py' | awk '{print $2}' | xargs -i kill {}

# call screencapper.py with a timeout before the next cron job runs
timeout 280 $HOME/airbitz/ENV/bin/python $HOME/airbitz/ENV/airbitz/screencapper.py

echo '--------------------------------------------------'
echo "FINISHED: " `date`
echo '--------------------------------------------------'
echo ''
echo ''