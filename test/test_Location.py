import unittest

from datetime import datetime, timedelta

from c3bottles import db
from c3bottles.model.drop_point import DropPoint
from c3bottles.model.location import Location

from test import C3BottlesTestCase

class LocationTestCase(C3BottlesTestCase):

    def test_addition_to_drop_point(self):

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

    def test_construction_exceptions(self):

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
