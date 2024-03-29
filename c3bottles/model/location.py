from datetime import datetime
from typing import Dict, List, Union

from flask_babel import LazyString, lazy_gettext

from c3bottles import app, db
from c3bottles.model import drop_point


class Location(db.Model):
    """
    A physical location of a drop point at some point in time.

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

    MAX_DESCRIPTION: int = 140

    loc_id = db.Column(db.Integer, primary_key=True)

    dp_id = db.Column(db.Integer, db.ForeignKey("drop_point.number"), nullable=False)

    dp = db.relationship("DropPoint")

    time = db.Column(db.DateTime)
    description = db.Column(db.String(MAX_DESCRIPTION))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    level = db.Column(db.Integer)

    def __init__(
        self,
        dp: "drop_point.DropPoint",
        time: datetime = None,
        description: str = None,
        lat: float = None,
        lng: float = None,
        level: int = None,
    ):
        errors: List[Dict[str, LazyString]] = []

        if not isinstance(dp, drop_point.DropPoint):
            errors.append({"Location": lazy_gettext("Not given a drop point object.")})
            raise ValueError(errors)

        self.dp = dp

        if time and not isinstance(time, datetime):
            errors.append({"Location": lazy_gettext("Start time not a datetime object.")})

        if isinstance(time, datetime) and time > datetime.now():
            errors.append({"Location": lazy_gettext("Start time in the future.")})

        if dp.locations and isinstance(time, datetime) and time < dp.locations[-1].time:
            errors.append({"Location": lazy_gettext("Location older than current.")})

        self.time = time if time else datetime.now()

        try:
            self.lat = float(lat)
        except (TypeError, ValueError):
            errors.append({"lat": lazy_gettext("Latitude is not a floating point number.")})

        try:
            self.lng = float(lng)
        except (TypeError, ValueError):
            errors.append({"lng": lazy_gettext("Longitude is not a floating point number.")})

        try:
            self.level = int(level)
        except (TypeError, ValueError):
            errors.append({"level": lazy_gettext("Level is not a number.")})

        try:
            self.description = str(description)
        except (TypeError, ValueError):
            errors.append({"description": lazy_gettext("Location description is not a string.")})
        else:
            if len(self.description) > self.MAX_DESCRIPTION:
                errors.append({"description": lazy_gettext("Location description is too long.")})

        if errors:
            raise ValueError(*errors)

        db.session.add(self)
        db.session.commit()

    @property
    def description_with_level(self) -> Union[str, LazyString]:
        map_source = app.config.get("MAP_SOURCE", {})
        if len(map_source.get("level_config", [])) > 1:
            return lazy_gettext(
                "%(location)s on level %(level)i",
                location=self.description if self.description else lazy_gettext("somewhere"),
                level=self.level,
            )
        else:
            return self.description if self.description else lazy_gettext("somewhere")

    def __repr__(self) -> str:
        return (
            f"Location {self.loc_id} of drop point {self.dp_id} "
            f"({self.description} since {self.time})"
        )
