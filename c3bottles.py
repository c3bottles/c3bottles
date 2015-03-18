#!/usr/bin/python

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

c3bottles = Flask(__name__)
c3bottles.config.from_object("config")

db = SQLAlchemy(c3bottles)

# Trim blocks in jinja2 so no unnecessary newlines appear in the output:
c3bottles.jinja_env.trim_blocks = True

from view import *

if __name__ == "__main__":
	c3bottles.run(debug=True)
