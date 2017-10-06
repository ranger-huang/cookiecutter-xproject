# -*- coding: utf-8 -*-
from .base import *

THIRD_PARTY_APPS += [
    'django_extensions',
    'behave_django',
    'django_nose',
]
LOCAL_APPS += ['{{cookiecutter.system_project_slug}}.fts', ]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--failed',
    '--stop',
    '--nocapture',
    '--with-cov',
    '--cov-config=' + str(ROOT_DIR.path('{{cookiecutter.system_slug}}_conf/.coveragerc')),
    '--cov=' + str(ROOT_DIR.path()),
    '--cov-report=html',
    '--cov-report=xml',
    '--with-xunit',
    '--xunit-file=' + str(ROOT_DIR.path('test-reports/junit.xml')),
    ]

STATIC_URL = '/media/'
MEDIA_URL = '/media/'
STATICFILES_STORAGE = '{{cookiecutter.system_project_slug}}.storage.XZLocalStorage'
DEFAULT_FILE_STORAGE = '{{cookiecutter.system_project_slug}}.storage.XZLocalStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        "": {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

