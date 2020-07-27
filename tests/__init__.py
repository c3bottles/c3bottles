import unittest

from c3bottles import app, db
from c3bottles.views.user import User


NAME = 'user'
PASSWORD = 'test'


class C3BottlesTestCase(unittest.TestCase):
    def setUp(self):
        self.c3bottles = app.test_client()
        db.create_all()
        self.ctx = app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()
        db.session.remove()
        db.drop_all()

    def create_user(self, user):
        db.session.add(user)
        db.session.commit()
        return User.get(user.user_id)

    def create_test_user(self):
        return self.create_user(User(NAME, PASSWORD))
