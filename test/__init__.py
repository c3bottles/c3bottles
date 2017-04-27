import unittest

from controller import c3bottles, db

def load_config():
    c3bottles.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    c3bottles.config['TESTING'] = True

class C3BottlesTestCase(unittest.TestCase):
    def setUp(self):
        load_config()
        self.c3bottles = c3bottles.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
