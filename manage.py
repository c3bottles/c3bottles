#!/usr/bin/env/python3

import click

from flask.cli import FlaskGroup
from werkzeug.contrib.profiler import ProfilerMiddleware

from c3bottles import c3bottles


def create_app(*args):
    return c3bottles


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass


@c3bottles.cli.command()
def initdb():
    """Initialize the database."""
    from c3bottles import db
    db.create_all()


@c3bottles.cli.command()
@click.option(
    "--name", prompt="User name"
)
@click.option(
    "--password", prompt=True, hide_input=True, confirmation_prompt=True
)
@click.option(
    "--can-visit", prompt="Can the user visit drop points?", is_flag=True
)
@click.option(
    "--can-edit", prompt="Can the user edit drop points?", is_flag=True
)
@click.option(
    "--admin", prompt="Is the user an administrator?", is_flag=True
)
@click.option(
    "--active", prompt="Is the user active?", is_flag=True, default=True
)
def createuser(name, password, can_visit, can_edit, admin, active):
    """Create a new user."""
    from c3bottles import db
    from c3bottles.model.user import User
    if User.get(name):
        print("A user with the name %s already exists!" % name)
        return
    user = User(name, password, can_visit, can_edit, admin, active)
    db.session.add(user)
    db.session.commit()
    print("User created successfully.")


@c3bottles.cli.command()
def profile():
    """Run a development server with profiling."""
    c3bottles.config["PROFILE"] = True
    c3bottles.wsgi_app = ProfilerMiddleware(
        c3bottles.wsgi_app, restrictions=[30]
    )
    c3bottles.run(debug=True)


if __name__ == '__main__':
    cli()
