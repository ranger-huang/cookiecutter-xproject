# -*- coding: utf-8 -*-
{% if cookiecutter.use_celery == 'y' %}
from __future__ import absolute_import

import os

from celery import Celery
from django.apps import apps, AppConfig
from django.conf import settings

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{cookiecutter.system_slug}}_config.settings.local')  # pragma: no cover


app = Celery('{{cookiecutter.system_project_slug}}')


def celery_ready():
    app.config_from_object('django.conf:settings', namespace='{{cookiecutter.system_project_slug}}_CELERY')
    installed_apps = [app_config.name for app_config in apps.get_app_configs()]
    app.autodiscover_tasks(lambda: installed_apps, force=True)

class CeleryConfig(AppConfig):
    name = '{{cookiecutter.system_project_slug}}.taskapp'
    verbose_name = '{{cookiecutter.system_project_slug}} Celery Config'

    def ready(self):
        celery_ready()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))  # pragma: no cover
{% else %}
# Use this as a starting point for your project with celery.
# If you are not using celery, you can remove this app
{% endif -%}
