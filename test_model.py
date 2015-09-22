#!/usr/bin/python

import os
import tempfile
import unittest

from datetime import datetime, timedelta
from flask.ext.sqlalchemy import BaseQuery

from c3bottles import c3bottles, db
from model import DropPoint, Location, Capacity, Report, Visit


class c3bottlesModelTestCase(unittest.TestCase):
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

        dp = DropPoint(dp_number)
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
            dp.locations,
            "Drop point has a location."
        )

        self.assertFalse(
            dp.capacities,
            "Drop point has a capacity."
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

    def test_drop_point_construction_exceptions(self):

        numbers = (-1, 3.14, "foo")

        for num in numbers:
            with self.assertRaisesRegexp(TypeError, "number"):
                DropPoint(num)

        DropPoint(1)
        db.session.commit()

        with self.assertRaisesRegexp(ValueError, "already exists"):
            DropPoint(1)

    def test_drop_point_getters(self):

        dp_number = 1
        default_priority = 3

        dp = DropPoint(dp_number)
        db.session.commit()

        self.assertIsNone(
            dp.get_current_location(),
            "get_current_location() did not return None."
        )

        self.assertEquals(
            dp.get_current_crate_count(), 0,
            "get_current_crate_count() did not return 0."
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

        self.assertEqual(
            dp.get_priority(), default_priority,
            "get_priority() did not return the default priority."
        )

    def test_drop_point_construction_with_placement(self):

        dp_number = 2
        location_description = "somewhere"
        location_coordinates = (23.5, 0, -42)
        crate_count = 3
        start_time = datetime.today() - timedelta(hours=1)

        dp = DropPoint(
            dp_number,
            placed=True,
            loc_desc=location_description,
            loc_coords=location_coordinates,
            crates=crate_count,
            start_time=start_time
        )

        db.session.commit()

        self.assertIsInstance(
            dp.locations[0], Location,
            "Drop point has no Location object."
        )

        self.assertIsInstance(
            dp.capacities[0], Capacity,
            "Drop point has no Capacity object."
        )

        self.assertEqual(
            dp.locations[0].description, location_description,
            "Location description not as expected."
        )

        coords = (
            dp.locations[0].coordinate_x,
            dp.locations[0].coordinate_y,
            dp.locations[0].coordinate_z
        )

        self.assertEqual(
            coords, location_coordinates,
            "Location coordinates not as expected."
        )

        self.assertEqual(
            dp.locations[0].start_time, start_time,
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
            dp.capacities[0].start_time, start_time,
            "Capacity start time not as expected."
        )

    def test_location_addition_to_drop_point(self):

        dp_number = 3
        first_location_description = "here"
        first_location_coordinates = (-23.5, 42, 0.1337)
        second_location_description = "there"
        second_location_coordinates = (42.23, -0.5, -3.14159)
        first_time = datetime.today() - timedelta(hours=2)
        second_time = datetime.today() - timedelta(hours=2 - 1)

        dp = DropPoint(
            dp_number,
            placed=True,
            loc_desc=first_location_description,
            loc_coords=first_location_coordinates,
            start_time=first_time
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
            description=second_location_description,
            coords=second_location_coordinates,
            start_time=second_time
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
            dp.locations[1].start_time -
            dp.locations[0].start_time,
            second_time - first_time,
            "Wrong time difference between locations."
        )

    def test_location_construction_exceptions(self):

        dp = DropPoint(1)

        with self.assertRaisesRegexp(TypeError, "drop point"):
            Location("foo")

        time_in_future = datetime.today() + timedelta(hours=1)

        with self.assertRaisesRegexp(ValueError, "future"):
            Location(dp, time_in_future)

        with self.assertRaisesRegexp(TypeError, "not a datetime"):
            Location(dp, "foo")

        start_time = datetime.today()

        with self.assertRaisesRegexp(ValueError, "older than current"):
            Location(dp, start_time=start_time)
            db.session.commit()
            Location(dp, start_time=start_time - timedelta(hours=1))

        invalid_coords = ((1, 2), (2, -3, "foo"), "bar")

        for coords in invalid_coords:
            with self.assertRaisesRegexp(TypeError, "coordinates"):
                Location(dp, coords=coords)

        invalid_description = 3.14

        with self.assertRaisesRegexp(TypeError, "not a string"):
            Location(dp, description=invalid_description)

        too_long_description = "a" * (Location.max_description + 1)

        with self.assertRaisesRegexp(ValueError, "too long"):
            Location(dp, description=too_long_description)

    def test_capacity_addition_to_drop_point(self):

        dp_number = 3
        first_crate_count = 5
        second_crate_count = 2
        first_time = datetime.today() - timedelta(hours=2)
        second_time = datetime.today() - timedelta(hours=2 - 1)

        dp = DropPoint(
            dp_number,
            placed=True,
            crates=first_crate_count,
            start_time=first_time
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
            start_time=second_time
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
            dp.get_current_crate_count(), second_crate_count,
            "Current crate count is not second crate count."
        )

        self.assertEqual(
            dp.capacities[1].start_time -
            dp.capacities[0].start_time,
            second_time - first_time,
            "Wrong time difference between capacities."
        )

    def test_capacity_construction(self):

        dp = DropPoint(1)

        capacity = Capacity(dp)
        db.session.commit()

        self.assertEqual(
            dp.capacities[0], capacity,
            "Capacity of drop point not capacity object created."
        )

        self.assertEqual(
            capacity.crates, Capacity.default_crate_count,
            "Crate count not default crate count."
        )

    def test_capacity_construction_exceptions(self):

        dp = DropPoint(1)

        with self.assertRaisesRegexp(TypeError, "drop point"):
            Capacity("foo")

        time_in_future = datetime.today() + timedelta(hours=1)

        with self.assertRaisesRegexp(ValueError, "future"):
            Capacity(dp, time_in_future)

        with self.assertRaisesRegexp(TypeError, "not a datetime"):
            Capacity(dp, "foo")

        start_time = datetime.today()

        with self.assertRaisesRegexp(ValueError, "older than current"):
            Capacity(dp, start_time=start_time)
            db.session.commit()
            Capacity(dp, start_time=start_time - timedelta(hours=1))

        invalid_crate_counts = (-1, 2.5, "some")

        for count in invalid_crate_counts:
            with self.assertRaisesRegexp(TypeError, "crate count"):
                Capacity(dp, crates=count)

    def test_drop_point_removal(self):

        dp = DropPoint(1)

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

        dp = DropPoint(2)

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

        dp = DropPoint(1)

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
