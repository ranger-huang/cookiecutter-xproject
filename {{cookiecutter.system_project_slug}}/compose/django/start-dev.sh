#!/bin/sh
python3 manage.py migrate
python3 manage.py runserver_plus 0.0.0.0:8000
