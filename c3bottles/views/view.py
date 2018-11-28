from flask import Blueprint, make_response, render_template

from ..lib.statistics import stats_obj
from ..model.category import categories_sorted
from ..model.drop_point import DropPoint


view = Blueprint("view", __name__)


@view.route("/list")
def list_():
    return render_template(
        "view/list.html",
        total_drop_points=stats_obj.drop_point_count,
        categories=categories_sorted(),
    )


@view.route("/list.js")
def list_js():
    resp = make_response(render_template(
        "js/list.js",
        all_dps_json=DropPoint.get_dps_json()
    ))
    resp.mimetype = "application/javascript"
    return resp


@view.route("/map")
def map_():
    return render_template(
        "view/map.html",
        total_drop_points=stats_obj.drop_point_count,
        categories=categories_sorted(),
    )


@view.route("/map.js")
def map_js():
    resp = make_response(render_template(
        "js/map.js",
        all_dps_json=DropPoint.get_dps_json()
    ))
    resp.mimetype = "application/javascript"
    return resp


@view.route("/details")  # This seems useless but we need this for dynamic URL building
@view.route("/details/<int:number>")
def details(number=None):
    dp = DropPoint.query.get_or_404(number)
    return render_template("view/details.html", dp=dp)


@view.route("/details.js/<int:number>")
def details_js(number):
    resp = make_response(render_template(
        "js/details.js",
        all_dps_json=DropPoint.get_dps_json(),
        dp=DropPoint.query.get_or_404(number),
    ))
    resp.mimetype = "application/javascript"
    return resp
