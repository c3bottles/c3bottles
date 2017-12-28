from flask import render_template, request, g, abort

from .. import c3bottles, db

from ..model.drop_point import DropPoint
from ..model.report import Report


@c3bottles.route("/report", methods=("GET", "POST"))
@c3bottles.route("/<int:number>")
def report(number=None):
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

    state = request.values.get("state")

    if state:
        if g.no_anonymous_reporting and g.user.is_anonymous:
            abort(401)
        try:
            Report(dp=dp, state=state)
        except ValueError as e:
            return render_template(
                "error.html",
                text="Errors occurred while processing your report:",
                errors=[v for d in e.args for v in d.values()]
            )
        else:
            if dp.type == "drop_point":
                back = "/bottle/map"
            else:
                back = "/trash/map"
            db.session.commit()
            return render_template(
                "success.html",
                heading="Thank you!",
                text="Your report has been received successfully.",
                back=back
            )
    else:
        return render_template(
            "report.html",
            dp=dp,
            typename=dp.get_typename()
        )
