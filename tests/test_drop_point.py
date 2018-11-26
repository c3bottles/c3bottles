import pytest

from datetime import datetime, timedelta

from flask_sqlalchemy import BaseQuery

from c3bottles import db
from c3bottles.model.drop_point import DropPoint
from c3bottles.model.location import Location
from c3bottles.model.report import Report

from . import C3BottlesTestCase


dp_number = 1
time = datetime.today() - timedelta(hours=1)
description = "somewhere"
lat = 20
lng = 10
level = 2


class BaseDropPointTestCase(C3BottlesTestCase):

    def setUp(self):
        super().setUp()
        self.dp = DropPoint(
            dp_number,
            time=time,
            description=description,
            lat=lat,
            lng=lng,
            level=level
        )
        db.session.commit()


class FreshDropPointTestCase(BaseDropPointTestCase):

    def test_dp_equals_dp_from_db(self):
        assert db.session.query(DropPoint).get(dp_number) == self.dp

    def test_dp_number_correct(self):
        assert self.dp.number == dp_number

    def test_dp_not_removed(self):
        assert self.dp.removed is None

    def test_reports_are_query(self):
        assert isinstance(self.dp.reports, BaseQuery)

    def test_dp_has_no_reports(self):
        assert not self.dp.reports.all()

    def test_visits_are_query(self):
        assert isinstance(self.dp.visits, BaseQuery)

    def test_dp_has_no_visits(self):
        assert not self.dp.visits.all()

    def test_dp_has_a_location(self):
        assert len(self.dp.locations) == 1

    def test_dp_location_is_location(self):
        assert isinstance(self.dp.locations[0], Location)

    def test_dp_location_desc(self):
        assert self.dp.locations[0].description == description

    def test_dp_location_lat(self):
        assert self.dp.locations[0].lat == lat

    def test_dp_location_lng(self):
        assert self.dp.locations[0].lng == lng

    def test_dp_location_level(self):
        assert self.dp.locations[0].level == level

    def test_dp_location_time(self):
        assert self.dp.locations[0].time == time

    def test_dp_creation_time(self):
        assert self.dp.time == time

    @staticmethod
    def test_dp_number_unique():
        with pytest.raises(ValueError) as e:
            DropPoint(dp_number, lat=0, lng=0, level=1)
        assert "already exists" in str(e)

    @staticmethod
    def test_dp_illegal_number():
        for num in [-1, "foo", None]:
            with pytest.raises(ValueError) as e:
                DropPoint(num, lat=0, lng=0, level=1)
            assert "number" in str(e)

    @staticmethod
    def test_dp_created_in_future():
        with pytest.raises(ValueError) as e:
            time_in_future = datetime.today() + timedelta(hours=1)
            DropPoint(dp_number+1, time=time_in_future, lat=0, lng=0, level=1)
        assert "future" in str(e)

    @staticmethod
    def test_dp_invalid_creation_time():
        with pytest.raises(ValueError) as e:
            DropPoint(dp_number + 1, time="foo", lat=0, lng=0, level=1)
        assert "not a datetime" in str(e)

    def test_dp_getter_returns_dp(self):
        assert DropPoint.get(dp_number) == self.dp

    @staticmethod
    def test_dp_getter_return_none_for_nonexistent():
        for num in [-1, "foo", None]:
            assert DropPoint.get(num) is None

    def test_dp_location_getter_returns_location_object(self):
        assert isinstance(self.dp.location, Location)

    def test_dp_is_in_default_state(self):
        assert self.dp.last_state == Report.states[1]

    def test_dp_total_report_count_is_zero(self):
        assert self.dp.total_report_count == 0

    def test_dp_new_report_count_is_zero(self):
        assert self.dp.new_report_count == 0

    def test_dp_no_last_visit(self):
        assert not self.dp.last_visit

    def test_dp_no_last_report(self):
        assert not self.dp.last_report

    def test_dp_no_new_reports(self):
        assert not self.dp.new_reports

    def test_dp_visit_interval_greater_zero(self):
        assert self.dp.visit_interval > 0

    def test_dp_history_is_list(self):
        assert type(self.dp.history) is list

    def test_dp_history_is_list_of_dicts(self):
        for entry in self.dp.history:
            assert type(entry) is dict

    def test_dp_history_length(self):
        # the history should contain the creation
        # and the setting of the initial location
        assert len(self.dp.history) == 2

    @staticmethod
    def test_dps_json_is_string():
        assert type(DropPoint.get_dps_json()) is str

    @staticmethod
    def test_dps_json_is_not_empty():
        assert len(DropPoint.get_dps_json()) > 1

    @staticmethod
    def test_fresh_dps_json_is_empty():
        assert DropPoint.get_dps_json(datetime.today()) == "{}"

    @staticmethod
    def test_dps_json_since_creation_empty():
        assert DropPoint.get_dps_json(time) == "{}"

    @staticmethod
    def test_dps_json_before_creation_not_empty():
        assert DropPoint.get_dps_json(time - timedelta(seconds=1)) != {}

    def test_dp_removal(self):
        self.dp.remove()
        assert self.dp.removed is not None

    def test_dp_removed_is_datetime(self):
        self.dp.remove()
        assert isinstance(self.dp.removed, datetime)

    def test_dp_removed_is_removal_time(self):
        removal_time = datetime.today()
        self.dp.remove(removal_time)
        assert self.dp.removed == removal_time

    def test_dp_removed_visit_priority(self):
        self.dp.remove()
        assert self.dp.priority == 0

    def test_dp_removal_in_future(self):
        with pytest.raises(ValueError) as e:
            self.dp.remove(datetime.today() + timedelta(hours=1))
        assert "future" in str(e)

    def test_dp_invalid_removal_time(self):
        with pytest.raises(TypeError) as e:
            self.dp.remove("foo")
        assert "not a datetime" in str(e)

    def test_dp_already_removed(self):
        self.dp.remove()
        with pytest.raises(RuntimeError) as e:
            self.dp.remove()
        assert "already removed" in str(e)


