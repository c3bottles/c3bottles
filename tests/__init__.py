import unittest

from c3bottles import c3bottles, db
from c3bottles.views.user import User


NAME = 'user'
PASSWORD = 'test'


def load_config():
    c3bottles.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    c3bottles.config['TESTING'] = True
    c3bottles.config['WTF_CSRF_ENABLED'] = False
    c3bottles.config['SECRET_KEY'] = 'secret'


class C3BottlesTestCase(unittest.TestCase):
    def setUp(self):
        load_config()
        self.c3bottles = c3bottles.test_client()
        db.create_all()
        self.ctx = c3bottles.test_request_context()
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
