from datetime import datetime
from functools import wraps

from flask import render_template, g, request, Response, get_flashed_messages, abort
from flask_login import current_user

from .. import c3bottles
from ..model.forms import LoginForm


@c3bottles.before_request
def before_request():
    g.alerts = get_flashed_messages()
    g.login_form = LoginForm()
    g.now = datetime.now()


def needs_reporting(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.can_report:
            return func(*args, **kwargs)
        else:
            abort(401)
    return decorated_view


def needs_visiting(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.can_visit:
            return func(*args, **kwargs)
        else:
            abort(401)
    return decorated_view


def needs_editing(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.can_edit:
            return func(*args, **kwargs)
        else:
            abort(401)
    return decorated_view


def needs_admin(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_admin:
            return func(*args, **kwargs)
        else:
            abort(401)
    return decorated_view


@c3bottles.errorhandler(400)
def bad_request(_):
    before_request()
    if request.path == "/api":
        return Response(
            "[{\"e\": \"API request failed.\"}]",
            mimetype="application/json",
            status=400)
    return render_template(
        "error.html",
        heading="Bad request",
        text="Your browser sent an invalid request."
    ), 400


@c3bottles.errorhandler(401)
def unauthorized(_):
    return render_template(
        "error.html",
        heading="Unauthorized",
        text="You do not have permission to view this page."
    ), 401


@c3bottles.errorhandler(404)
def not_found(_):
    return render_template(
        "error.html",
        heading="Not found",
        text="The requested URL was not found on the server."
    ), 404
