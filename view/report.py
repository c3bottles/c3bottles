from flask import render_template, request

from controller import c3bottles, db
from model.drop_point import DropPoint

@c3bottles.route("/report", methods=("GET", "POST"))
@c3bottles.route("/<int:number>")
def report(number=None):
    if number:
        dp = DropPoint.get(number)
    else:
        dp = DropPoint.get(request.values.get("number"))

    if not dp:
        return render_template(
            "error.html",
            heading="Error!",
            text="Drop point not found.",
        )

    state = request.values.get("state")

    if state:
        from model.report import Report
        try:
            Report(dp=dp, state=state)
        except ValueError as e:
            return render_template(
                "error.html",
                text="Errors occurred while processing your report:",
                errors=[v for d in e.args for v in d.values()]
            )
        else:
            db.session.commit()
            return render_template(
                "success.html",
                heading="Thank you!",
                text="Your report has been received successfully."
            )
    else:
        return render_template(
            "report.html",
            dp=dp
        )

# vim: set expandtab ts=4 sw=4:
