from flask import render_template, Blueprint

from c3bottles import db
from model.drop_point import DropPoint
from model.report import Report
from model.visit import Visit

stats = Blueprint("statistics", __name__)

@stats.route("/numbers")
def statistics():
    return render_template(
        "statistics.html",
        stats=Statistics()
    )   

class Statistics():

    @property
    def drop_point_count(self):
        return DropPoint.query.count()

    @property
    def report_count(self):
        return Report.query.count()

    @property
    def visit_count(self):
        return Visit.query.count()

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

# vim: set expandtab ts=4 sw=4:
