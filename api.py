import json
from datetime import datetime

from flask import request, Response, g, Blueprint

from c3bottles import c3bottles, db
from model.drop_point import DropPoint
from model.report import Report
from model.visit import Visit


api = Blueprint("api", __name__)

@api.route("/api", methods=("POST", "GET"))
def process():
    if request.values.get("action") == "report":
        return report()
    elif request.values.get("action") == "visit":
        return visit()
    elif request.values.get("action") == "dp_json":
        return dp_json()

    return Response(
        json.dumps(
            "Invalid or missing API action.",
            indent=4 if c3bottles.debug else None
        ),
        mimetype="application/json",
        status=400
    )


def report():
    number = request.values.get("number")
    try:
        Report(
            dp=DropPoint.get(number),
            state=request.values.get("state")
        )
    except ValueError as e:
        return Response(
            json.dumps(e.message, indent=4 if c3bottles.debug else None),
            mimetype="application/json",
            status=400
        )
    else:
        db.session.commit()
        return Response(
            DropPoint.get_dp_json(number),
            mimetype="application/json"
        )


def visit():
    if not (g.user.is_authenticated() and g.user.can_visit()):
        return Response(
            json.dumps(
                [{"msg": "Not logged in or unsufficient privileges."}],
                indent=4 if c3bottles.debug else None
            ),
            mimetype="application/json",
            status=401
        )
    number = request.values.get("number")
    try:
        Visit(
            dp=DropPoint.get(number),
            action=request.values.get("maintenance")
        )
    except ValueError as e:
        return Response(
            json.dumps(e.message, indent=4 if c3bottles.debug else None),
            mimetype="application/json",
            status=400
        )
    else:
        db.session.commit()
        return Response(
            DropPoint.get_dp_json(number),
            mimetype="application/json"
        )


def dp_json():
    ts = request.values.get("ts")
    if ts:
        try:
            dps = DropPoint.get_dps_json(
                datetime.fromtimestamp(float(ts))
            )
        except ValueError as e:
            return Response(
                json.dumps(e.message, indent=4 if c3bottles.debug else None),
                mimetype="application/json",
                status=400
            )
    else:
        dps = DropPoint.get_dps_json()

    return Response(
        dps,
        mimetype="application/json"
    )

# vim: set expandtab ts=4 sw=4:
