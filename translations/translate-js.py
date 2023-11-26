#!/usr/bin/env python3

import os

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
os.sys.path.insert(0, parent)

from markupsafe import Markup

from flask import render_template
from flask_babel import force_locale

from c3bottles import app, languages

_js_escapes = {
    '\\': '\\u005C',
    '\'': '\\u0027',
    '"': '\\u0022',
    '>': '\\u003E',
    '<': '\\u003C',
    '&': '\\u0026',
    '=': '\\u003D',
    '-': '\\u002D',
    ';': '\\u003B',
    u'\u2028': '\\u2028',
    u'\u2029': '\\u2029'
}


def escapejs(value):
    retval = []
    for letter in value:
        if letter in _js_escapes:
            retval.append(_js_escapes[letter])
        else:
            retval.append(letter)
    return Markup("".join(retval))


app.jinja_env.filters["escapejs"] = escapejs


for l in languages:
    with app.app_context(), force_locale(l), \
         open("{}/static/lib/js/{}.js".format(parent, l), "w") as f:

        f.write(render_template("js/l10n.js", lang=l))

        print("updated JS translations in {}".format(os.path.relpath(f.name)))
