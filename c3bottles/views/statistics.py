from flask import render_template, Blueprint, make_response

from ..model.drop_point import DropPoint
from ..model.report import Report
from ..model.visit import Visit


stats = Blueprint("statistics", __name__)


@stats.route("/numbers")
def html():
    return render_template(
        "statistics.html",
        stats=Statistics()
    )


@stats.route("/numbers.js")
def js():
    resp = make_response(render_template(
        "js/statistics.js",
        stats=Statistics()
    ))
    resp.mimetype = "application/javascript"
    return resp


class Statistics(object):

    @property
    def drop_point_count(self):
        return DropPoint.query.filter(DropPoint.removed == None).count()

    @property
    def report_count(self):
        return Report.query.count()

    @property
    def visit_count(self):
        return Visit.query.count()

    @property
    def drop_points_by_state(self):
        ret = {}
        for state in Report.states:
            ret[state] = 0
        for dp in DropPoint.query.all():
            if not dp.removed:
                s = dp.last_state
                ret[s] = ret[s] + 1 if s in ret else 1
        return ret

    @property
    def reports_by_state(self):
        ret = {}
        for state in Report.states:
            ret[state] = Report.query.filter(Report.state == state).count()
        return ret

    @property
    def visits_by_action(self):
        ret = {}
        for action in Visit.actions:
            ret[action] = Visit.query.filter(Visit.action == action).count()
        return ret
