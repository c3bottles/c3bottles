from datetime import datetime, timedelta
from flask_sqlalchemy import BaseQuery

from c3bottles import db
from c3bottles.model.drop_point import DropPoint
from c3bottles.model.location import Location
from c3bottles.model.report import Report

from test import C3BottlesTestCase


class DropPointTestCase(C3BottlesTestCase):

    def test_construction(self):

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

    def test_construction_exceptions(self):

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

    def test_getters(self):

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

    def test_removal(self):

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

    def test_reporting(self):

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
