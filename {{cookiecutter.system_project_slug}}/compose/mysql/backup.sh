#!/bin/bash
# stop on errors
set -e

# export the postgres password so that subsequent commands don't ask for it

echo "creating backup"
echo "---------------"

FILENAME=backup_$(date +'%Y_%m_%dT%H_%M_%S').sql.gz
mysqldump -h mysql -u $MYSQL_USER --password=$MYSQL_PASSWORD $MYSQL_USER | gzip > /backups/$FILENAME

echo "successfully created backup $FILENAME"
