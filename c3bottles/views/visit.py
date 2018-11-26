from flask import render_template, request, url_for, abort, flash, redirect
from flask_babel import lazy_gettext

from .. import c3bottles, db
from ..model.drop_point import DropPoint
from ..model.visit import Visit
from . import needs_visiting


@c3bottles.route("/visit", methods=("GET", "POST"))
@c3bottles.route("/visit/<int:number>")
@needs_visiting
def visit(number=None):
    dp = DropPoint.query.get_or_404(request.values.get("number", number))

    if dp.removed:
        abort(404)

    action = request.values.get("maintenance")

    if action:
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
            flash({
                "class": "success disappear",
                "text": lazy_gettext("Your visit has been processed successfully."),
            })
            return redirect("{}#{}/{}/{}/3".format(url_for("dp_map"), dp.level, dp.lat, dp.lng))
    else:
        return render_template(
            "visit.html",
            dp=dp,
        )
