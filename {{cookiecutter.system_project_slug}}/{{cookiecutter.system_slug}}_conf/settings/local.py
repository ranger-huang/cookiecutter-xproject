# -*- coding: utf-8 -*-
from .base import *

SECRET_KEY = "CHANGEME!!!"
# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
THIRD_PARTY_APPS += [
    'django_extensions',
    #'behave_django',
    #'django_nose',
    'rest_framework_swagger',
]
LOCAL_APPS += ['{{cookiecutter.system_project_slug}}.fts', ]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_STORAGE = '{{cookiecutter.system_project_slug}}.storage.XZLocalStaticStorage'
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


