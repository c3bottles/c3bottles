from datetime import datetime

from controller import db
import model.drop_point


class Visit(db.Model):
    """A maintenance visit of bottle collectors at a drop point.

    After a report of a problem with a certain drop point has been
    generated or a drop point has not been visited for a long time, the
    bottle collectors are advised to visit that drop point. After doing
    so, they log their visit and the action taken.
    """

    actions = (
        "EMPTIED",          # 0 should be the action that empties a drop point
        "ADDED_CRATE",
        "REMOVED_CRATE",
        "RELOCATED",
        "REMOVED",
        "NO_ACTION"
    )

    vis_id = db.Column(db.Integer, primary_key=True)

    dp_id = db.Column(
        db.Integer,
        db.ForeignKey("drop_point.number"),
        nullable=False
    )

    dp = db.relationship("DropPoint")

    time = db.Column(db.DateTime, nullable=False)

    action = db.Column(
        db.Enum(*actions, name="visit_actions"),
        default=actions[0]
    )

    def __init__(self, dp, time=None, action=None):

        errors = []

        self.dp = dp

        if not isinstance(dp, drop_point.DropPoint):
            errors.append({"Visit": "Not given a drop point object."})

        if time and not isinstance(time, datetime):
            errors.append({"Visit": "Time not a datetime object."})

        if isinstance(time, datetime) and time > datetime.today():
            errors.append({"Visit": "Start time in the future."})

        self.time = time if time else datetime.today()

        if action in Visit.actions:
            self.action = action
        else:
            errors.append({"Visit": "Invalid or missing maintenance action."})

        if errors:
            raise ValueError(errors)

        db.session.add(self)

    def __repr__(self):
        return "Visit %s of drop point %s (action %s at %s)" % (
            self.vis_id, self.dp_id,
            self.action, self.time
        )

# vim: set expandtab ts=4 sw=4:
