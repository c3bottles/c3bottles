from flask import request, Response

from c3bottles import db
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
        dp = db.session.query(DropPoint).get(request.values.get("number"))
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
        dp = db.session.query(DropPoint).get(request.values.get("number"))
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
    return Response(
        DropPoint.get_all_dps_as_geojson(),
        mimetype="application/json"
    )

# vim: set expandtab ts=4 sw=4:
