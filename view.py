from flask import render_template

from c3bottles import c3bottles, db


@c3bottles.route("/")
def index():
    return render_template("index.html")


@c3bottles.route("/faq")
def faq():
    return render_template("faq.html")


@c3bottles.route("/numbers")
def statistics():
    return "TODO: Show some nice statistics"


@c3bottles.route("/list")
def dp_list():
    from model import DropPoint
    all_dps = []
    all_locations = []
    for dp in db.session.query(DropPoint).order_by(DropPoint.number).all():
        if dp.get_new_reports():
            last_state = dp.get_new_reports()[0].state
        else:
            last_state = None
        loc = dp.get_current_location()
        all_dps.append({
            "number": dp.number,
            "location": loc,
            "reports_total": dp.get_total_report_count(),
            "reports_new": dp.get_new_report_count(),
            "priority": dp.get_priority(),
            "last_state": last_state,
            "crates": dp.get_current_crate_count(),
            "removed": True if dp.removed else False
        })
        if loc.description not in all_locations and not dp.removed:
            all_locations.append(loc.description)
    return render_template(
        "list.html",
        all_dps=sorted(all_dps, key=lambda k: k["priority"], reverse=True),
        all_locations=sorted(all_locations)
    )


@c3bottles.route("/map")
def dp_map():
    return "TODO: Show the drop point map"


@c3bottles.route("/view/<int:dp_number>")
def dp_view(dp_number):
    from model import DropPoint
    return render_template(
        "view.html",
        dp=db.session.query(DropPoint).get(dp_number)
    )


@c3bottles.route("/report/<int:dp_number>")
@c3bottles.route("/<int:dp_number>")
def dp_report(dp_number):
    return "TODO: Report drop point " + str(dp_number)


@c3bottles.route("/visit/<int:dp_number>")
def dp_visit(dp_number):
    return "TODO: Visit drop point " + str(dp_number)


@c3bottles.route("/api")
def api():
    import api
    return api.process()

# vim: set expandtab ts=4 sw=4:
