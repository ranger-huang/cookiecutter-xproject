"""
Does the following:

1. Generates and saves random secret key
2. Removes the taskapp if celery isn't going to be used
3. Removes the .idea directory if PyCharm isn't going to be used
4. Copy files from /docs/ to {{ cookiecutter.system_project_slug }}/docs/

"""
from __future__ import print_function

import os
import random
import shutil
import string

# Get the root project directory

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

# Use the system PRNG if possible
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False


def get_random_string(length=50):
    """
    Returns a securely generated random string.
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    punctuation = string.punctuation.replace('"', '').replace("'", '')
    punctuation = punctuation.replace('\\', '')
    if using_sysrandom:
        return ''.join(random.choice(
            string.digits + string.ascii_letters + punctuation
        ) for i in range(length))

    print(
        "Cookiecutter Django couldn't find a secure pseudo-random number generator on your system."
        " Please change change your SECRET_KEY variables in conf/settings/local.py and env.example"
        " manually."
    )
    return "CHANGEME!!!"


def set_secret_key(setting_file_location):
    # Open locals.py
    if not os.path.exists(setting_file_location):
        import sh
        content = sh.cat(setting_file_location)
        print('#' * 100)
        print(content)
        print('#' * 100)

    with open(setting_file_location) as f:
        file_ = f.read()

    # Generate a SECRET_KEY that matches the Django standard
    SECRET_KEY = get_random_string()

    # Replace "CHANGEME!!!" with SECRET_KEY
    file_ = file_.replace('CHANGEME!!!', SECRET_KEY, 1)

    # Write the results to the locals.py module
    with open(setting_file_location, 'w') as f:
        f.write(file_)


def make_secret_key(project_directory):
    """Generates and saves random secret key"""
    # Determine the local_setting_file_location

    # local.py settings file

    for env_name in ['test', 'local', 'production']:
        setting_file = os.path.join(
            project_directory,
            '{{cookiecutter.system_slug}}_conf/settings/%s.py' % env_name
        )
        set_secret_key(setting_file)

        env_file = os.path.join(
            project_directory,
            '{{cookiecutter.system_slug}}_conf/%s.env' %env_name,
        )
        # env.example file
        set_secret_key(env_file)


def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


def remove_task_app(project_directory):
    """Removes the taskapp if celery isn't going to be used"""
    # Determine the local_setting_file_location
    task_app_location = os.path.join(
        PROJECT_DIRECTORY,
        '{{cookiecutter.system_project_slug}}/taskapp'
    )
    shutil.rmtree(task_app_location)


def remove_pycharm_dir(project_directory):
    """
    Removes directories related to PyCharm
    if it isn't going to be used
    """
    idea_dir_location = os.path.join(PROJECT_DIRECTORY, '.idea/')
    if os.path.exists(idea_dir_location):
        shutil.rmtree(idea_dir_location)

    docs_dir_location = os.path.join(PROJECT_DIRECTORY, 'docs/pycharm/')
    if os.path.exists(docs_dir_location):
        shutil.rmtree(docs_dir_location)


def remove_docker_files():
    """
    Removes files needed for docker if it isn't going to be used
    """
    for filename in [".env", ".dockerignore"]:
        os.remove(os.path.join(
            PROJECT_DIRECTORY, filename
        ))

    shutil.rmtree(os.path.join(
        PROJECT_DIRECTORY, "compose"
    ))


def remove_postgresql_files():
    """
    Removes files needed for postgresql if it isn't going to be used
    """
    shutil.rmtree(os.path.join(
        PROJECT_DIRECTORY, "compose", "postgres"
    ), ignore_errors=True)


def remove_mysql_files():
    """
    Removes files needed for mysql if it isn't going to be used
    """
    shutil.rmtree(os.path.join(
        PROJECT_DIRECTORY, "compose", "mysql"
    ), ignore_errors=True)

# 1. Generates and saves random secret key
make_secret_key(PROJECT_DIRECTORY)

# 2. Removes the taskapp if celery isn't going to be used
if '{{ cookiecutter.use_celery }}'.lower() == 'n':
    remove_task_app(PROJECT_DIRECTORY)

# 3. Removes the .idea directory if PyCharm isn't going to be used
if '{{ cookiecutter.use_pycharm }}'.lower() != 'y':
    remove_pycharm_dir(PROJECT_DIRECTORY)

if '{{ cookiecutter.use_docker }}'.lower() != 'y':
    remove_docker_files()

if '{{ cookiecutter.use_mysql }}'.lower() != 'y':
    remove_mysql_files()

if '{{ cookiecutter.use_postgresql }}'.lower() != 'y':
    remove_postgresql_files()
