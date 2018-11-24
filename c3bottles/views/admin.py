from flask import Blueprint, abort, render_template
from flask_login import current_user


admin = Blueprint("admin", __name__, url_prefix="/admin")


def check_for_admin():
    if current_user.is_admin:
        pass
    else:
        abort(401)


admin.before_request(check_for_admin)


@admin.route("/")
def index():
    return render_template("admin.html")
