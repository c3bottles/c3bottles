from flask import Blueprint, make_response, render_template, abort

from c3bottles import app
from c3bottles.lib.statistics import stats_obj
from c3bottles.model.category import categories_sorted
from c3bottles.model.drop_point import DropPoint


bp = Blueprint("view", __name__)


@bp.route("/list")
def list_():
    return render_template(
        "view/list.html",
        total_drop_points=stats_obj.overall_drop_point_count,
        categories=categories_sorted(),
    )


@bp.route("/list.js")
def list_js():
    resp = make_response(
        render_template("js/list.js", all_dps_json=DropPoint.get_dps_json())
    )
    resp.mimetype = "application/javascript"
    return resp


@bp.route("/map")
def map_():
    if not app.config.get("MAP_SOURCE"):
        abort(404)
    return render_template(
        "view/map.html",
        total_drop_points=stats_obj.overall_drop_point_count,
        categories=categories_sorted(),
    )


@bp.route("/map.js")
def map_js():
    resp = make_response(
        render_template("js/map.js", all_dps_json=DropPoint.get_dps_json())
    )
    resp.mimetype = "application/javascript"
    return resp


@bp.route("/details")  # This seems useless but we need this for dynamic URL building
@bp.route("/details/<int:number>")
def details(number: int = None):
    dp = DropPoint.query.get_or_404(number)
    return render_template("view/details.html", dp=dp)


@bp.route("/details.js/<int:number>")
def details_js(number: int):
    resp = make_response(
        render_template(
            "js/details.js",
            all_dps_json=DropPoint.get_dps_json(),
            dp=DropPoint.query.get_or_404(number),
        )
    )
    resp.mimetype = "application/javascript"
    return resp
