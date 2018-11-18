from datetime import datetime, timedelta

from c3bottles.model.drop_point import DropPoint
from c3bottles.model.report import Report

from . import C3BottlesTestCase


class ReportTestCase(C3BottlesTestCase):

    def test_construction_exceptions(self):

        states = Report.states

        dp = DropPoint(1, lat=0, lng=0, level=1)

        with self.assertRaisesRegex(ValueError, "drop point"):
            Report(None)

        with self.assertRaisesRegex(ValueError, "state"):
            Report(dp)

        time_in_future = datetime.today() + timedelta(hours=1)

        with self.assertRaisesRegex(ValueError, "future"):
            Report(dp, time=time_in_future, state=states[0])

        with self.assertRaisesRegex(ValueError, "not a datetime"):
            Report(dp, time="foo", state=states[0])

        with self.assertRaisesRegex(ValueError, "state"):
            Report(dp, state="whatever")

    def test_weight_calculation(self):
        pass  # TODO
