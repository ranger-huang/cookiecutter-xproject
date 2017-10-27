# -*- coding: utf-8 -*-
import os

import environ

# {{cookiecutter.system_project_slug}}/{{cookiecutter.system_slug}}_config/settings/base.py - 3 = {{cookiecutter.system_project_slug}}/
ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('{{cookiecutter.system_project_slug}}')

# Load operating system environment variables and then prepare to use them
env = environ.Env()
# .env file, should load only in development environment
DOT_ENV_FILE = os.environ.get('DOT_ENV_FILE', default='{{cookiecutter.system_slug}}_config/local.env')
if DOT_ENV_FILE:
    env_file = str(ROOT_DIR.path(DOT_ENV_FILE))
    if os.path.exists(env_file):
        print('Loading : {}'.format(env_file))
        env.read_env(env_file)
        print('The env file has been loaded. See base.py for more information.')

# Quick-start development settings -
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('DJANGO_SECRET_KEY', '')

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', True)

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # for allauth
    'django.contrib.sites',

    # Useful template tags:
    'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
]

THIRD_PARTY_APPS = [
    'crispy_forms',  # Form layouts
    'allauth',  # registration
    'allauth.account',  # registration
    'allauth.socialaccount',  # registration

    'rest_framework',
    'django_user_agents',
    'import_export',
]

LOCAL_APPS = [
    '{{cookiecutter.system_project_slug}}',
    '{{cookiecutter.system_project_slug}}.users',
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': '{{ cookiecutter.project_slug }}.contrib.sites.migrations'
}

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]


# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("""{{cookiecutter.author_name}}""", '{{cookiecutter.email}}'),
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

ALLOWED_HOSTS = [
    '*'
]

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    {% if cookiecutter.use_mysql == 'y' -%}
    '{{cookiecutter.use_mysql_alias}}': env.db('MYSQL_DATABASE_URL'),
    {%- endif %}
    {% if cookiecutter.use_postgresql == 'y' -%}
    '{{cookiecutter.use_postgresql_alias}}': env.db('POSTGRES_DATABASE_URL'),
    {%- endif %}
    {% if cookiecutter.use_postgresql == 'n' and cookiecutter.use_mysql -%}
    'default': env.db('DATABASE_URL'),
    {%- endif %}
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = '{{ cookiecutter.timezone }}'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_ROOT = ROOT_DIR('static')

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    # APPS_DIR('static'),
]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_URL = '/static/'
STATICFILES_STORAGE = '{{cookiecutter.system_project_slug}}.storage.XZLocalStaticStorage'
DEFAULT_FILE_STORAGE = '{{cookiecutter.system_project_slug}}.storage.XZLocalStorage'

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_URL = '/media/'
MEDIA_ROOT = ROOT_DIR('media')


# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = '{{cookiecutter.system_slug}}_conf.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = '{{cookiecutter.system_slug}}_conf.wsgi.application'

# PASSWORD STORAGE SETTINGS
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# Password validation
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
    ('zh-hans', _('中文简体')),
    ('zh-hant', _('中文繁體')),
    ('en', _('English')),
)
LOCALE_PATHS = (
    APPS_DIR('locale'),
)


########## CACHE
CACHES = {
    "session": env.cache_url('CACHE_REDIS_URL_SESSION', default='redis://'),
    "default": env.cache_url('CACHE_REDIS_URL_DEFAULT', default='redis://'),
}
########## END CACHE

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'EXCEPTION_HANDLER': '{{cookiecutter.system_project_slug}}.restfw.views.exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        '{{cookiecutter.system_project_slug}}.restfw.authentication.CsrfExemptSessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],
}

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Some really nice defaults
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
ACCOUNT_ADAPTER = '{{cookiecutter.system_project_slug}}.users.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = '{{cookiecutter.system_project_slug}}.users.adapters.SocialAccountAdapter'

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'users:redirect'
LOGIN_URL = 'account_login'

# Location of root django.contrib.admin URL, use {% raw %}{% url 'admin:index' %}{% endraw %}
ADMIN_URL = r'^admin/'

# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

{% if cookiecutter.use_celery == 'y' %}
########## CELERY
LOCAL_APPS += ['{{cookiecutter.system_project_slug}}.taskapp.celery.CeleryConfig']
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', default='django://')
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND', default='django://')
CELERY_TASK_ALWAYS_EAGER = env.str('CELERY_TASK_ALWAYS_EAGER', default=False)
CELERY_TASK_SERIALIZER = 'json'
CELERYD_SEND_EVENTS = True
########## END CELERY
{% endif %}

{%- if cookiecutter.use_compressor == 'y'-%}
# django-compressor
# ------------------------------------------------------------------------------
THIRD_PARTY_APPS += ['compressor']
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

STATICFILES_FINDERS += ['compressor.finders.CompressorFinder']
{%- endif %}

# ------------------------------------------------------------------------------
# Constants
from {{cookiecutter.system_slug}}_conf.constants import *

