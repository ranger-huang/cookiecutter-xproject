#!/bin/bash
set -e
cmd="$@"

{% if cookiecutter.use_postgresql == 'y' %}
export POSTGRES_DATABASE_URL=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_USER
function postgres_ready(){
python3 << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="$POSTGRES_USER", user="$POSTGRES_USER", password="$POSTGRES_PASSWORD", host="$POSTGRES_HOST", port=$POSTGRES_PORT)
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}


until postgres_ready; do
  >&2 echo "Postgresql Database is unavailable - sleeping"
  sleep 1
done
{% endif %}

{% if cookiecutter.use_mysql == 'y' %}
export MYSQL_DATABASE_URL=mysql://$MYSQL_USER:$MYSQL_PASSWORD@$MYSQL_HOST:$MYSQL_PORT/$MYSQL_DATABASE
function mysql_ready(){
python3 << END
import sys
import _mysql
# mysqlclient
try:
    db=_mysql.connect(db="$MYSQL_DATABASE",user="$MYSQL_USER", passwd="$MYSQL_PASSWORD", host="$MYSQL_HOST", port=$MYSQL_PORT)
except _mysql.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until mysql_ready; do
  >&2 echo "MySQL Database is unavailable - sleeping"
  sleep 1
done
{% endif %}


>&2 echo "Database is up - continuing..."
exec $cmd
