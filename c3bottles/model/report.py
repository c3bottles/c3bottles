from datetime import datetime
from typing import Dict, List, Tuple

from flask_babel import lazy_gettext, LazyString

from c3bottles import db
from c3bottles.lib import metrics
from c3bottles.model import drop_point


class Report(db.Model):
    """
    The report of a visitor that a drop point needs maintenance.

    When visitors find a drop point needing maintenance, they may report
    the drop point to the bottle collectors. A report is issued for a
    given drop point which has a time and optionally some information
    about the state of the drop point in question.
    """

    state_weights: List[Tuple[str, float]] = [
        ("DEFAULT", 5.0),  # 0 should be the default/unknown state
        ("NEW", 1.0),  # 1 should be the state of new drop points
        ("NO_CRATES", 5.0),
        ("SOME_BOTTLES", 1.0),
        ("REASONABLY_FULL", 2.0),
        ("FULL", 3.0),
        ("OVERFLOW", 5.0),
        ("EMPTY", 0.0),  # -1 should be the EMPTY state
    ]

    states: List[str] = [e[0] for e in state_weights]

    rep_id = db.Column(db.Integer, primary_key=True)

    dp_id = db.Column(db.Integer, db.ForeignKey("drop_point.number"), nullable=False)

    dp = db.relationship("DropPoint")

    time = db.Column(db.DateTime, nullable=False)

    state = db.Column(db.Enum(*states, name="report_states"), default=states[0])

    def __init__(self, dp: "drop_point.DropPoint", time: datetime = None, state: str = None):

        errors: List[Dict[str, LazyString]] = []

        self.dp = dp

        if not isinstance(dp, drop_point.DropPoint):
            errors.append({"Report": lazy_gettext("Not given a drop point object.")})
        else:
            if dp.removed:
                errors.append({"Report": lazy_gettext("Drop point has been removed.")})

        if time and not isinstance(time, datetime):
            errors.append({"Report": lazy_gettext("Time not a datetime object.")})

        if isinstance(time, datetime) and time > datetime.now():
            errors.append({"Report": lazy_gettext("Start time in the future.")})

        self.time = time if time else datetime.now()

        if state in Report.states:
            self.state = state
        else:
            errors.append({"Report": lazy_gettext("Invalid or missing reported state.")})

        if errors:
            raise ValueError(*errors)

        dp.last_state = self.state

        db.session.add(dp)
        db.session.add(self)
        db.session.commit()

        metrics.report_count.labels(state=self.state, category=self.dp.category.metrics_name).inc()

    def get_weight(self) -> float:
        """Get the weight (i.e. significance) of a report.

        The weight of a report determines how significant it is for the
        calculation of the priority to visit the respective drop point
        soon.

        Most important for the weight of a report is the state of the
        drop point as seen by the reporter. The report of an
        overflowing drop point is certainly more important than one
        of a drop point nearly empty.

        If the reporter is a trusted user, that increases the weight.

        Special users see special weights: The supervisor of the
        bottle collectors is not focused on full drop points (that's
        what they have a collector team for) but rather on solving
        problems like overflows or missing crates reported by trusted
        users.

        The default weight under default conditions is 1 and all
        influences should only multiply that default value with some
        factor.
        """

        # TODO:
        # - weight should depend on the reporter (trusted > stranger)
        # - weight should depend on the viewer (supervisor: problem-
        #   focused, collector: collection-focused)

        return self.get_state_weight(self.state)

    @classmethod
    def get_state_weight(cls, state: str) -> float:
        for name, weight in cls.state_weights:
            if name == state:
                return weight
        return float(cls.state_weights[0][1])

    def __repr__(self) -> str:
        return (
            f"Report {self.rep_id} of drop point {self.dp_id} "
            f"(state {self.state} at {self.time})"
        )
