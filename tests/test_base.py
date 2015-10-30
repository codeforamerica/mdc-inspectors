import unittest
from inspectors.app import db, create_app as _create_app
from inspectors.settings import TestConfig
from sqlalchemy.schema import (
    MetaData,
    Table,
    DropTable,
    ForeignKeyConstraint,
    DropConstraint,
)
from flask_testing import TestCase

class BaseTestCase(TestCase):

    def create_app(self):
        return _create_app()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.get_engine(self.app).dispose()


