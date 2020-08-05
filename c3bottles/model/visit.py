from datetime import datetime
from typing import Dict, List, Tuple

from flask_babel import LazyString, lazy_gettext

from c3bottles import db
from c3bottles.lib import metrics
from c3bottles.model import drop_point, report


class Visit(db.Model):
    """
    A maintenance visit of bottle collectors at a drop point.

    After a report of a problem with a certain drop point has been
    generated or a drop point has not been visited for a long time, the
    bottle collectors are advised to visit that drop point. After doing
    so, they log their visit and the action taken.
    """

    actions: Tuple[str] = (
        "EMPTIED",  # 0 should be the action that empties a drop point
        "ADDED_CRATE",
        "REMOVED_CRATE",
        "RELOCATED",
        "REMOVED",
        "NO_ACTION",
    )

    vis_id = db.Column(db.Integer, primary_key=True)

    dp_id = db.Column(db.Integer, db.ForeignKey("drop_point.number"), nullable=False)

    dp = db.relationship("DropPoint")

    time = db.Column(db.DateTime, nullable=False)

    action = db.Column(db.Enum(*actions, name="visit_actions"), default=actions[0])

    def __init__(self, dp: "drop_point.DropPoint", time: datetime = None, action: str = None):

        errors: List[Dict[str, LazyString]] = []

        self.dp = dp

        if not isinstance(dp, drop_point.DropPoint):
            errors.append({"Visit": lazy_gettext("Not given a drop point object.")})
        else:
            if dp.removed:
                errors.append({"Visit": lazy_gettext("Drop point has been removed.")})

        if time and not isinstance(time, datetime):
            errors.append({"Visit": lazy_gettext("Time not a datetime object.")})

        if isinstance(time, datetime) and time > datetime.today():
            errors.append({"Visit": lazy_gettext("Start time in the future.")})

        self.time = time if time else datetime.today()

        if action in Visit.actions:
            self.action = action
        else:
            errors.append({"Visit": lazy_gettext("Invalid or missing maintenance action.")})

        if errors:
            raise ValueError(*errors)

        if self.action == Visit.actions[0]:
            dp.last_state = report.Report.states[-1]
            db.session.add(dp)

        db.session.add(self)
        db.session.commit()

        metrics.visit_count.labels(action=self.action, category=self.dp.category.metrics_name).inc()

    def __repr__(self) -> str:
        return (
            f"Visit {self.vis_id} of drop point {self.dp_id} (action {self.action} at {self.time})"
        )
