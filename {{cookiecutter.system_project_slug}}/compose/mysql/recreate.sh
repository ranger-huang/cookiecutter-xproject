#!/bin/bash

# stop on errors
set -e

echo "beginning recreate from $MYSQL_DATABASE"
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
