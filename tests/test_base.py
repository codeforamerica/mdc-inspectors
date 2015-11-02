import unittest
from flask.ext.testing import TestCase
from inspectors.app import db, create_app as _create_app
from inspectors.settings import TestConfig

class BaseTestCase(TestCase):

    def create_app(self):
        return _create_app()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.get_engine(self.app).dispose()
