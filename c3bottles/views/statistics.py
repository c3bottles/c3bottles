from flask import render_template, Blueprint, make_response, jsonify

from c3bottles.lib.statistics import stats_obj


bp = Blueprint("statistics", __name__)


@bp.route("/numbers")
def numbers():
    return render_template(
        "statistics/numbers.html",
        stats=stats_obj
    )


@bp.route("/numbers.json")
def numbers_json():
    return jsonify({
        "dropPoints": stats_obj.overall_drop_points_by_state,
        "reports": stats_obj.reports_by_state
    })


@bp.route("/numbers.js")
def numbers_js():
    resp = make_response(render_template(
        "js/statistics.js",
        stats=stats_obj
    ))
    resp.mimetype = "application/javascript"
    return resp
