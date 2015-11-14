from unittest import TestCase

from mock import Mock
from marshmallow import Schema, fields

from inspectors.inspections.util import (
        SchemaLoader
        )
"""What should my tests check?
    They should ensure that things work as I expect
    They should ensure that it handles likely problems in the right way
"""

class FakeModelSchema(Schema):
    a_field = fields.Integer(load_from="a", required=True)
    b_field = fields.Integer(load_from="b")
    c = fields.Integer()

    class Meta:
        fields = (
                'a_field',
                'b_field',
                'c',
                )

class TestSchemaLoader(TestCase):

    def setUp(self):
        self.datum = { "a": 1, "b": 2, "c": 3, "d": 4 }
        self.datum2 = { "a": 1, "b": 2  }
        self.data = [self.datum, self.datum2]
        self.loader = SchemaLoader(FakeModelSchema())

    def test_slice(self):
        sliced = self.loader._slice(self.datum)
        self.assertSetEqual(set(['a','b','c']), set(sliced.keys()))

    def test_slice_and_add_data(self):
        self.assertEquals(self.loader.slice_and_add(self.datum), 0)
        self.assertEquals(self.loader.slice_and_add(self.datum2), 1)
        self.assertEquals(self.loader.slice_and_add(self.datum), 0)

    def test_slice_and_add_empty(self):
        self.assertEquals(self.loader.slice_and_add({}), 0)

    def test_slice_and_add_multiple(self):
        for ix, d in enumerate(self.data):
            self.assertEqual(self.loader.slice_and_add(d), ix)











