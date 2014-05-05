#!/bin/bash
#
# Get latest database and media files from staging server
#
# REQUIRES dev_keys file to be copied to /staging/.ssh/dev_keys manually


# Text color variables
txtund=$(tput sgr 0 1)          	# Underline
txtbld=$(tput bold)             	# Bold
bldred=${txtbld}$(tput setaf 1) 	# red
bldblu=${txtbld}$(tput setaf 4) 	# blue
bldwht=${txtbld}$(tput setaf 7) 	# white

comment=${txtbld}$(tput setaf 3)	# yellow
txtcmd=${txtbld}$(tput setaf 6) 	# light blue

txtrst=$(tput sgr0)             	# Reset
info=${bldwht}*${txtrst}        	# Feedback
pass=${bldblu}*${txtrst}
warn=${bldred}*${txtrst}
ques=${bldblu}?${txtrst}


DUMP_FILE=$1
STAGING_SERVER_USER=devbitz
STAGING_SERVER_IP=198.61.228.9


if [ "$DUMP_FILE" = "" ]
then
	DATE=`date +%Y-%m-%d`
	DUMP_FILE=$DATE"_00-00-01.dump"
	echo ""
	echo "No dumpfile specified so defaulting to last nights backup."${txtrst}
	echo ${txtcmd}"$DUMP_FILE"${txtrst}
	echo ""

fi

echo ${txtcmd}"Copying DB backup file from Staging server now"${txtrst}
echo ""

rsync --progress --inplace --delete -avz --rsh 'ssh -i /staging/.ssh/dev_keys' $STAGING_SERVER_USER@$STAGING_SERVER_IP:~/backups/$DUMP_FILE /staging/$DUMP_FILE

echo ""
echo ${txtcmd}"Importing DB backup now using load_backup.sh"${txtrst}
echo ""

./load_backup.sh $DUMP_FILE

echo ""
echo ${txtcmd}"Updating solr index"${txtrst}
echo ""

cd /home/vagrant/airbitz/ENV/airbitz
./rebuild_index.sh

echo ""
echo ${txtcmd}"Syncing MEDIA files now"${txtrst}
echo ""

cd /staging
rsync --progress --inplace -avz --rsh 'ssh -i /staging/.ssh/dev_keys' $STAGING_SERVER_USER@$STAGING_SERVER_IP:/home/$STAGING_SERVER_USER/media/ /staging/media/

