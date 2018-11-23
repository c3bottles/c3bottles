from flask import render_template, request, g, abort, url_for
from flask_babel import lazy_gettext
from flask_login import login_required

from .. import c3bottles, db

from ..model.drop_point import DropPoint
from ..model.visit import Visit


@c3bottles.route("/visit", methods=("GET", "POST"))
@c3bottles.route("/visit/<int:number>")
@login_required
def visit(number=None):
    if number:
        dp = DropPoint.get(number)
    else:
        dp = DropPoint.get(request.values.get("number"))

    if not dp or dp.removed:
        return render_template(
            "error.html",
            heading=lazy_gettext("Error!"),
            text=lazy_gettext("Point not found."),
        )

    action = request.values.get("maintenance")

    if action:
        if g.user.is_anonymous:
            abort(401)
        try:
            Visit(dp=dp, action=action)
        except ValueError as e:
            return render_template(
                "error.html",
                text=lazy_gettext("Errors occurred while processing your visit:"),
                errors=[v for d in e.args for v in d.values()]
            )
        else:
            db.session.commit()
            return render_template(
                "success.html",
                heading=lazy_Gettext("Thank you!"),
                text=lazy_gettext("Your visit has been processed successfully."),
                back="{}#{}/{}/{}/3".format(url_for("dp_map"), dp.level, dp.lat, dp.lng)
            )
    else:
        return render_template(
            "visit.html",
            dp=dp,
        )
