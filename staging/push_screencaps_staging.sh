#!/bin/bash
#
# Copy all the screencaps from local vagrant instance to staging server
#
# REQUIRES dev_keys file to be copied to /staging/.ssh/dev_keys manually


STAGING_SERVER_USER="devbitz"
STAGING_SERVER_IP="198.61.228.9"

RSYNC_SRC="/staging/media/screencaps/"
RSYNC_DEST="${STAGING_SERVER_USER}@$STAGING_SERVER_IP:~/media/screencaps"

rsync --progress --inplace --exclude=".DS_Store" -avz --rsh 'ssh -i /staging/.ssh/dev_keys' $RSYNC_SRC $RSYNC_DEST