import json
from datetime import datetime

from flask import request, Response, Blueprint
from flask_login import current_user

from c3bottles import app, db
from c3bottles.model.drop_point import DropPoint
from c3bottles.model.report import Report
from c3bottles.model.visit import Visit


bp = Blueprint("api", __name__)


@bp.route("/api", methods=("POST", "GET"))
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
            indent=4 if app.debug else None
        ),
        mimetype="application/json",
        status=400
    )


def report():
    if not current_user.can_report:
        return Response(
            json.dumps(
                [{"msg": "Not logged in or insufficient privileges."}],
                indent=4 if app.debug else None
            ),
            mimetype="application/json",
            status=401
        )
    number = request.values.get("number")
    try:
        Report(
            dp=DropPoint.query.get(number),
            state=request.values.get("state")
        )
    except ValueError as e:
        return Response(
            json.dumps(e.args, indent=4 if app.debug else None),
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
    if not current_user.can_visit:
        return Response(
            json.dumps(
                [{"msg": "Not logged in or insufficient privileges."}],
                indent=4 if app.debug else None
            ),
            mimetype="application/json",
            status=401
        )
    number = request.values.get("number")
    try:
        Visit(
            dp=DropPoint.query.get(number),
            action=request.values.get("maintenance")
        )
    except ValueError as e:
        return Response(
            json.dumps(e.args, indent=4 if app.debug else None),
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
                time=datetime.fromtimestamp(float(ts))
            )
        except ValueError as e:
            return Response(
                json.dumps(e.args, indent=4 if app.debug else None),
                mimetype="application/json",
                status=400
            )
    else:
        dps = DropPoint.get_dps_json()

    return Response(
        dps,
        mimetype="application/json"
    )
