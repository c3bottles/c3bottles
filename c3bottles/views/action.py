from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_babel import lazy_gettext

from c3bottles.model.drop_point import DropPoint
from c3bottles.model.report import Report
from c3bottles.model.visit import Visit
from c3bottles.views import needs_reporting, needs_visiting

bp = Blueprint("action", __name__)


@bp.route("/report", methods=("GET", "POST"))
@bp.route("/<int:number>")
@needs_reporting
def report(number: int = None):
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
                errors=[v for d in e.args for v in d.values()],
            )
        else:
            return render_template(
                "success.html",
                heading=lazy_gettext("Thank you!"),
                text=lazy_gettext("Your report has been received successfully."),
            )
    else:
        return render_template("action/report.html", dp=dp)


@bp.route("/visit", methods=("GET", "POST"))
@bp.route("/visit/<int:number>")
@needs_visiting
def visit(number: int = None):
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
                errors=[v for d in e.args for v in d.values()],
            )
        else:
            flash(
                {
                    "class": "success disappear",
                    "text": lazy_gettext("Your visit has been processed successfully."),
                }
            )
            return redirect(f"{url_for('view.map_')}#{dp.level}/{dp.lat}/{dp.lng}/3")
    else:
        return render_template(
            "action/visit.html",
            dp=dp,
        )
