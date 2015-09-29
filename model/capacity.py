from datetime import datetime

from c3bottles import db
import drop_point


class Capacity(db.Model):
    """The capacity of a drop point at some point in time.

    The capacity of drop points may change over time as empty crates can
    and will be added or removed on demand. Like the location, the
    capacity is tracked over time to allow for analysis and optimization
    after an event.

    Each capacity has a start time indicating the presence of a particular
    number of empty crates at the drop point at that time. If crates are
    added or removed, a new capacity with the respective start time is
    added. If the start time is null, the crates have been there forever.

    If the number of crates is null, the drop point only consists of a
    sign on the wall but no crates at all.
    """

    default_crate_count = 1

    cap_id = db.Column(db.Integer, primary_key=True)

    dp_id = db.Column(
        db.Integer,
        db.ForeignKey("drop_point.number"),
        nullable=False
    )

    dp = db.relationship("DropPoint")

    time = db.Column(db.DateTime)
    crates = db.Column(db.Integer, default=default_crate_count)

    def __init__(
            self,
            dp,
            time=None,
            crates=default_crate_count
    ):

        errors = []

        if not isinstance(dp, drop_point.DropPoint):
            errors.append({"Capacity": "Not given a drop point object."})
            raise ValueError(errors)

        self.dp = dp

        if time and not isinstance(time, datetime):
            errors.append({"Capacity": "Start time not a datetime object."})
            raise ValueError(errors)

        if time and time > datetime.today():
            errors.append({"Capacity": "Start time in the future."})

        if dp.capacities and time and \
                time < dp.capacities[-1].time:
            errors.append({"Capacity": "Capacity older than current."})

        self.time = time if time else datetime.today()

        if crates is None:
            self.crates = self.default_crate_count
        else:
            try:
                self.crates = int(crates)
            except (TypeError, ValueError):
                errors.append({"crates": "Crate count is not a number."})
            else:
                if self.crates < 0:
                    errors.append({"crates": "Crate count is not positive."})

        if errors:
            raise ValueError(errors)

        db.session.add(self)

    def __repr__(self):
        return "Capacity %s of drop point %s (%s crates since %s)" % (
            self.cap_id, self.dp_id,
            self.crates, self.time
        )

# vim: set expandtab ts=4 sw=4:
