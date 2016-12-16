#!/usr/bin/python

import sys
import unittest

from datetime import datetime, timedelta
from flask_sqlalchemy import BaseQuery

from controller import c3bottles, db
from model.drop_point import DropPoint
from model.location import Location
from model.report import Report
from model.visit import Visit

print("Tests running with Python %s.%s" % (sys.version_info[0], sys.version_info[1]))

def load_config():
    c3bottles.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    c3bottles.config['TESTING'] = True

class C3bottlesModelTestCase(unittest.TestCase):
    def setUp(self):
        load_config()
        self.c3bottles = c3bottles.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_drop_point_construction(self):

        dp_number = 1
        time = datetime.today() - timedelta(hours=1)
        description = "somewhere"
        lat = 20
        lng = 10
        level = 2

        dp = DropPoint(
            dp_number,
            time=time,
            description=description,
            lat=lat,
            lng=lng,
            level=level
        )

        db.session.commit()

        self.assertEqual(
            db.session.query(DropPoint).get(dp_number), dp,
            "Drop point from DB session is not drop point created."
        )

        self.assertEqual(
            dp.number, dp_number,
            "Wrong drop point number"
        )

        self.assertFalse(
            dp.removed,
            "Drop point is removed."
        )

        self.assertIsInstance(
            dp.reports, BaseQuery,
            "Reports are not a query object."
        )

        self.assertFalse(
            dp.reports.all(),
            "Drop point has reports."
        )

        self.assertIsInstance(
            dp.visits, BaseQuery,
            "Visits are not a query object."
        )

        self.assertFalse(
            dp.visits.all(),
            "Drop point has visits."
        )

        self.assertIsInstance(
            dp.locations[0], Location,
            "Drop point has no Location object."
        )

        self.assertEqual(
            dp.time, time,
            "Drop point creation time not as expected."
        )

        self.assertEqual(
            dp.locations[0].description, description,
            "Location description not as expected."
        )

        self.assertEqual(
            dp.locations[0].lat, lat,
            "Latitude not as expected."
        )

        self.assertEqual(
            dp.locations[0].lng, lng,
            "Longitude not as expected."
        )

        self.assertEqual(
            dp.locations[0].level, level,
            "Building level not as expected."
        )

        self.assertEqual(
            dp.locations[0].time, time,
            "Location start time not as expected."
        )

    def test_drop_point_construction_exceptions(self):

        dp_number = 1

        DropPoint(dp_number, lat=0, lng=0, level=1)

        db.session.commit()

        with self.assertRaisesRegexp(ValueError, "already exists"):
            DropPoint(dp_number, lat=0, lng=0, level=1)

        numbers = (-1, "foo", None)

        for num in numbers:
            with self.assertRaisesRegexp(ValueError, "number"):
                DropPoint(num, lat=0, lng=0, level=1)

        time_in_future = datetime.today() + timedelta(hours=1)

        with self.assertRaisesRegexp(ValueError, "future"):
            DropPoint(dp_number, time=time_in_future, lat=0, lng=0, level=1)

        with self.assertRaisesRegexp(ValueError, "not a datetime"):
            DropPoint(dp_number, time="foo", lat=0, lng=0, level=1)

    def test_drop_point_getters(self):

        dp_number = 1
        time = datetime.today()

        dp = DropPoint(
            dp_number,
            time=time,
            lat=0,
            lng=0,
            level=1
        )

        db.session.commit()

        self.assertEqual(
            DropPoint.get(dp_number), dp,
            "DropPoint.get() did not return the drop point created."
        )

        wrong_numbers = (dp_number+1, -1, "foo", None)

        for number in wrong_numbers:
            self.assertIsNone(
                DropPoint.get(number),
                "DropPoint.get() for wrong number number did not return None."
            )

        self.assertIsInstance(
            dp.get_current_location(), Location,
            "get_current_location() is not a Location object."
        )

        self.assertEqual(
            dp.get_last_state(), Report.states[1],
            "get_last_state() did not return the default state."
        )

        self.assertEqual(
            dp.get_total_report_count(), 0,
            "get_total_report_count() did not return 0."
        )

        self.assertEqual(
            dp.get_new_report_count(), 0,
            "get_new_report_count() did not return 0."
        )

        self.assertFalse(
            dp.get_last_visit(),
            "get_last_visit() returned something not False."
        )

        self.assertFalse(
            dp.get_last_report(),
            "get_last_report() returned something not False."
        )

        self.assertFalse(
            dp.get_new_reports(),
            "get_new_reports() returned something not False."
        )

        self.assertGreater(
            dp.get_visit_interval(), 0,
            "get_visit_interval() returned a value <= 0."
        )

        self.assertIsInstance(
            dp.get_history(), list,
            "get_history() did not return a list."
        )

        for elem in dp.get_history():
            self.assertIsInstance(
                elem, dict,
                "get_history() did not return a list of dicts."
            )

        # The history should have 2 entries:
        # 1. drop point creation
        # 2. location setting
        assumed_history_length = 2

        self.assertEqual(
            len(dp.get_history()), assumed_history_length,
            "get_history() does not have a length of 3."
        )

        self.assertIsInstance(
            DropPoint.get_dps_json(), str,
            "get_dps_json() did not return a string."
        )

        self.assertGreater(
            len(DropPoint.get_dps_json()), 1,
            "get_dps_json() did return a string too short."
        )

        self.assertEqual(
            DropPoint.get_dps_json(datetime.today()), "{}",
            "get_dps_json() for now did not return an empty JSON object."
        )

        self.assertEqual(
            DropPoint.get_dps_json(datetime.today()), "{}",
            "get_dps_json() JSON object for now not empty."
        )

        self.assertEqual(
            DropPoint.get_dps_json(time), "{}",
            "get_dps_json() JSON object for creation time not empty."
        )

        self.assertNotEqual(
            DropPoint.get_dps_json(time - timedelta(seconds=1)), "{}",
            "get_dps_json() JSON object for time < creation time empty."
        )

    def test_location_addition_to_drop_point(self):

        dp_number = 3
        first_description = "here"
        first_lat = -23.5
        first_lng = 84
        first_level = 3
        second_description = "there"
        second_lat = 3.14
        second_lng = -2.71828
        second_level = 2
        first_time = datetime.today() - timedelta(hours=2)
        second_time = datetime.today() - timedelta(hours=2 - 1)

        dp = DropPoint(
            dp_number,
            description=first_description,
            lat=first_lat,
            lng=first_lng,
            level=first_level,
            time=first_time
        )

        db.session.commit()

        self.assertEqual(
            len(dp.locations), 1,
            "Drop point does not have exactly one location."
        )

        self.assertEqual(
            db.session.query(Location).count(), 1,
            "Not exactly one location in the database."
        )

        second_location = Location(
            dp,
            description=second_description,
            lat=second_lat,
            lng=second_lng,
            level=second_level,
            time=second_time
        )

        db.session.commit()

        self.assertEqual(
            len(dp.locations), 2,
            "Drop point does not have exactly two locations."
        )

        self.assertEqual(
            db.session.query(Location).count(), 2,
            "Not exactly two locations in the database."
        )

        self.assertEqual(
            dp.get_current_location(), second_location,
            "Current drop point location is not second location."
        )

        self.assertEqual(
            dp.locations[1].time -
            dp.locations[0].time,
            second_time - first_time,
            "Wrong time difference between locations."
        )

    def test_location_construction_exceptions(self):

        dp = DropPoint(1, lat=0, lng=0, level=1)

        with self.assertRaisesRegexp(ValueError, "drop point"):
            Location("foo")

        time_in_future = datetime.today() + timedelta(hours=1)

        with self.assertRaisesRegexp(ValueError, "future"):
            Location(dp, time=time_in_future, lat=0, lng=0, level=1)

        with self.assertRaisesRegexp(ValueError, "not a datetime"):
            Location(dp, time="foo", lat=0, lng=0, level=1)

        start_time = datetime.today()

        with self.assertRaisesRegexp(ValueError, "older than current"):
            Location(dp, time=start_time, lat=0, lng=0, level=1)
            db.session.commit()
            Location(dp, time=start_time - timedelta(hours=1))

        invalid_lat = ("foo", -180, 91, None)
        invalid_lng = ("bar", -181, 251.5, None)
        invalid_level = ("quux", None)

        for lat in invalid_lat:
            with self.assertRaisesRegexp(ValueError, "lat"):
                Location(dp, lat=lat, lng=0, level=1)

        for lng in invalid_lng:
            with self.assertRaisesRegexp(ValueError, "lng"):
                Location(dp, lat=0, lng=lng, level=1)

        for level in invalid_level:
            with self.assertRaisesRegexp(ValueError, "level"):
                Location(dp, lat=0, lng=0, level=level)

        too_long = "a" * (Location.max_description + 1)

        with self.assertRaisesRegexp(ValueError, "too long"):
            Location(dp, lat=0, lng=0, level=1, description=too_long)

    def test_drop_point_removal(self):

        dp = DropPoint(1, lat=0, lng=0, level=1)

        self.assertFalse(
            dp.removed,
            "Freshly created drop point is removed."
        )

        removal_time = datetime.today()

        dp.remove(time=removal_time)

        self.assertIsInstance(
            dp.removed, datetime,
            "Drop point not removed or removal time not datetime."
        )

        self.assertEqual(
            dp.removed, removal_time,
            "Removal time of drop point not time given."
        )

        dp = DropPoint(2, lat=0, lng=0, level=1)

        dp.remove()

        self.assertIsInstance(
            dp.removed, datetime,
            "Drop point not removed or removal time not datetime."
        )

        self.assertEqual(
            dp.get_priority(), 0,
            "Non-zero visit priority of a removed drop point."
        )

    def test_drop_point_removal_exceptions(self):

        dp = DropPoint(1, lat=0, lng=0, level=1)

        time_in_future = datetime.today() + timedelta(hours=1)

        with self.assertRaisesRegexp(ValueError, "future"):
            dp.remove(time_in_future)

        with self.assertRaisesRegexp(TypeError, "not a datetime"):
            dp.remove("foo")

        with self.assertRaisesRegexp(RuntimeError, "already removed"):
            dp.remove()
            dp.remove()

    def test_drop_point_reporting(self):

        states = Report.states

        dp = DropPoint(1, lat=0, lng=0, level=1)

        first_time = datetime.today()
        first_state = states[0]
        first_report = Report(dp, state=first_state, time=first_time)

        db.session.commit()

        self.assertEqual(
            first_report.time, first_time,
            "Report creation time not as expected."
        )

        self.assertEqual(
            first_report.state, first_state,
            "Report state not as expected."
        )

        self.assertEqual(
            dp.reports[0], first_report,
            "First report not first report of associated drop point."
        )

        self.assertEqual(
            dp.get_last_report(), first_report,
            "get_last_report() did not return first report."
        )

        self.assertEqual(
            dp.get_last_state(), first_state,
            "get_last_state() did not return state."
        )

        self.assertEqual(
            dp.get_total_report_count(), 1,
            "get_total_report_count() not as expected."
        )

        self.assertEqual(
            dp.get_new_report_count(), 1,
            "get_new_report_count() not as expected."
        )

        self.assertEqual(
            dp.get_new_reports()[0], first_report,
            "First element returned by get_new_reports() not the report wanted."
        )

        second_time = datetime.today()
        second_state = states[-1]
        second_report = Report(dp, state=second_state, time=second_time)

        db.session.commit()

        self.assertEqual(
            second_report.state, second_state,
            "Report state not as expected."
        )

        self.assertEqual(
            dp.reports[-1], second_report,
            "Second report not last report of associated drop point."
        )

        self.assertEqual(
            dp.get_last_report(), second_report,
            "get_last_report() did not return second report."
        )

        self.assertEqual(
            dp.get_last_state(), second_state,
            "get_last_state() did not return second state."
        )

        self.assertEqual(
            dp.get_total_report_count(), 2,
            "get_total_report_count() not as expected."
        )

        self.assertEqual(
            dp.get_new_report_count(), 2,
            "get_new_report_count() not as expected."
        )

        self.assertEqual(
            dp.get_new_reports()[0], second_report,
            "First element returned by get_new_reports() not the report wanted."
        )

    def test_report_construction_exceptions(self):

        states = Report.states

        dp = DropPoint(1, lat=0, lng=0, level=1)

        with self.assertRaisesRegexp(ValueError, "drop point"):
            Report(None)

        with self.assertRaisesRegexp(ValueError, "state"):
            Report(dp)

        time_in_future = datetime.today() + timedelta(hours=1)

        with self.assertRaisesRegexp(ValueError, "future"):
            Report(dp, time=time_in_future, state=states[0])

        with self.assertRaisesRegexp(ValueError, "not a datetime"):
            Report(dp, time="foo", state=states[0])

        with self.assertRaisesRegexp(ValueError, "state"):
            Report(dp, state="whatever")

    def test_report_weight_calculation(self):
        pass  # TODO

    def test_drop_point_visiting(self):

        actions = Visit.actions

        dp = DropPoint(1, lat=0, lng=0, level=1)

        first_time = datetime.today()
        first_action = actions[1]
        first_visit = Visit(dp, action=first_action, time=first_time)

        db.session.commit()

        self.assertEqual(
            first_visit.time, first_time,
            "Visit creation time not as expected."
        )

        self.assertEqual(
            first_visit.action, first_action,
            "Visit action not as expected."
        )

        self.assertEqual(
            dp.visits[0], first_visit,
            "First visit not first visit of associated drop point."
        )

        self.assertEqual(
            dp.get_last_visit(), first_visit,
            "get_last_visit() did not return first visit."
        )

        report_time = datetime.today()
        report_state = Report.states[0]
        report = Report(dp, state=report_state, time=report_time)

        second_time = datetime.today()
        second_action = actions[0]
        second_visit = Visit(dp, action=second_action, time=second_time)

        db.session.commit()

        self.assertEqual(
            second_visit.action, second_action,
            "Visit action not as expected."
        )

        self.assertEqual(
            dp.visits[-1], second_visit,
            "Second visit not last visit of associated drop point."
        )

        self.assertEqual(
            dp.get_last_visit(), second_visit,
            "get_last_visit() did not return second visit."
        )

        self.assertNotEqual(
            dp.get_last_state(), report_state,
            "get_last_state() returns unchanged state after visit."
        )

        self.assertEqual(
            dp.get_new_report_count(), 0,
            "get_new_report_count() nonzero after visit."
        )

        self.assertFalse(
            dp.get_new_reports(),
            "get_new_reports() returned something not False after visit."
        )

        self.assertEqual(
            dp.get_last_report(), report,
            "get_last_report() did not return report after visit."
        )

        self.assertEqual(
            dp.get_total_report_count(), 1,
            "get_total_report_count() not as expected after visit."
        )

    def test_visit_construction_exceptions(self):

        actions = Visit.actions

        dp = DropPoint(1, lat=0, lng=0, level=1)

        with self.assertRaisesRegexp(ValueError, "drop point"):
            Visit(None)

        with self.assertRaisesRegexp(ValueError, "action"):
            Visit(dp)

        time_in_future = datetime.today() + timedelta(hours=1)

        with self.assertRaisesRegexp(ValueError, "future"):
            Visit(dp, time=time_in_future, action=actions[0])

        with self.assertRaisesRegexp(ValueError, "not a datetime"):
            Visit(dp, time="foo", action=actions[0])

        with self.assertRaisesRegexp(ValueError, "action"):
            Visit(dp, action="whatever")

    def test_drop_point_visit_priority_calculation(self):
        pass  # TODO


if __name__ == "__main__":
    unittest.main()

# vim: set expandtab ts=4 sw=4:
