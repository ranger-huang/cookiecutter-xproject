#!/bin/sh
test_type=$1

if [[ "$test_type" ='UT' ]]; then
    python3 manage.py test --keepdb {{cookiecutter.system_project_slug}}.tests
elif [[ "$test_type" ='FT' ]]; then
    python3 manage.py behave --keepdb {{cookiecutter.system_project_slug}}/fts/features/
else
    python3 manage.py test --keepdb {{cookiecutter.system_project_slug}}.tests
    python3 manage.py behave --keepdb {{cookiecutter.system_project_slug}}/fts/features/
fi
# python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000