class OnceReportedDropPointTestCase(BaseDropPointTestCase):

    def setUp(self):
        super().setUp()
        self.report_time = datetime.today()
        self.report_state = Report.states[0]
        self.report = Report(
            self.dp, state=self.report_state, time=self.report_time
        )
        db.session.commit()

    def test_dp_report_time(self):
        assert self.report.time == self.report_time

    def test_dp_report_state(self):
        assert self.report.state == self.report_state

    def test_dp_report_is_first_report(self):
        assert self.dp.reports[0] == self.report

    def test_dp_report_is_last_report(self):
        assert self.dp.last_report == self.report

    def test_dp_state_is_reported_state(self):
        assert self.dp.last_state == self.report_state

    def test_dp_total_report_count(self):
        assert self.dp.total_report_count == 1

    def test_dp_new_report_count(self):
        assert self.dp.new_report_count == 1

    def test_dp_first_new_report(self):
        assert self.dp.new_reports[0] == self.report


class TwiceReportedDropPointTestCase(BaseDropPointTestCase):

    def setUp(self):
        super().setUp()
        self.report_time_1 = datetime.today()
        self.report_state_1 = Report.states[0]
        self.report_time_2 = datetime.today()
        self.report_state_2 = Report.states[-1]
        self.report_1 = Report(
            self.dp, state=self.report_state_1, time=self.report_time_1
        )
        self.report_2 = Report(
            self.dp, state=self.report_state_2, time=self.report_time_2
        )
        db.session.commit()

    def test_dp_first_report_is_first_in_list(self):
        assert self.dp.reports[0] == self.report_1

    def test_dp_second_report_is_last_in_list(self):
        assert self.dp.reports[-1] == self.report_2

    def test_dp_second_report_is_returned_as_last(self):
        assert self.dp.last_report == self.report_2

    def test_dp_second_state_is_reported_state(self):
        assert self.dp.last_state == self.report_state_2

    def test_dp_has_two_total_reports(self):
        assert self.dp.total_report_count == 2

    def test_dp_has_two_new_reports(self):
        assert self.dp.new_report_count == 2
