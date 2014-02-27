#!/bin/bash

source $HOME/airbitz/ENV/bin/activate
if [[ -e /etc/profile.d/environment_vars.sh ]]; then
    source /etc/profile.d/environment_vars.sh
fi

echo "Rebuilding"
python $HOME/airbitz/ENV/airbitz/manage.py update_index --batch-size 100 --remove directory
echo "Rebuilding finished"

