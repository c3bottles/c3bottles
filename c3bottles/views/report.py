from flask import render_template, request, abort
from flask_babel import lazy_gettext

from .. import c3bottles, db
from ..model.drop_point import DropPoint
from ..model.report import Report
from . import needs_reporting


@c3bottles.route("/report", methods=("GET", "POST"))
@c3bottles.route("/<int:number>")
@needs_reporting
def report(number=None):
    dp = DropPoint.query.get_or_404(request.values.get("number", number))

    if dp.removed:
        abort(404)

    state = request.values.get("state")

    if state:
        try:
            Report(dp=dp, state=state)
        except ValueError as e:
            return render_template(
                "error.html",
                text=lazy_gettext("Errors occurred while processing your report:"),
                errors=[v for d in e.args for v in d.values()]
            )
        else:
            db.session.commit()
            return render_template(
                "success.html",
                heading=lazy_gettext("Thank you!"),
                text=lazy_gettext("Your report has been received successfully."),
            )
    else:
        return render_template(
            "report.html",
            dp=dp
        )
