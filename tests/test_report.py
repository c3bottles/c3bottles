from datetime import datetime, timedelta

import pytest

from c3bottles import db
from c3bottles.model.drop_point import DropPoint
from c3bottles.model.report import Report


@pytest.fixture
def dp():
    db.session.expunge_all()
    return DropPoint(number=1, lat=0, lng=0, level=1)


report_time = datetime.now()


@pytest.fixture
def report(dp):
    return Report(dp, time=report_time, state=Report.states[0])


def test_report_time(report):
    assert report.time == report_time


def test_report_state(report):
    assert report.state == Report.states[0]


def test_dp_new_report_count(dp, report):
    assert dp.new_report_count == 1


def test_dp_total_report_count(dp, report):
    assert dp.total_report_count == 1


def test_dp_last_report(dp, report):
    assert dp.last_report == report


def test_report_removed_dp(dp):
    dp.remove()
    with pytest.raises(ValueError, match="removed"):
        Report(dp, state=Report.states[0])


def test_report_none():
    with pytest.raises(ValueError, match="drop point"):
        Report(None)  # noqa


def test_report_missing_state(dp):
    with pytest.raises(ValueError, match="state"):
        Report(dp)


def test_report_future(dp):
    time_in_future = datetime.today() + timedelta(hours=1)
    with pytest.raises(ValueError, match="future"):
        Report(dp, time=time_in_future, state=Report.states[0])


def test_report_not_datetime(dp):
    with pytest.raises(ValueError, match="not a datetime"):
        Report(dp, time="foo", state=Report.states[0])  # noqa


def test_report_wrong_state(dp):
    with pytest.raises(ValueError, match="state"):
        Report(dp, state="whatever")


def test_weight_calculation():
    pass  # TODO
