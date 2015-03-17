#!/usr/bin/python

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

c3bottles = Flask(__name__)
c3bottles.config.from_object("config")

db = SQLAlchemy(c3bottles)

@c3bottles.route("/")
def index():
	return "Hello, world!"

if __name__ == "__main__":
	c3bottles.run(debug=True)
