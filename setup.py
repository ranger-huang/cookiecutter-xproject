#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as rfile:
    requirements = rfile.readlines()

requirements = [
    'Click>=6.0',
    'cookiecutter',
] + requirements

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

setup(
    name='cookiecutter-xproject',
    version='0.1.0',
    description="A Cookiecutter template for creating XProject quickly.",
    long_description=readme + '\n\n' + history,
    author="Ranger.Huang",
    author_email='ranger_huang@yeah.net',
    url='https://github.com/ranger-huang/cookiecutter-xproject',
    packages=find_packages(include=['cookiecutter-xproject', 'xproject'],
                           #exclude=['.*']
                           ),
    entry_points={
        'console_scripts': [
            'xproject=xproject.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='cookiecutter-xproject',
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',

    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
