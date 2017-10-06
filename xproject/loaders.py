import ast

from jinja2 import FileSystemLoader


def _escape_backslashes(data, jinja_env):
    """Double backslashes within jinja2 expressions

    A user may enter something like this in a playbook::

      debug:
        msg: "Test Case 1\\3; {{ test1_name | regex_replace('^(.*)_name$', '\\1')}}"

    The string inside of the {{ gets interpreted multiple times First by yaml.
    Then by python.  And finally by jinja2 as part of it's variable.  Because
    it is processed by both python and jinja2, the backslash escaped
    characters get unescaped twice.  This means that we'd normally have to use
    four backslashes to escape that.  This is painful for playbook authors as
    they have to remember different rules for inside vs outside of a jinja2
    expression (The backslashes outside of the "{{ }}" only get processed by
    yaml and python.  So they only need to be escaped once).  The following
    code fixes this by automatically performing the extra quoting of
    backslashes inside of a jinja2 expression.

    """
    if '\\' in data and '{{' in data:
        new_data = []
        d2 = jinja_env.preprocess(data)
        in_var = False

        for token in jinja_env.lex(d2):
            if token[1] == 'variable_begin':
                in_var = True
                new_data.append(token[2])
            elif token[1] == 'variable_end':
                in_var = False
                new_data.append(token[2])
            elif in_var and token[1] == 'string':
                # Double backslashes only if we're inside of a jinja2 variable
                new_data.append(token[2].replace('\\', '\\\\'))
            else:
                new_data.append(token[2])

        data = ''.join(new_data)

    return data


JINJA2_OVERRIDE = '#jinja2:'


class Jinja2OverrideFileSystemLoader(FileSystemLoader):

    def overlay_source_environment(self, source, environment):
        myenv = environment.overlay()
        if source.startswith(JINJA2_OVERRIDE):
            eol = source.find('\n')
            line = source[len(JINJA2_OVERRIDE):eol]
            source = source[eol + 1:]
            for pair in line.split(','):
                (key, val) = pair.split(':')
                key = key.strip()
                setattr(myenv, key, ast.literal_eval(val.strip()))

        myenv.filters.update(environment.filters.copy())
        myenv.tests.update(environment.tests.copy())
        _escape_backslashes(source, myenv)
        return source, myenv

    def load(self, environment, name, globals=None):
        """Loads a template.  This method looks up the template in the cache
        or loads one by calling :meth:`get_source`.  Subclasses should not
        override this method as loaders working on collections of other
        loaders (such as :class:`PrefixLoader` or :class:`ChoiceLoader`)
        will not call this method but `get_source` directly.
        """
        code = None
        if globals is None:
            globals = {}

        # first we try to get the source for this template together
        # with the filename and the uptodate function.
        source, filename, uptodate = self.get_source(environment, name)

        source, environment = self.overlay_source_environment(
            source=source, environment=environment)

        # try to load the code from the bytecode cache if there is a
        # bytecode cache configured.
        bcc = environment.bytecode_cache
        if bcc is not None:
            bucket = bcc.get_bucket(environment, name, filename, source)
            code = bucket.code

        # if we don't have code so far (not cached, no longer up to
        # date) etc. we compile the template
        if code is None:
            code = environment.compile(source, name, filename)

        # if the bytecode cache is available and the bucket doesn't
        # have a code so far, we give the bucket the new code and put
        # it back to the bytecode cache.
        if bcc is not None and bucket.code is None:
            bucket.code = code
            bcc.set_bucket(bucket)

        return environment.template_class.from_code(environment, code,
                                                    globals, uptodate)


