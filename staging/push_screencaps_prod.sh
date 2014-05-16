#!/bin/bash
#
# Copy all the screencaps from local vagrant instance to production server
#
# REQUIRES dev_keys file to be copied to /staging/.ssh/prod_keys manually


STAGING_SERVER_USER="bitz"
STAGING_SERVER_IP="192.237.240.48"

RSYNC_SRC="/staging/media/screencaps/"
RSYNC_DEST="${STAGING_SERVER_USER}@$STAGING_SERVER_IP:~/media/screencaps"

rsync --progress --inplace --delete --exclude=".DS_Store" -avz --rsh 'ssh -i /staging/.ssh/prod_keys' $RSYNC_SRC $RSYNC_DEST