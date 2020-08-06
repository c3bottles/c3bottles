import json
from datetime import datetime

from flask import Blueprint, Response, jsonify, request
from flask_login import current_user
from flask_wtf.csrf import generate_csrf

from c3bottles import app
from c3bottles.model.drop_point import DropPoint
from c3bottles.model.report import Report
from c3bottles.model.visit import Visit

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/")
def index():
    return jsonify({})


@bp.route("/token")
def update_csrf_token():
    return jsonify({"token": generate_csrf()})


@bp.route("/all_dp.json")
def all_dp_json():
    ts = request.values.get("ts")
    if ts:
        try:
            dps = DropPoint.get_dps_json(time=datetime.fromtimestamp(int(ts)))
        except ValueError as e:
            return Response(
                json.dumps(e.args, indent=4 if app.debug else None),
                mimetype="application/json",
                status=400,
            )
    else:
        dps = DropPoint.get_dps_json()

    return Response(dps, mimetype="application/json")


@bp.route("/map_source.json")
def map_source():
    map_source = app.config.get("MAP_SOURCE", {})
    return jsonify(
        {
            "attribution": map_source.get("attribution", ""),
            "tileserver": map_source.get("tileserver", ""),
            "tileserver_subdomains": map_source.get("tileserver_subdomains", []),
            "bounds": map_source.get("bounds", None),
            "initial_view": map_source.get("initial_view", None),
            "level_config": map_source.get("level_config", None),
            "min_zoom": map_source.get("min_zoom", 0),
            "max_zoom": map_source.get("max_zoom", 0),
            "simple_crs": map_source.get("simple_crs", False),
            "hack_257px": map_source.get("hack_257px", False),
            "tms": map_source.get("tms", False),
            "no_wrap": map_source.get("no_wrap", False),
        }
    )


@bp.route("/report", methods=("POST",))
def report():
    if not current_user.can_report:
        return Response(
            json.dumps(
                [{"msg": "Not logged in or insufficient privileges."}],
                indent=4 if app.debug else None,
            ),
            mimetype="application/json",
            status=401,
        )
    number = request.values.get("number")
    try:
        Report(dp=DropPoint.query.get(number), state=request.values.get("state"))
    except ValueError as e:
        return Response(
            json.dumps(e.args, indent=4 if app.debug else None),
            mimetype="application/json",
            status=400,
        )
    else:
        return Response(DropPoint.get_dp_json(number), mimetype="application/json")


@bp.route("/visit", methods=("POST",))
def visit():
    if not current_user.can_visit:
        return Response(
            json.dumps(
                [{"msg": "Not logged in or insufficient privileges."}],
                indent=4 if app.debug else None,
            ),
            mimetype="application/json",
            status=401,
        )
    number = request.values.get("number")
    try:
        Visit(dp=DropPoint.query.get(number), action=request.values.get("maintenance"))
    except ValueError as e:
        return Response(
            json.dumps(e.args, indent=4 if app.debug else None),
            mimetype="application/json",
            status=400,
        )
    else:
        return Response(DropPoint.get_dp_json(number), mimetype="application/json")
