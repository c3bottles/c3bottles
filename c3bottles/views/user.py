from json import loads
from re import sub

from flask import render_template, url_for, redirect, request, Blueprint
from flask_babel import lazy_gettext
from flask_login import current_user, login_user, logout_user
from werkzeug.routing import BuildError

from c3bottles.model.user import User
from c3bottles.views.forms import LoginForm


bp = Blueprint("user", __name__)


@bp.route("/login", methods=("POST", "GET"))
def login():
    if request.method == "GET":
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            back = redirect(url_for(form.back.data, **loads(sub("( u)?'", '"', form.args.data))))
        except (BuildError, ValueError):
            back = redirect(url_for("main.index"))
        if current_user.is_authenticated:
            return back
        user = User.get(form.username.data)
        if user and user.is_active and user.validate_password(form.password.data):
            login_user(user, remember=True)
            return back
    return render_template(
        "error.html",
        heading=lazy_gettext("Login failed!"),
        text=lazy_gettext("Wrong user name or password."),
        back=form.back.data,
        args=form.args.data,
    )


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
