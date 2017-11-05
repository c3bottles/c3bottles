from flask import render_template, request, g, abort
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
            heading="Error!",
            text="Drop point not found.",
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
                text="Errors occurred while processing your visit:",
                errors=[v for d in e.args for v in d.values()]
            )
        else:
            db.session.commit()
            return render_template(
                "success.html",
                heading="Thank you!",
                text="Your visit has been processed successfully."
            )
    else:
        return render_template(
            "visit.html",
            dp=dp
        )

# vim: set expandtab ts=4 sw=4:
