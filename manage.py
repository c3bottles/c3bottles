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
import click

from flask.cli import FlaskGroup
from werkzeug.contrib.profiler import ProfilerMiddleware

from c3bottles import c3bottles


@click.group(cls=FlaskGroup, create_app=lambda _: c3bottles)
def cli():
    pass


@c3bottles.cli.command()
def initdb():
    """
    Initializes the database.

    This creates all database tables if they do not exist already.
    """
    from c3bottles import db
    db.create_all()


@c3bottles.cli.command()
def dropdp():
    """
    Removes the database.

    This removes everything from the database.
    """
    from c3bottles import db
    with click.confirm("This deletes everything from the database!"):
        db.drop_all()


@c3bottles.cli.command()
@click.option(
    "--host", "-h",
    help="The interface to bind to.", default="127.0.0.1"
)
@click.option(
    "--port", "-p",
    help="The port to bind to.", default=5000
)
def profile(host, port):
    """
    Runs a development server with profiling.

    This is similar to the run command. It adds werkzeug's profiler
    middleware to facilitate easy profiling of the application.
    """
    c3bottles.config["PROFILE"] = True
    c3bottles.wsgi_app = ProfilerMiddleware(
        c3bottles.wsgi_app, restrictions=[30]
    )
    c3bottles.run(debug=True, host=host, port=port)


@c3bottles.cli.command()
def pytest():
    """
    Runs the tests.
    """
    import pytest
    pytest.main(["test"])


if __name__ == '__main__':
    cli()
