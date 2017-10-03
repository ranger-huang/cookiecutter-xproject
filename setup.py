#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

setup_requirements = [
    'pytest-runner',
    # TODO(killuavx): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='cookiecutter-xingzhe-django',
    version='0.1.0',
    description="A Cookiecutter template for creating Xingzhe Django projects quickly.",
    long_description=readme + '\n\n' + history,
    author="Ranger.Huang",
    author_email='ranger_huang@yeah.net',
    url='https://github.com/killuavx/cookiecutter-xingzhe-django',
    packages=find_packages(include=['cookiecutter-xingzhe-django']),
    entry_points={
        'console_scripts': [
            'create_project_xdj=xproject.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='cookiecutter-xingzhe-django',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 1 - Pre-Alpha',
        'Environment :: Console',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',

    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
