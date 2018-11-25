from flask import Blueprint, abort, render_template, flash, redirect, url_for
from flask_babel import lazy_gettext
from flask_login import current_user

from . import not_found, unauthorized
from .. import db
from ..model.forms import DeleteUserForm
from ..model.user import User


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
        delete_form=DeleteUserForm()
    )


@admin.route("/delete_user", methods=("POST",))
def delete_user():
    form = DeleteUserForm()
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
