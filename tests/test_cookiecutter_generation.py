import os
import re

import pytest
import sh
from binaryornot.check import is_binary

PATTERN = '{{(\s?cookiecutter)[.](.*?)}}'
RE_OBJ = re.compile(PATTERN)


@pytest.fixture
def context():
    return {
        "system_name": "Xingzhe",
        "system_slug":  "xingzhe",
        "project_name": "Workout",
        "project_slug": "workout",
        "system_project_slug": "xingzhe_workout",
        "system_project_name": "Xingzhe Workout",
        "author_name": "Ranger.Huang",
        "email": "ranger.huang@bi-ci.com",
        "description": "A short description of the project.",
        "domain_name": "workout.xingzhe.com",
        "version": "0.1.0",
        "timezone": "UTC",
        "use_pycharm": "y",
        "use_cas": "n",
        "use_mailhog": "n",
        "use_celery": "n",
        "use_docker": "y",
        "use_compressor": "n",
        "postgresql_version": "9.6",
        "mysql_version": "5.6",

        "use_postgresql": "n",
        "use_postgresql_alias": "db2",
        "use_mysql": "n",
        "use_mysql_alias": "default",

        "release_date": "{% now 'local' %}",
        "_extensions": ["jinja2_time.TimeExtension"],
        "_copy_without_render": [
            "playbook/*"
        ]
    }


def build_files_list(root_dir):
    """Build a list containing absolute paths to the generated files."""
    return [
        os.path.join(dirpath, file_path)
        for dirpath, subdirs, files in os.walk(root_dir)
        for file_path in files
    ]


def check_paths(paths):
    """Method to check all paths have correct substitutions,
    used by other tests cases
    """
    # Assert that no match is found in any of the files
    for path in paths:
        if is_binary(path):
            continue
        for line in open(path, 'r'):
            match = RE_OBJ.search(line)
            msg = 'cookiecutter variable not replaced in {}'
            assert match is None, msg.format(path)


def test_default_configuration(cookies, context):
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0, str(result.exception)
    assert result.exception is None
    assert result.project.basename == context['system_project_slug']
    assert result.project.isdir()
    print(result)

    paths = build_files_list(str(result.project))
    assert paths
    check_paths(paths)


@pytest.mark.skip
def test_flake8_compliance(cookies, context):
    """generated project should pass flake8"""
    result = cookies.bake(extra_context=context)

    import io
    out = io.StringIO()
    try:
        sh.flake8(str(result.project), _err_to_out=True, _out=out)
    except sh.ErrorReturnCode as e:
        pytest.fail(out)
        pytest.fail(e)
