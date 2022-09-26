"""
    pygments.styles.native
    ~~~~~~~~~~~~~~~~~~~~~~

    pygments version of my "native" vim theme.

    :copyright: Copyright 2006-2022 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Token, Whitespace


class NativeStyle(Style):
    """
    Pygments version of the "native" vim theme.
    """

    background_color = '#202020'
    highlight_color = '#404040'
    line_number_color = '#aaaaaa'

    styles = {
        Token:              '#d0d0d0',
        Whitespace:         '#666666',

        Comment:            'italic #ababab',
        Comment.Preproc:    'noitalic bold #cd2828',
        Comment.Special:    'noitalic bold #e50808 bg:#520000',

        Keyword:            'bold #6ebf26',
        Keyword.Pseudo:     'nobold',
        Operator.Word:      'bold #6ebf26',

        String:             '#ed9d13',
        String.Other:       '#ffa500',

        Number:             '#51b2fd',

        Name.Builtin:       '#2fbccd',
        Name.Variable:      '#40ffff',
        Name.Constant:      '#40ffff',
        Name.Class:         'underline #71adff',
        Name.Function:      '#71adff',
        Name.Namespace:     'underline #71adff',
        Name.Exception:     '#bbbbbb',
        Name.Tag:           'bold #6ebf26',
        Name.Attribute:     '#bbbbbb',
        Name.Decorator:     '#ffa500',

        Generic.Heading:    'bold #ffffff',
        Generic.Subheading: 'underline #ffffff',
        Generic.Deleted:    '#d22323',
        Generic.Inserted:   '#589819',
        Generic.Error:      '#d22323',
        Generic.Emph:       'italic',
        Generic.Strong:     'bold',
        Generic.Prompt:     '#aaaaaa',
        Generic.Output:     '#cccccc',
        Generic.Traceback:  '#d22323',

        Error:              'bg:#e3d2d2 #a61717'
    }
