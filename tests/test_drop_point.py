from datetime import datetime, timedelta

import pytest
from flask_sqlalchemy.query import Query

from c3bottles import app, db
from c3bottles.model.drop_point import DropPoint
from c3bottles.model.location import Location
from c3bottles.model.report import Report

dp_number = 1
creation_time = datetime.now()
description = "somewhere"
lat = 20
lng = 10
level = 2


@pytest.fixture
def dp():
    db.session.expunge_all()
    return DropPoint(
        dp_number, time=creation_time, description=description, lat=lat, lng=lng, level=level
    )


def test_dp_equals_dp_from_db(dp):
    assert db.session.query(DropPoint).get(dp_number) == dp


def test_dp_number_correct(dp):
    assert dp.number == dp_number


def test_dp_not_removed(dp):
    assert dp.removed is None


def test_reports_are_query(dp):
    assert isinstance(dp.reports, Query)


def test_dp_has_no_reports(dp):
    assert not dp.reports.all()


def test_visits_are_query(dp):
    assert isinstance(dp.visits, Query)


def test_dp_has_no_visits(dp):
    assert not dp.visits.all()


def test_dp_has_a_location(dp):
    assert len(dp.locations) == 1


def test_dp_location_is_location(dp):
    assert isinstance(dp.locations[0], Location)


def test_dp_location_desc(dp):
    assert dp.locations[0].description == description


def test_dp_location_lat(dp):
    assert dp.locations[0].lat == lat


def test_dp_location_lng(dp):
    assert dp.locations[0].lng == lng


def test_dp_location_level(dp):
    assert dp.locations[0].level == level


def test_dp_location_time(dp):
    assert dp.locations[0].time == creation_time


def test_dp_creation_time(dp):
    assert dp.time == creation_time


def test_dp_number_unique(dp):
    with pytest.raises(ValueError, match="already exists"):
        DropPoint(dp_number, lat=0, lng=0, level=1)


@pytest.mark.parametrize("num", [-1, "foo", None, False])
def test_dp_invalid_number(num):
    with pytest.raises(ValueError, match="number"):
        DropPoint(num, lat=0, lng=0, level=1)


def test_dp_created_in_future():
    time_in_future = datetime.today() + timedelta(hours=1)
    with pytest.raises(ValueError, match="future"):
        DropPoint(dp_number + 1, time=time_in_future, lat=0, lng=0, level=1)


@pytest.mark.parametrize("time", [-1, "foo", False])
def test_dp_invalid_creation_time(time):
    with pytest.raises(ValueError, match="not a datetime"):
        DropPoint(dp_number + 1, time=time, lat=0, lng=0, level=1)  # noqa


def test_dp_getter_returns_dp(dp):
    assert DropPoint.query.get(dp_number) == dp


@pytest.mark.parametrize("num", [-1, "foo", False, 1234])
def test_dp_getter_return_none_for_nonexistent(num):
    assert DropPoint.query.get(num) is None  # noqa


def test_dp_location_getter_returns_location_object(dp):
    assert isinstance(dp.location, Location)


def test_dp_is_in_default_state(dp):
    assert dp.last_state == Report.states[1]


def test_dp_total_report_count_is_zero(dp):
    assert dp.total_report_count == 0


def test_dp_new_report_count_is_zero(dp):
    assert dp.new_report_count == 0


def test_dp_no_last_visit(dp):
    assert not dp.last_visit


def test_dp_no_last_report(dp):
    assert not dp.last_report


def test_dp_no_new_reports(dp):
    assert not dp.new_reports


def test_dp_visit_interval_greater_zero(dp):
    assert dp.visit_interval > 0


def test_dp_history_is_list(dp):
    assert isinstance(dp.history, list)


def test_dp_history_is_list_of_dicts(dp):
    for entry in dp.history:
        assert type(entry) is dict


def test_dp_history_length(dp):
    # the history should contain the creation
    # and the setting of the initial location
    assert len(dp.history) == 2  # noqa


def test_dps_json_is_string(dp):
    assert type(DropPoint.get_dps_json()) is str


def test_dps_json_is_not_empty(dp):
    assert len(DropPoint.get_dps_json()) > 1


def test_fresh_dps_json_is_empty(dp):
    assert DropPoint.get_dps_json(datetime.now()) == "{}"


def test_dps_json_since_creation_empty(dp):
    assert DropPoint.get_dps_json(creation_time) == "{}"


def test_dps_json_before_creation_not_empty(dp):
    assert DropPoint.get_dps_json(creation_time - timedelta(seconds=1)) != {}


def test_dp_removed_is_datetime(dp):
    dp.remove()
    assert isinstance(dp.removed, datetime)


def test_dp_removed_is_removal_time(dp):
    removal_time = datetime.now()
    dp.remove(removal_time)
    assert dp.removed == removal_time


def test_dp_removed_visit_priority(dp):
    dp.remove()
    assert dp.priority == 0


def test_dp_removal_in_future(dp):
    with pytest.raises(ValueError, match="future"):
        dp.remove(datetime.today() + timedelta(hours=1))


def test_dp_invalid_removal_time(dp):
    with pytest.raises(TypeError, match="not a datetime"):
        dp.remove("foo")  # noqa


def test_dp_already_removed(dp):
    dp.remove()
    with pytest.raises(RuntimeError, match="already removed"):
        dp.remove()


first_report_time = datetime.now()


@pytest.fixture
def first_report(dp):
    return Report(dp, state=Report.states[0], time=first_report_time)


def test_dp_report_time(first_report):
    assert first_report.time == first_report_time


def test_dp_report_state(first_report):
    assert first_report.state == Report.states[0]


def test_dp_report_is_first_report(dp, first_report):
    assert dp.reports[0] == first_report


def test_dp_report_is_last_report(dp, first_report):
    assert dp.last_report == first_report


def test_dp_state_is_reported_state(dp, first_report):
    assert dp.last_state == Report.states[0]


def test_dp_total_report_count(dp, first_report):
    assert dp.total_report_count == 1


def test_dp_new_report_count(dp, first_report):
    assert dp.new_report_count == 1


def test_dp_first_new_report(dp, first_report):
    assert dp.new_reports[0] == first_report  # noqa


second_report_time = datetime.now()


@pytest.fixture
def second_report(dp, first_report):
    return Report(dp, state=Report.states[-1], time=second_report_time)


def test_dp_first_report_is_first_in_list(dp, first_report, second_report):
    assert dp.reports[0] == first_report


def test_dp_second_report_is_returned_as_last(dp, second_report):
    assert dp.last_report == second_report


def test_dp_second_state_is_reported_state(dp, second_report):
    assert dp.last_state == Report.states[-1]


def test_dp_has_two_total_reports(dp, second_report):
    assert dp.total_report_count == 2


def test_dp_has_two_new_reports(dp, second_report):
    assert dp.new_report_count == 2
