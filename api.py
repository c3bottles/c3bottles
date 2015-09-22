import json

from flask import request, Response

from c3bottles import c3bottles, db
from model import DropPoint, Report, Visit, report_states, visit_actions


def process():
    if request.values.get("action") == "report":
        return report()
    elif request.values.get("action") == "visit":
        return visit()
    elif request.values.get("action") == "dp_json":
        return dp_json()

    return Response("Invalid or missing API action.", status=400)


def report():
    try:
        dp = db.session.query(DropPoint).get(request.values.get("dp_number"))
    except TypeError:
        return Response("Missing drop point number.", status=400)

    if not isinstance(dp, DropPoint):
        return Response("Invalid drop point number.", status=404)

    reported_state = request.values.get("state")
    if reported_state not in report_states:
        return Response("Invalid or missing reported state", status=404)

    Report(dp, state=reported_state)
    db.session.commit()

    return Response("Success.")


def visit():
    try:
        dp = db.session.query(DropPoint).get(request.values.get("dp_number"))
    except TypeError:
        return Response("Missing drop point number.", status=400)

    if not isinstance(dp, DropPoint):
        return Response("Invalid drop point number.", status=404)

    performed_maintenance = request.values.get("maintenance")
    if performed_maintenance not in visit_actions:
        return Response("Invalid or missing maintenance action.", status=404)

    Visit(dp, action=performed_maintenance)
    db.session.commit()

    return Response("Success.")


def dp_json():
    all_dps = []
    for dp in db.session.query(DropPoint).order_by(DropPoint.number).all():
        all_dps.append({
            "number": dp.number,
            "location": dp.get_current_location().description,
            "reports_total": dp.get_total_report_count(),
            "reports_new": dp.get_new_report_count(),
            "priority": dp.get_priority(),
            "last_state": dp.get_last_state(),
            "crates": dp.get_current_crate_count(),
            "removed": True if dp.removed else False
        })
    return Response(
        json.dumps(all_dps, indent=4 if c3bottles.debug else None),
        mimetype="application/json"
    )

# vim: set expandtab ts=4 sw=4:
