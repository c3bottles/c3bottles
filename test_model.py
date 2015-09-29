#!/usr/bin/python

import os
import tempfile
import unittest

from datetime import datetime, timedelta
from flask.ext.sqlalchemy import BaseQuery

from c3bottles import c3bottles, db
from model.drop_point import DropPoint
from model.location import Location
from model.capacity import Capacity


class C3bottlesModelTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp_fd, self.tmp_name = tempfile.mkstemp()
        c3bottles.config['SQLALCHEMY_DATABASE_URI'] = \
            "sqlite:///" + self.tmp_name
        c3bottles.config['TESTING'] = True
        self.c3bottles = c3bottles.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.close(self.tmp_fd)
        os.unlink(self.tmp_name)

    def test_drop_point_construction(self):

        dp_number = 1
        time = datetime.today() - timedelta(hours=1)
        description = "somewhere"
        lat = 20
        lng = 10
        level = 2
        crate_count = 3

        dp = DropPoint(
            dp_number,
            time=time,
            description=description,
            lat=lat,
            lng=lng,
            level=level,
            crates=crate_count
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

        self.assertIsInstance(
            dp.capacities[0], Capacity,
            "Drop point has no Capacity object."
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

        self.assertEqual(
            dp.get_current_crate_count(), crate_count,
            "Drop point crate count not as expected."
        )

        self.assertEqual(
            dp.capacities[0].crates, crate_count,
            "Capacity crate count not as expected."
        )

        self.assertEqual(
            dp.capacities[0].time, time,
            "Capacity start time not as expected."
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

    def test_drop_point_getters(self):

        dp = DropPoint(1, lat=0, lng=0, level=1)

        db.session.commit()

        self.assertIsInstance(
            dp.get_current_location(), Location,
            "get_current_location() is not a Location object."
        )

        self.assertEquals(
            dp.get_current_crate_count(), Capacity.default_crate_count,
            "get_current_crate_count() did not return the default crate count."
        )

        self.assertEquals(
            dp.get_total_report_count(), 0,
            "get_total_report_count() did not return 0."
        )

        self.assertEquals(
            dp.get_new_report_count(), 0,
            "get_new_report_count() did not return 0."
        )

        self.assertFalse(
            dp.get_last_visit(),
            "get_last_visit() returned something not False."
        )

        self.assertFalse(
            dp.get_new_reports(),
            "get_new_reports() returned something not False."
        )

        self.assertGreater(
            dp.get_visit_interval(), 0,
            "get_visit_interval() returned a value <= 0."
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

    def test_capacity_addition_to_drop_point(self):

        dp_number = 3
        first_crate_count = 5
        second_crate_count = 2
        first_time = datetime.today() - timedelta(hours=2)
        second_time = datetime.today() - timedelta(hours=2 - 1)

        dp = DropPoint(
            dp_number,
            crates=first_crate_count,
            time=first_time,
            lat=0, lng=0, level=1
        )

        db.session.commit()

        self.assertEqual(
            len(dp.capacities), 1,
            "Drop point does not have exactly one capacity."
        )

        self.assertEqual(
            db.session.query(Capacity).count(), 1,
            "Not exactly one capacity in the database."
        )

        second_capacity = Capacity(
            dp,
            crates=second_crate_count,
            time=second_time
        )

        db.session.commit()

        self.assertEqual(
            len(dp.capacities), 2,
            "Drop point does not have exactly two capacities."
        )

        self.assertEqual(
            db.session.query(Capacity).count(), 2,
            "Not exactly two capacities in the database."
        )

        self.assertEqual(
            dp.capacities[-1], second_capacity,
            "Current capacity is not the second capacity object."
        )

        self.assertEqual(
            dp.get_current_crate_count(), second_crate_count,
            "Current crate count is not second crate count."
        )

        self.assertEqual(
            dp.capacities[1].time -
            dp.capacities[0].time,
            second_time - first_time,
            "Wrong time difference between capacities."
        )

    def test_capacity_construction(self):

        dp = DropPoint(1, lat=0, lng=0, level=1)

        capacity = Capacity(dp)
        db.session.commit()

        self.assertEqual(
            dp.capacities[-1], capacity,
            "Capacity of drop point not capacity object created."
        )

        self.assertEqual(
            capacity.crates, Capacity.default_crate_count,
            "Crate count not default crate count."
        )

    def test_capacity_construction_exceptions(self):

        dp = DropPoint(1, lat=0, lng=0, level=1)

        with self.assertRaisesRegexp(ValueError, "drop point"):
            Capacity("foo")

        time_in_future = datetime.today() + timedelta(hours=1)

        with self.assertRaisesRegexp(ValueError, "future"):
            Capacity(dp, time_in_future)

        with self.assertRaisesRegexp(ValueError, "not a datetime"):
            Capacity(dp, "foo")

        start_time = datetime.today()

        with self.assertRaisesRegexp(ValueError, "older than current"):
            Capacity(dp, time=start_time)
            db.session.commit()
            Capacity(dp, time=start_time - timedelta(hours=1))

        invalid_crate_counts = (-1, "some")

        for count in invalid_crate_counts:
            with self.assertRaisesRegexp(ValueError, "count"):
                Capacity(dp, crates=count)

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
        pass  # TODO

    def test_report_construction_exceptions(self):
        pass  # TODO

    def test_report_weight_calculation(self):
        pass  # TODO

    def test_drop_point_visiting(self):
        pass  # TODO

    def test_visit_construction_exceptions(self):
        pass  # TODO

    def test_drop_point_visit_priority_calculation(self):
        pass  # TODO


if __name__ == "__main__":
    unittest.main()

# vim: set expandtab ts=4 sw=4:
