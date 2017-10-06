import os
import shutil
import sys

from cookiecutter.main import cookiecutter

cur_cc = os.path.abspath(
        os.path.dirname(os.path.dirname(os.path.relpath(__file__))))

context = {
    "system_name": "XSystem",
    "system_slug":  "xsystem",
    "project_name": "XProject",
    "project_slug": "xproject",
    "system_project_slug": "xsystem_xproject",
    "system_project_short": "xsystemxproject",
    "system_project_name": "XSystem XProject",
    "system_project_id": "01",
    "author_name": "Your Name",
    "email": "your.name@domain.com",

    "description": "A short description of the project.",
    "domain_name": "xproject.xsystem.com",
    "version": "0.1.0",
    "timezone": "Asia/Shanghai",
    "python_version": "3.6",
    "use_pycharm": "y",
    "use_cas": "y",
    "use_mailhog": "y",
    "use_celery": "y",
    "use_docker": "y",
    "use_compressor": "y",
    "use_websocket": "y",
    "postgresql_version": "9.6",
    "mysql_version": "5.6",

    "use_python3": "y",
    "use_postgresql": "y",
    "use_postgresql_alias": "db2",
    "use_mysql": "y",
    "use_mysql_alias": "default",

    "release_date": "{% now 'local' %}",
    "_extensions": ["jinja2_time.TimeExtension"],
    "_copy_without_render": [
        "playbook/*"
    ]
}

checkout_to = sys.argv[1]
assert os.path.isdir(checkout_to)

project_dir = os.path.join(checkout_to, context['system_project_slug'])
shutil.rmtree(project_dir, ignore_errors=True)

from unittest import mock
from xproject.loaders import Jinja2OverrideFileSystemLoader as MockFileSystemLoader


with mock.patch('cookiecutter.generate.FileSystemLoader',
                new_callable=lambda: MockFileSystemLoader):
    cookiecutter(template=cur_cc, checkout=checkout_to,
                 no_input=True,
                 extra_context=context)
