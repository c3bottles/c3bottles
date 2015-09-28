import json

from flask import request, Response

from c3bottles import c3bottles, db
from model.droppoint import DropPoint
from model.report import Report
from model.visit import Visit


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
    try:
        Report(
            dp=DropPoint.get(request.values.get("number")),
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
            json.dumps("Success.", indent=4 if c3bottles.debug else None),
            mimetype="application/json"
        )


def visit():
    try:
        Visit(
            dp=DropPoint.get(request.values.get("number")),
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
            json.dumps("Success.", indent=4 if c3bottles.debug else None),
            mimetype="application/json"
        )


def dp_json():
    return Response(
        DropPoint.get_all_dps_as_geojson(),
        mimetype="application/json"
    )

# vim: set expandtab ts=4 sw=4:
