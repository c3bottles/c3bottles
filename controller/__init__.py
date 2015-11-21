#!/usr/bin/python

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

c3bottles = Flask(__name__,
    static_folder="../static",
    template_folder="../templates"
)

def load_config():
    c3bottles.config.from_object("config")

db = SQLAlchemy(c3bottles)

lm = LoginManager(c3bottles)

# Trim and strip blocks in jinja2 so no unnecessary
# newlines and tabs appear in the output:
c3bottles.jinja_env.trim_blocks = True
c3bottles.jinja_env.lstrip_blocks = True

from view.legacy import *
from view.api import api
from view.statistics import stats
c3bottles.register_blueprint(api)
c3bottles.register_blueprint(stats)

# vim: set expandtab ts=4 sw=4:
