import pytest

from controller import db
from model.user import User

from test import C3BottlesTestCase, NAME, PASSWORD


class LoginViewTestCase(C3BottlesTestCase):

    def test_login(self):
        self.create_test_user()

        resp = self.c3bottles.post('/login', data=dict(
            username=NAME,
            password=NAME
            ), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('Wrong user name or password' in str(resp.data))

        resp = self.c3bottles.post('/login', data=dict(
            username=NAME,
            password=PASSWORD
            ), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse('Wrong user name or password' in str(resp.data))
