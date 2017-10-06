system_project_slug = '{{ cookiecutter.system_project_slug }}'

if hasattr(system_project_slug, 'isidentifier'):
    assert system_project_slug.isidentifier(), 'System Project slug should be valid Python identifier!'

system_project_id = '{{ cookiecutter.system_project_id }}'
try:
    int(system_project_id)
except:
    assert False, 'invalid system_project_id'
