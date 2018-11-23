from datetime import datetime, timedelta

from c3bottles import db
from c3bottles.model.drop_point import DropPoint
from c3bottles.model.visit import Visit
from c3bottles.model.report import Report

from . import C3BottlesTestCase


class VisitTestCase(C3BottlesTestCase):

    def test_construction_exceptions(self):

        actions = Visit.actions

        dp = DropPoint(1, lat=0, lng=0, level=1)

        with self.assertRaisesRegex(ValueError, "drop point"):
            Visit(None)

        with self.assertRaisesRegex(ValueError, "action"):
            Visit(dp)

        time_in_future = datetime.today() + timedelta(hours=1)

        with self.assertRaisesRegex(ValueError, "future"):
            Visit(dp, time=time_in_future, action=actions[0])

        with self.assertRaisesRegex(ValueError, "not a datetime"):
            Visit(dp, time="foo", action=actions[0])

        with self.assertRaisesRegex(ValueError, "action"):
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
            dp.last_visit, first_visit,
            "last_visit did not return first visit."
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
            dp.last_visit, second_visit,
            "last_visit did not return second visit."
        )

        self.assertNotEqual(
            dp.last_state, report_state,
            "last_state returns unchanged state after visit."
        )

        self.assertEqual(
            dp.new_report_count, 0,
            "new_report_count nonzero after visit."
        )

        self.assertFalse(
            dp.new_reports,
            "new_reports returned something not False after visit."
        )

        self.assertEqual(
            dp.last_report, report,
            "last_report did not return report after visit."
        )

        self.assertEqual(
            dp.total_report_count, 1,
            "total_report_count not as expected after visit."
        )

    def test_priority_calculation(self):
        pass  # TODO
