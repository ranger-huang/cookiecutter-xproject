#!/bin/sh
python3 /app/manage.py collectstatic --noinput
python3 /app/manage.py migrate
/usr/local/bin/gunicorn {{cookiecutter.system_project_slug}}.wsgi -c /gunicorn_conf.py --chdir=/app
