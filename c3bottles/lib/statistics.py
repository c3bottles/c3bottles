from c3bottles.model.drop_point import DropPoint
from c3bottles.model.report import Report
from c3bottles.model.visit import Visit
from c3bottles.model.category import categories_sorted


def drop_points_by_category_gen(category):
    return lambda: DropPoint.query.filter(DropPoint.category_id == category.category_id, DropPoint.removed == None).count()  # noqa


def drop_points_by_state(state):
    count = 0
    for dp in DropPoint.query.all():
        if not dp.removed:
            s = dp.last_state
            if s == state:
                count += 1
    return count


def drop_points_by_state_gen(state):
    return lambda: drop_points_by_state(state)


def drop_points_by_category_and_state(category, state):
    count = 0
    for dp in DropPoint.query.filter(DropPoint.category_id == category.category_id):
        if not dp.removed:
            s = dp.last_state
            if s == state:
                count += 1
    return count


def drop_points_by_category_and_state_gen(category, state):
    return lambda: drop_points_by_category_and_state(category, state)


def reports_by_category_and_state(category, state):
    count = 0
    for report in Report.query.filter(Report.state == state):
        if report.dp.category_id == category.category_id:
            count += 1
    return count


def reports_by_category_and_state_gen(category, state):
    return lambda: reports_by_category_and_state(category, state)


class Statistics(object):

    @property
    def overall_drop_point_count(self):
        try:
            return DropPoint.query.filter(DropPoint.removed == None).count()  # noqa
        except:  # noqa
            return 0

    @property
    def drop_points_by_category(self):
        ret = {}
        try:
            for category in categories_sorted():
                ret[category.name] = drop_points_by_category_gen(category)
        except:  # noqa
            pass
        return ret

    @property
    def report_count(self):
        try:
            return Report.query.count()
        except:  # noqa
            return 0

    @property
    def visit_count(self):
        try:
            return Visit.query.count()
        except:  # noqa
            return 0

    @property
    def overall_drop_points_by_state_prometheus(self):
        ret = {}
        for state in Report.states:
            ret[state] = drop_points_by_state_gen(state)
        return ret

    @property
    def overall_drop_points_by_state(self):
        ret = {}
        for state in Report.states:
            ret[state] = 0
        try:
            for dp in DropPoint.query.all():
                if not dp.removed:
                    s = dp.last_state
                    ret[s] = ret[s] + 1 if s in ret else 1
        except:  # noqa
            pass
        return ret

    @property
    def drop_points_by_category_and_state(self):
        ret = {}
        try:
            for category in categories_sorted():
                ret[category.name] = {}
                for state in Report.states:
                    ret[category.name][state] = drop_points_by_category_and_state_gen(
                        category, state)
        except:  # noqa
            pass
        return ret

    @property
    def reports_by_state(self):
        ret = {}
        for state in Report.states:
            try:
                ret[state] = Report.query.filter(Report.state == state).count()
            except:  # noqa
                ret[state] = 0
        return ret

    @property
    def reports_by_category_and_state(self):
        ret = {}
        for cat in categories_sorted():
            ret[cat.name] = {}
            for state in Report.states:
                ret[cat.name][state] = reports_by_category_and_state_gen(cat, state)
        return ret

    @property
    def visits_by_action(self):
        ret = {}
        for action in Visit.actions:
            try:
                ret[action] = Visit.query.filter(Visit.action == action).count()
            except:  # noqa
                ret[action] = 0
        return ret


stats_obj = Statistics()
