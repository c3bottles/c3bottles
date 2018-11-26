from flask import Blueprint, abort, render_template, flash, redirect, url_for
from flask_babel import lazy_gettext
from flask_login import current_user

from . import not_found, unauthorized
from .. import db, bcrypt
from ..model.forms import UserIdForm, PermissionsForm, PasswordForm, UserCreateForm
from ..model.user import User, make_secure_token


admin = Blueprint("admin", __name__, url_prefix="/admin")


def check_for_admin():
    if current_user.is_admin:
        pass
    else:
        abort(401)


admin.before_request(check_for_admin)


@admin.app_errorhandler(404)
def handle_404(_):
    if current_user.is_admin:
        return not_found(_)
    else:
        return unauthorized(_)


@admin.route("/")
def index():
    return render_template(
        "admin.html",
        users=User.all(),
        user_id_form=UserIdForm(),
        permissions_form=PermissionsForm(),
        password_form=PasswordForm(),
        user_create_form=UserCreateForm(),
    )


@admin.route("/disable_user", methods=("POST",))
def disable_user():
    form = UserIdForm()
    if form.validate_on_submit():
        user = User.get(form.user_id.data)
        if user is None:
            abort(404)
        else:
            user.is_active = False
            user.token = make_secure_token()
            db.session.add(user)
            db.session.commit()
            flash({
                "class": "success",
                "text": lazy_gettext("The user has been disabled successfully.")
            })
            return redirect(url_for("admin.index"))
    else:
        abort(400)


@admin.route("/enable_user", methods=("POST",))
def enable_user():
    form = UserIdForm()
    if form.validate_on_submit():
        user = User.get(form.user_id.data)
        if user is None:
            abort(404)
        else:
            user.is_active = True
            db.session.add(user)
            db.session.commit()
            flash({
                "class": "success",
                "text": lazy_gettext("The user has been enabled successfully.")
            })
            return redirect(url_for("admin.index"))
    else:
        abort(400)


@admin.route("/user_permissions", methods=("POST",))
def user_permissions():
    form = PermissionsForm()
    if form.validate_on_submit():
        user = User.get(form.user_id.data)
        if user is None:
            abort(404)
        else:
            user.can_visit = form.can_visit.data
            user.can_edit = form.can_edit.data
            user.is_admin = form.is_admin.data
            db.session.add(user)
            db.session.commit()
            flash({
                "class": "success",
                "text": lazy_gettext("The user's permissions have been updated successfully.")
            })
            return redirect(url_for("admin.index"))
    else:
        abort(400)


@admin.route("/user_password", methods=("POST",))
def user_password():
    form = PasswordForm()
    if form.validate_on_submit():
        user = User.get(form.user_id.data)
        if user is None:
            abort(404)
        else:
            if form.password_1.data == form.password_2.data:
                user.password = bcrypt.generate_password_hash(form.password_1.data)
                user.token = make_secure_token()
                db.session.add(user)
                db.session.commit()
                flash({
                    "class": "success",
                    "text": lazy_gettext("The user's password has been changed successfully")
                })
                if user == current_user:
                    return redirect(url_for("index"))
                else:
                    return redirect(url_for("admin.index"))
            else:
                flash({
                    "class": "danger",
                    "text": lazy_gettext("The passwords do not match.")
                })
                return redirect(url_for("admin.index"))
    else:
        abort(400)


@admin.route("/delete_user", methods=("POST",))
def delete_user():
    form = UserIdForm()
    if form.validate_on_submit():
        user = User.get(form.user_id.data)
        if user is None:
            abort(404)
        else:
            db.session.delete(user)
            db.session.commit()
            flash({
                "class": "success",
                "text": lazy_gettext("The user has been deleted successfully.")
            })
            return redirect(url_for("admin.index"))
    else:
        abort(400)


@admin.route("/create_user", methods=("POST",))
def create_user():
    form = UserCreateForm()
    if form.validate_on_submit():
        if User.get(form.username.data) is not None:
            flash({
                "class": "danger",
                "text": lazy_gettext("A user with this name already exists")
            })
            return redirect(url_for("admin.index"))
        else:
            user = User(
                form.username.data, form.password.data, form.can_visit.data, form.can_edit.data, form.is_admin.data,
                False
            )
            db.session.add(user)
            db.session.commit()
            flash({
                "class": "success",
                "text": lazy_gettext("The new user has been created successfully.")
            })
            return redirect(url_for("admin.index"))
    else:
        abort(400)
