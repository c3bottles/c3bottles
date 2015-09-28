import json

from datetime import datetime

from c3bottles import c3bottles, db
from location import Location
from capacity import Capacity
from report import Report
from visit import Visit


class DropPoint(db.Model):
    """A location in the venue for visitors to drop their empty bottles.

    A drop point consists of a sign "bottle drop point <number>" at the
    wall which tells visitors that a drop point should be present there
    and a number of empty crates to drop bottles into. The sign is
    resembled by the location class whereas the crates are resembled by
    the capacity class. Drop points may exist with capacity zero (i.e.
    only a sign on the wall, no crates) or a location with valid time but
    no description or coordinates (i.e. the drop point is present
    somewhere but the location is unknown).

    If the `removed` column is not null, the drop
    point has been removed from the venue completely (numbers are not
    reassigned).

    Each drop point is referenced by a unique number, which is
    consequently the primary key to identify a specific drop point. Since
    capacity and location of drop points may change over time, they are
    not simply saved in the table of drop points but rather classes
    themselves.
    """

    number = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=False)

    time = db.Column(db.DateTime)

    removed = db.Column(db.DateTime)

    locations = db.relationship(
        "Location",
        order_by="Location.time"
    )

    capacities = db.relationship(
        "Capacity",
        order_by="Capacity.time"
    )

    reports = db.relationship(
        "Report",
        lazy="dynamic"
    )

    visits = db.relationship(
        "Visit",
        lazy="dynamic"
    )

    def __init__(
            self,
            number,
            description=None,
            lat=None,
            lng=None,
            level=None,
            crates=None,
            time=None
    ):

        errors = []

        try:
            self.number = int(number)
        except (TypeError, ValueError):
            errors.append({"number": "Drop point number is not a number."})
        else:
            if self.number < 1:
                errors.append({"number": "Drop point number is not positive."})
            if db.session.query(DropPoint).get(self.number):
                errors.append({"number": "That drop point already exists."})

        if time and not isinstance(time, datetime):
            errors.append({"DropPoint": "Creation time not a datetime object."})

        if time and time > datetime.today():
            errors.append({"DropPoint": "Creation time in the future."})

        self.time = time if time else datetime.today()

        try:
            Location(
                self,
                time=self.time,
                description=description,
                lat=lat,
                lng=lng,
                level=level
            )
        except ValueError as e:
            for m in e.message:
                errors.append(m)

        try:
            Capacity(
                self,
                time=self.time,
                crates=crates
            )
        except ValueError as e:
            for m in e.message:
                errors.append(m)

        if errors:
            raise ValueError(errors)

        db.session.add(self)

    def remove(self, time=None):

        if self.removed:
            raise RuntimeError({"DropPoint": "Drop point already removed."})

        if time and not isinstance(time, datetime):
            raise TypeError({"DropPoint": "Removal time not a datetime object."})

        if time and time > datetime.today():
            raise ValueError({"DropPoint": "Removal time in the future."})

        self.removed = time if time else datetime.today()

    def report(self, state=None, time=None):
        Report(self, time=time, state=state)

    def visit(self, action=None, time=None):
        Visit(self, time=time, action=action)

    def get_current_location(self):
        return self.locations[-1] if self.locations else None

    def get_current_crate_count(self):
        return self.capacities[-1].crates if self.capacities else 0

    def get_total_report_count(self):
        return self.reports.count()

    def get_new_report_count(self):
        last_visit = self.get_last_visit()
        if last_visit:
            return self.reports. \
                filter(Report.time > last_visit.time). \
                count()
        else:
            return self.get_total_report_count()

    def get_last_state(self):
        last_report = self.get_last_report()
        last_visit = self.get_last_visit()

        if last_report is not None and last_visit is not None:
            if last_visit.time > last_report.time \
                    and last_visit.action == "EMPTIED":
                return "EMPTY"
            else:
                return last_report.state
        elif last_report is not None:
            return last_report.state
        else:
            return "UNKNOWN"

    def get_last_report(self):
        return self.reports.order_by(Report.time.desc()).first()

    def get_last_visit(self):
        return self.visits.order_by(Visit.time.desc()).first()

    def get_new_reports(self):
        last_visit = self.get_last_visit()
        if last_visit:
            return self.reports. \
                filter(Report.time > last_visit.time). \
                order_by(Report.time.desc()). \
                all()
        else:
            return self.reports.order_by(Report.time.desc()).all()

    def get_history(self):
        history = []

        for visit in self.visits.all():
            history.append({
                "time": visit.time,
                "message": "Visited and maintenance performed: " + visit.action
            })

        for report in self.reports.all():
            history.append({
                "time": report.time,
                "message": "Reported as: " + report.state
            })

        for location in self.locations:
            history.append({
                "time": location.time,
                "message": "Location set to " + str(location.lat) + "," +
                           str(location.lng) + " (" + location.description +
                           " on level " + str(location.level) + ")"
            })

        for capacity in self.capacities:
            history.append({
                "time": capacity.time,
                "message": "Capacity set to " + str(capacity.crates)
            })

        history.append({
            "time": self.time,
            "message": "Drop point created."
        })

        return sorted(history, key=lambda k: k["time"], reverse=True)

    def get_visit_interval(self):
        """Get the visit interval for this drop point.

        This method returns the visit interval for this drop point
        in seconds.

        This is not implemented as a static method or a constant
        since in the future the visit interval might depend on
        capacity or location of drop points, time of day or a
        combination of those.
        """

        # TODO:
        # currently fixed at 2 hours (in seconds). the base interval
        # should be stored in the configuration or something.

        return 120 * 60

    def get_priority(self):
        """Get the priority to visit this drop point.

        The priority to visit a drop point mainly depends on the
        number and weight of reports since the last visit and
        the capacity of the drop point (larger: more important).

        In addition, priority increases with time since the last
        visit even if the states of reports indicate a low priority.
        This ensures that every drop point is visited from time to
        time.
        """

        # The priority of a removed drop point obviously is always 0.
        if self.removed:
            return 0

        new_reports = self.get_new_reports()

        # This is the starting priority. The report weight should
        # be scaled relative to 1, so this can be interpreted as a
        # number of standing default reports ensuring that every
        # drop point's priority increases slowly if it is not
        # visited even if no real reports come in.
        priority = 1

        for report in new_reports:
            priority += report.get_weight()

        if self.get_current_crate_count() >= 1:
            priority *= (1 + 0.1 * self.get_current_crate_count())

        if self.get_last_visit():
            priority *= (datetime.today() -
                         self.get_last_visit().time).total_seconds() \
                        / self.get_visit_interval()
        else:
            priority *= 3

        return round(priority, 2)

    @staticmethod
    def get(number):
        try:
            return db.session.query(DropPoint).get(number)
        except TypeError:
            return None

    @staticmethod
    def get_all_dps_as_geojson():
        """Get all drop points as a GeoJSON string."""

        arr = []

        for dp in db.session.query(DropPoint).all():
            arr.append({
                "type": "Feature",
                "properties": {
                    "number": dp.number,
                    "description": dp.get_current_location().description,
                    "reports_total": dp.get_total_report_count(),
                    "reports_new": dp.get_new_report_count(),
                    "priority": dp.get_priority(),
                    "last_state": dp.get_last_state(),
                    "crates": dp.get_current_crate_count(),
                    "removed": True if dp.removed else False
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        dp.get_current_location().lng,
                        dp.get_current_location().lat
                    ]
                }
            })

        return json.dumps(arr, indent=4 if c3bottles.debug else None)

    def __repr__(self):
        return "Drop point %s (%s)" % (
            self.number,
            "inactive" if self.removed else "active"
        )

# vim: set expandtab ts=4 sw=4:
