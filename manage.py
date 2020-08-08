#!/usr/bin/env python3
"""
Managing script for c3bottles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This script can be used to manage the c3bottles installation. It is able to
perform tasks like initializing the database, creating users or running the
development web server.

When using this script, you should make sure that the right Python interpreter
is used. When calling this script from the shell without a virtual environment
as `./manage.py`, you need to have all dependencies installed in the
environment or your system's default Python interpreter. To use this script
in a virtual environment, either activate the virtual environment first
or call it like `venv/bin/python manage.py`.
"""
import os

import click
from flask.cli import FlaskGroup
from werkzeug.middleware.profiler import ProfilerMiddleware

from c3bottles import app

os.environ["FLASK_ENV"] = "development"


@click.group(cls=FlaskGroup, create_app=lambda _: app)
def cli():
    pass


@app.cli.command()
def initdb():
    """
    Initializes the database.

    This creates all database tables if they do not exist already.
    """
    from c3bottles import db

    db.create_all()


@app.cli.command()
def dropdb():
    """
    Removes the database.

    This removes everything from the database.
    """
    from c3bottles import db

    if click.confirm("This deletes everything from the database!"):
        db.drop_all()


@app.cli.command()
@click.option("--host", "-h", help="The interface to bind to.", default="127.0.0.1")
@click.option("--port", "-p", help="The port to bind to.", default=5000)
def serve(host, port):
    """
    Runs a development server.
    """
    os.environ["FLASK_RUN_FROM_CLI"] = "false"
    app.jinja_env.auto_reload = True
    app.run(debug=True, host=host, port=port)


@app.cli.command()
@click.option("--host", "-h", help="The interface to bind to.", default="127.0.0.1")
@click.option("--port", "-p", help="The port to bind to.", default=5000)
def profile(host, port):
    """
    Runs a development server with profiling.

    This is similar to the 'serve' command. It adds werkzeug's profiler
    middleware to facilitate easy profiling of the application.
    """
    app.jinja_env.auto_reload = True
    app.config["PROFILE"] = True
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    app.run(debug=True, host=host, port=port)


if __name__ == "__main__":
    cli()
