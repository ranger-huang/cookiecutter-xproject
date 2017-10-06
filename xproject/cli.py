# -*- coding: utf-8 -*-

"""Console script for cookiecutter_xingzhe_django."""

def main():
    from cookiecutter.__main__ import main as cmain
    from unittest import mock
    from xproject.loaders import Jinja2OverrideFileSystemLoader as MockFileSystemLoader
    with mock.patch('cookiecutter.generate.FileSystemLoader',
                    new_callable=lambda: MockFileSystemLoader):
        cmain(prog_name="xproject")

if __name__ == "__main__":
    main()
