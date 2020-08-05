import pytest

from datetime import datetime, timedelta

from c3bottles import db
from c3bottles.model.drop_point import DropPoint
from c3bottles.model.location import Location


dp_number = 3
first_description = "here"
first_lat = -23.5
first_lng = 84
first_level = 3
second_description = "there"
second_lat = 3.14
second_lng = -2.71828
second_level = 2
first_time = datetime.now() - timedelta(hours=2)
second_time = datetime.now() - timedelta(hours=2 - 1)


@pytest.fixture
def dp():
    db.session.expunge_all()
    return DropPoint(
        dp_number,
        description=first_description,
        lat=first_lat,
        lng=first_lng,
        level=first_level,
        time=first_time
    )


def test_dp_has_one_location(dp):
    assert len(dp.locations) == 1


def test_database_has_one_location(dp):
    assert db.session.query(Location).count() == 1


@pytest.fixture
def l2(dp):
    return Location(
        dp,
        description=second_description,
        lat=second_lat,
        lng=second_lng,
        level=second_level,
        time=second_time
    )


def test_dp_has_two_locations(dp, l2):
    assert len(dp.locations) == 2


def test_database_has_two_locations(l2):
    assert db.session.query(Location).count() == 2


def test_second_location_is_dp_location(dp, l2):
    assert dp.location == l2


def test_location_time_diff(dp, l2):
    assert dp.locations[1].time - dp.locations[0].time == second_time - first_time


def test_invalid_dp():
    with pytest.raises(ValueError, match="drop point"):
        Location("foo")  # noqa


def test_location_future(dp):
    time_in_future = datetime.today() + timedelta(hours=1)
    with pytest.raises(ValueError, match="future"):
        Location(dp, time=time_in_future, lat=0, lng=0, level=1)


def test_location_invalid_time(dp):
    with pytest.raises(ValueError, match="not a datetime"):
        Location(dp, time="foo", lat=0, lng=0, level=1)  # noqa


def test_new_location_earlier(dp):
    with pytest.raises(ValueError, match="older than current"):
        Location(dp, time=first_time - timedelta(hours=1))


@pytest.mark.parametrize("lat", ["foo", None])
def test_invalid_lat(dp, lat):
    with pytest.raises(ValueError, match="lat"):
        Location(dp, lat=lat, lng=0, level=1)


@pytest.mark.parametrize("lng", ["foo", None])
def test_invalid_lng(dp, lng):
    with pytest.raises(ValueError, match="lng"):
        Location(dp, lat=0, lng=lng, level=1)


@pytest.mark.parametrize("level", ["foo", None])
def test_invalid_level(dp, level):
    with pytest.raises(ValueError, match="level"):
        Location(dp, lat=0, lng=0, level=level)


def test_description_too_long(dp):
    too_long = "a" * (Location.MAX_DESCRIPTION + 1)
    with pytest.raises(ValueError, match="too long"):
        Location(dp, lat=0, lng=0, level=1, description=too_long)
