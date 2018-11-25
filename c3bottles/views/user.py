from werkzeug.routing import BuildError
from json import loads
from re import sub

from flask import render_template, url_for, redirect, request, g

from flask_babel import lazy_gettext as _
from flask_login import login_user, logout_user

from .. import c3bottles

from ..model.forms import LoginForm
from ..model.user import User


@c3bottles.route("/login", methods=("POST", "GET"))
def login():
    if request.method == "GET":
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            back = redirect(
                url_for(
                    form.back.data,
                    **loads(sub("( u)?'", "\"", form.args.data))
                )
            )
        except (BuildError, ValueError):
            back = redirect(url_for("index"))
        if g.user and g.user.is_authenticated:
            return back
        user = User.get(form.username.data)
        if user and user.is_active and user.validate_password(form.password.data):
            login_user(user, remember=True)
            return back
    return render_template(
        "error.html",
        heading=_("Login failed!"),
        text=_("Wrong user name or password."),
        back=form.back.data,
        args=form.args.data
    )


@c3bottles.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
