from datetime import datetime, timedelta

from c3bottles import db
from c3bottles.model.drop_point import DropPoint
from c3bottles.model.visit import Visit
from c3bottles.model.report import Report

from test import C3BottlesTestCase


class VisitTestCase(C3BottlesTestCase):

    def test_construction_exceptions(self):

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

    def test_construction(self):

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

    def test_priority_calculation(self):
        pass  # TODO
