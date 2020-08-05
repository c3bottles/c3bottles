from flask import Blueprint, abort, render_template, flash, redirect, url_for, request
from flask_babel import lazy_gettext
from flask_login import current_user

from c3bottles import db, bcrypt
from c3bottles.model.user import User, make_secure_token
from c3bottles.views import not_found, unauthorized, needs_admin
from c3bottles.views.forms import (
    UserIdForm,
    PermissionsForm,
    PasswordForm,
    UserCreateForm,
)


bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.before_request
@needs_admin
def check_for_admin():
    pass


@bp.app_errorhandler(404)
def handle_404(e):
    if request.path.startswith(bp.url_prefix) and not current_user.is_admin:
        return unauthorized(e)
    else:
        return not_found(e)


@bp.route("/")
def index():
    return render_template(
        "admin/index.html",
        users=User.all(),
        user_id_form=UserIdForm(),
        permissions_form=PermissionsForm(),
        password_form=PasswordForm(),
        user_create_form=UserCreateForm(),
    )


@bp.route("/disable_user", methods=("POST",))
def disable_user():
    form = UserIdForm()
    if not form.validate_on_submit():
        abort(400)
    user = User.get_or_404(form.user_id.data)
    user.is_active = False
    user.token = make_secure_token()
    db.session.add(user)
    db.session.commit()
    flash(
        {"class": "success", "text": lazy_gettext("The user has been disabled successfully."),}
    )
    return redirect(url_for("admin.index"))


@bp.route("/enable_user", methods=("POST",))
def enable_user():
    form = UserIdForm()
    if not form.validate_on_submit():
        abort(400)
    user = User.get_or_404(form.user_id.data)
    user.is_active = True
    db.session.add(user)
    db.session.commit()
    flash(
        {"class": "success", "text": lazy_gettext("The user has been enabled successfully."),}
    )
    return redirect(url_for("admin.index"))


@bp.route("/user_permissions", methods=("POST",))
def user_permissions():
    form = PermissionsForm()
    if not form.validate_on_submit():
        abort(400)
    user = User.get_or_404(form.user_id.data)
    user.can_visit = form.can_visit.data
    user.can_edit = form.can_edit.data
    user.is_admin = form.is_admin.data
    db.session.add(user)
    db.session.commit()
    flash(
        {
            "class": "success",
            "text": lazy_gettext("The user's permissions have been updated successfully."),
        }
    )
    return redirect(url_for("admin.index"))


@bp.route("/user_password", methods=("POST",))
def user_password():
    form = PasswordForm()
    if not form.validate_on_submit():
        abort(400)
    user = User.get_or_404(form.user_id.data)
    if form.password_1.data == form.password_2.data:
        user.password = bcrypt.generate_password_hash(form.password_1.data)
        user.token = make_secure_token()
        db.session.add(user)
        db.session.commit()
        flash(
            {
                "class": "success",
                "text": lazy_gettext("The user's password has been changed successfully"),
            }
        )
        if user == current_user:
            return redirect(url_for("main.index"))
        else:
            return redirect(url_for("admin.index"))
    else:
        flash({"class": "danger", "text": lazy_gettext("The passwords do not match.")})
        return redirect(url_for("admin.index"))


@bp.route("/delete_user", methods=("POST",))
def delete_user():
    form = UserIdForm()
    if not form.validate_on_submit():
        abort(400)
    user = User.get_or_404(form.user_id.data)
    db.session.delete(user)
    db.session.commit()
    flash(
        {"class": "success", "text": lazy_gettext("The user has been deleted successfully."),}
    )
    return redirect(url_for("admin.index"))


@bp.route("/create_user", methods=("POST",))
def create_user():
    form = UserCreateForm()
    if not form.validate_on_submit():
        abort(400)
    if User.get(form.username.data) is not None:
        flash(
            {"class": "danger", "text": lazy_gettext("A user with this name already exists"),}
        )
        return redirect(url_for("admin.index"))
    else:
        user = User(
            form.username.data,
            form.password.data,
            form.can_visit.data,
            form.can_edit.data,
            form.is_admin.data,
            False,
        )
        db.session.add(user)
        db.session.commit()
        flash(
            {
                "class": "success",
                "text": lazy_gettext("The new user has been created successfully."),
            }
        )
        return redirect(url_for("admin.index"))
