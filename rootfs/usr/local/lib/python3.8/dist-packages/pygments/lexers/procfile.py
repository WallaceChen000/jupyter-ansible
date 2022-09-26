"""
    pygments.lexers.procfile
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexer for Procfile file format.

    :copyright: Copyright 2006-2022 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups
from pygments.token import Name, Number, String, Text, Punctuation

__all__ = ["ProcfileLexer"]


class ProcfileLexer(RegexLexer):
    """
    Lexer for Procfile file format.

    The format is used to run processes on Heroku or is used by Foreman or
    Honcho tools.

    .. versionadded:: 2.10
    """
    name = 'Procfile'
    url = 'https://devcenter.heroku.com/articles/procfile#procfile-format'
    aliases = ['procfile']
    filenames = ['Procfile']

    tokens = {
        'root': [
            (r'^([a-z]+)(:)', bygroups(Name.Label, Punctuation)),
            (r'\s+', Text.Whitespace),
            (r'"[^"]*"', String),
            (r"'[^']*'", String),
            (r'[0-9]+', Number.Integer),
            (r'\$[a-zA-Z_][\w]*', Name.Variable),
            (r'(\w+)(=)(\w+)', bygroups(Name.Variable, Punctuation, String)),
            (r'([\w\-\./]+)', Text),
        ],
    }
