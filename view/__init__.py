from datetime import datetime
from flask import render_template, g
from flask.ext.login import current_user

from controller import c3bottles
from model.forms import LoginForm

@c3bottles.before_request
def before_request():
    g.login_form = LoginForm()
    g.user = current_user
    g.now = datetime.now()


@c3bottles.errorhandler(401)
def unauthorized(e):
    return render_template(
        "error.html",
        heading="Unauthorized!",
        text="You do not have permission to view this page."
    ), 401


@c3bottles.errorhandler(404)
def not_found(e):
    return render_template(
        "error.html",
        heading="Not found",
        text="The requested URL was not found on the server."
    ), 404

# vim: set expandtab ts=4 sw=4:
