from flask import render_template, Blueprint, make_response

from ..lib import stats_obj
from ..model.drop_point import DropPoint
from ..model.report import Report
from ..model.visit import Visit


stats = Blueprint("statistics", __name__)


@stats.route("/numbers")
def html():
    return render_template(
        "statistics.html",
        stats=stats_obj
    )


@stats.route("/numbers.js")
def js():
    resp = make_response(render_template(
        "js/statistics.js",
        stats=stats_obj
    ))
    resp.mimetype = "application/javascript"
    return resp
