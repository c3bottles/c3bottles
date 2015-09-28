from datetime import datetime

from c3bottles import db
import droppoint


class Report(db.Model):
    """The report of a visitor that a drop point needs maintenance.

    When visitors find a drop point needing maintenance, they may report
    the drop point to the bottle collectors. A report is issued for a
    given drop point which has a time and optionally some information
    about the state of the drop point in question.
    """

    states = (
        "DEFAULT",
        "NO_CRATES",
        "EMPTY",
        "SOME_BOTTLES",
        "REASONABLY_FULL",
        "FULL",
        "OVERFLOW"
    )

    rep_id = db.Column(db.Integer, primary_key=True)

    dp_id = db.Column(
        db.Integer,
        db.ForeignKey("drop_point.number"),
        nullable=False
    )

    dp = db.relationship("DropPoint")

    time = db.Column(db.DateTime, nullable=False)

    state = db.Column(
        db.Enum(*states, name="report_states"),
        default=states[0]
    )

    def __init__(self, dp, time=None, state=None):

        errors = []

        self.dp = dp

        if not isinstance(dp, droppoint.DropPoint):
            errors.append({"Report": "Not given a drop point object."})

        if time and not isinstance(time, datetime):
            errors.append({"Report": "Time not a datetime object."})

        if time and time > datetime.today():
            errors.append({"Report": "Start time in the future."})

        self.time = time if time else datetime.today()

        if state in Report.states:
            self.state = state
        else:
            errors.append({"Report": "Invalid or missing reported state."})

        if errors:
            raise ValueError(errors)

        db.session.add(self)

    def get_weight(self):
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
        # - weight should depend on the state (OVERFLOW > FULL > rest)
        # - weight should depend on the reporter (trusted > stranger)
        # - weight should depend on the viewer (supervisor: problem-
        #   focused, collector: collection-focused)

        return 1

    def __repr__(self):
        return "Report %s of drop point %s (state %s at %s)" % (
            self.rep_id, self.dp_id,
            self.state, self.time
        )

# vim: set expandtab ts=4 sw=4:
