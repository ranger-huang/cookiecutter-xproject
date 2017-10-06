#!/bin/sh
rm -f /app/.noseids /app/.coverage
rm -rf /app/test-reports /app/allure-reports
mkdir -p /app/test-reports /app/test-reports/allure-reports
python3 manage.py behave {{cookiecutter.system_project_slug}}/fts/features/
python3 manage.py test --keepdb {{cookiecutter.system_project_slug}}.tests

python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000
