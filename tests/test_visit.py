import pytest

from datetime import datetime, timedelta

from c3bottles import db
from c3bottles.model.drop_point import DropPoint
from c3bottles.model.visit import Visit
from c3bottles.model.report import Report


@pytest.fixture
def dp():
    db.session.expunge_all()
    return DropPoint(number=1, lat=0, lng=0, level=1)


def test_visit_none():
    with pytest.raises(ValueError, match="drop point"):
        Visit(None)  # noqa


def test_visit_missing_action(dp):
    with pytest.raises(ValueError, match="action"):
        Visit(dp)


def test_visit_future(dp):
    time_in_future = datetime.today() + timedelta(hours=1)
    with pytest.raises(ValueError, match="future"):
        Visit(dp, time=time_in_future, action=Visit.actions[0])


def test_visit_not_datetime(dp):
    with pytest.raises(ValueError, match="not a datetime"):
        Visit(dp, time="foo", action=Visit.actions[0])  # noqa


def test_visit_wrong_action(dp):
    with pytest.raises(ValueError, match="action"):
        Visit(dp, action="whatever")


first_time = datetime.today()
first_action = Visit.actions[1]


@pytest.fixture
def first_visit(dp):
    return Visit(dp, action=first_action, time=first_time)


def test_visit_time(first_visit):
    assert first_visit.time == first_time


def test_visit_action(first_visit):
    assert first_visit.action == first_action


def test_dp_visits(dp, first_visit):
    assert dp.visits[0] == first_visit


def test_dp_last_visit(dp, first_visit):
    assert dp.last_visit == first_visit


report_time = datetime.today()
report_state = Report.states[0]


@pytest.fixture
def report(dp):
    return Report(dp, state=report_state, time=report_time)


def test_report_state(dp, report):
    assert dp.last_state == report_state


def test_new_report_count(dp, report):
    assert dp.new_report_count == 1


second_time = datetime.today()
second_action = Visit.actions[0]


@pytest.fixture
def second_visit(dp, first_visit):
    return Visit(dp, action=second_action, time=second_time)


def test_second_visit_action(second_visit):
    assert second_visit.action == second_action


def test_second_visit_dp_visits(dp, second_visit):
    assert dp.visits[-1] == second_visit


def test_second_visit_last_visit(dp, second_visit):
    assert dp.last_visit == second_visit


def test_second_visit_last_state(dp, second_visit):
    assert dp.last_state == Report.states[-1]


def test_second_visit_new_report_count(dp, second_visit):
    assert dp.new_report_count == 0


def test_second_visit_no_new_reports(dp, second_visit):
    assert not dp.new_reports


def test_second_visit_last_report(dp, report, second_visit):
    assert dp.last_report == report


def test_second_visit_total_report_count(dp, report, second_visit):
    assert dp.total_report_count == 1


def test_priority_calculation():
    pass  # TODO
