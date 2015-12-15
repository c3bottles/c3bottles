from flask import render_template, Response

from controller import c3bottles, db
from model.drop_point import DropPoint


@c3bottles.route("/")
def index():
    return render_template("index.html")


@c3bottles.route("/faq")
def faq():
    return render_template("faq.html")


@c3bottles.route("/list")
def dp_list():
    all_dps = []
    for dp in db.session.query(DropPoint).all():
        if not dp.removed:
            all_dps.append({
                "number": dp.number,
                "location": dp.get_current_location(),
                "reports_total": dp.get_total_report_count(),
                "reports_new": dp.get_new_report_count(),
                "priority": dp.get_priority(),
                "last_state": dp.get_last_state(),
                "crates": dp.get_current_crate_count(),
            })
    return render_template(
        "list.html",
        all_dps=sorted(all_dps, key=lambda k: k["priority"], reverse=True),
        all_dps_json=DropPoint.get_dps_json()
    )


@c3bottles.route("/map")
def dp_map():
    return render_template(
        "map.html",
        all_dps_json=DropPoint.get_dps_json()
    )


@c3bottles.route("/view/<int:number>")
@c3bottles.route("/view")
def dp_view(number=None):
    dp = DropPoint.get(number)
    if dp:
        history = dp.get_history()
        return render_template(
            "view.html",
            dp=dp,
            history=history
        )
    else:
        return render_template(
            "error.html",
            heading="Error!",
            text="Drop point not found.",
        )


@c3bottles.route("/label/<int:number>.pdf")
def dp_label(number=None):
    dp = DropPoint.get(number)
    if dp:
        from cairosvg import svg2pdf
        return Response(
            svg2pdf(render_template("label.svg", number=number)),
            mimetype="application/pdf"
        )
    else:
        return render_template(
            "error.html",
            heading="Error!",
            text="Drop point not found.",
        )

# vim: set expandtab ts=4 sw=4:
