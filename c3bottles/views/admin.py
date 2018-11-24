from flask import Blueprint, abort, render_template
from flask_babel import lazy_gettext
from flask_login import current_user

from . import not_found, unauthorized
from .. import db
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
        users=User.all()
    )


@admin.route("/delete_user/<string:user_id>")
def delete_user(user_id):
    try:
        user = User.get(int(user_id))
    except (TypeError, ValueError):
        abort(404)
    else:
        if user is None:
            abort(404)
        else:
            db.session.delete(user)
            db.session.commit()
            return render_template(
                "admin.html",
                users=User.all(),
                message=("success", lazy_gettext("The user has been deleted successfully."))
            )
