from datetime import datetime

from flask import render_template, g, request, Response, get_flashed_messages
from flask_login import current_user

from .. import c3bottles

from ..model.forms import LoginForm


@c3bottles.before_request
def before_request():
    g.alerts = get_flashed_messages()
    g.login_form = LoginForm()
    g.user = current_user
    g.now = datetime.now()
    g.no_anonymous_reporting = \
        c3bottles.config.get("NO_ANONYMOUS_REPORTING", False)


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
