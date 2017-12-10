from datetime import datetime

from flask_babel import lazy_gettext as _

from .. import db

from . import drop_point


class Location(db.Model):
    """A physical location of a drop point at some point in time.

    Drop points may be relocated at any time for whatever reason. For
    analysis after an event and optimization of the drop point locations
    for the next event at the same venue, drop point locations are tracked
    over time.

    Each location has a start time indicating the placement of the drop
    point at that location. If a drop point is relocated, a new location
    with the respective start time is added. If the start time is null,
    the drop point has been there since the creation of the universe.

    If the human-readable description as well as the coordinates both are
    null, the location of that drop point is unknown.
    """

    max_description = 140

    loc_id = db.Column(db.Integer, primary_key=True)

    dp_id = db.Column(
        db.Integer,
        db.ForeignKey("drop_point.number"),
        nullable=False
    )

    dp = db.relationship("DropPoint")

    time = db.Column(db.DateTime)
    description = db.Column(db.String(max_description))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    level = db.Column(db.Integer)

    def __init__(
            self,
            dp,
            time=None,
            description=None,
            lat=None,
            lng=None,
            level=None
    ):

        errors = []

        if not isinstance(dp, drop_point.DropPoint):
            errors.append({
                "Location": _("Not given a drop point object.")
            })
            raise ValueError(errors)

        self.dp = dp

        if time and not isinstance(time, datetime):
            errors.append({
                "Location": _("Start time not a datetime object.")
            })

        if isinstance(time, datetime) and time > datetime.today():
            errors.append({
                "Location": _("Start time in the future.")
            })

        if dp.locations and isinstance(time, datetime) and \
                time < dp.locations[-1].time:
            errors.append({
                "Location": _("Location older than current.")
            })

        self.time = time if time else datetime.today()

        try:
            self.lat = float(lat)
        except (TypeError, ValueError):
            errors.append({
                "lat": _("Latitude is not a floating point number.")
            })

        try:
            self.lng = float(lng)
        except (TypeError, ValueError):
            errors.append({
                "lng": _("Longitude is not a floating point number.")
            })

        try:
            self.level = int(level)
        except (TypeError, ValueError):
            errors.append({
                "level": _("Level is not a number.")
            })

        try:
            self.description = str(description)
        except (TypeError, ValueError):
            errors.append({
                "description": _("Location description is not a string.")
            })
        else:
            if len(self.description) > self.max_description:
                errors.append({
                    "description": _("Location description is too long.")
                })

        if errors:
            raise ValueError(*errors)

        db.session.add(self)

    def __repr__(self):
        return "Location %s of drop point %s (%s since %s)" % (
            self.loc_id, self.dp_id,
            self.description, self.time
        )
