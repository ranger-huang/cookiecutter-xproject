#!/bin/bash

# stop on errors
set -e


# export the postgres password so that subsequent commands don't ask for it


# check that we have an argument for a filename candidate
if [[ $# -eq 0 ]] ; then
    echo 'usage:'
    echo '    docker-compose run mysql restore <backup-file>'
    echo ''
    echo 'to get a list of available backups, run:'
    echo '    docker-compose run mysql list-backups'
    exit 1
fi

# set the backupfile variable
BACKUPFILE=/backups/$1

# check that the file exists
if ! [ -f $BACKUPFILE ]; then
    echo "backup file not found"
    echo 'to get a list of available backups, run:'
    echo '    docker-compose run postgres list-backups'
    exit 1
fi

echo "beginning restore from $1"
echo "-------------------------"

# delete the db
# deleting the db can fail. Spit out a comment if this happens but continue since the db
# is created in the next step
echo "deleting old database $MYSQL_DATABASE"
if echo "DROP DATABASE $MYSQL_DATABASE;" | mysql -u $MYSQL_USER --password=$MYSQL_PASSWORD $MYSQL_DATABASE
then echo "deleted $MYSQL_DATABASE database"
else echo "database $MYSQL_DATABASE does not exist, continue"
fi

# create a new database
echo "creating new database $MYSQL_DATABASE"
echo "CREATE DATABASE $MYSQL_DATABASE;" | mysql -u $MYSQL_USER --password=$MYSQL_PASSWORD

# restore the database
echo "restoring database $MYSQL_USER"
gunzip -c $BACKUPFILE | mysql -u $MYSQL_USER --password=$MYSQL_PASSWORD
