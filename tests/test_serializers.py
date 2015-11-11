import copy
from flask import current_app
from .test_base import BaseTestCase
from inspectors.inspections.serializers import (
        supervisor_schema,
        inspector_schema,
        inspection_schema,
        )
from inspectors.inspections.util import (
        SchemaLoader
        )
from inspectors.inspections.mock import make_fake


class TestSchemaLoader(BaseTestCase):

    def setUp(self):
        """All names, characters, and incidents appearing in this
            test data are fictitious. Any resemblance to real persons, living or
            dead, is purely coincidental.
        """
        BaseTestCase.setUp(self)
        fake = make_fake()
        self.sample_row = {
                'additional_comments': 'ceiling box, island.',
                'comments_code': 'x2016016074. unit 4 only. unit 3 pending mud rings, ceiling',
                'date': '2015/10/31',
                'dir_email': 'DRT@miamidade.gov',
                'dir_name': 'Tilda Duchamps',
                'dir_phone': '(777) 999-8888',
                'disp_description': 'APPROVED PARTIAL',
                'first_name': 'Jim',
                'input_order': '9999',
                'inspection_description': 'ROUGH',
                'inspector_id': 'JBRECKENRIDGE',
                'job_site_address': '4444 SW 375 CT',
                'last_name': 'Breckenridge',
                'permit_number': '2015062054',
                'permit_type': 'ELEC',
                'photo': 'images\\jpg\\generic.jpg',
                'request_date': '2015-12-25 00:00:00.0',
                'super_email': 'ILDA@miamidade.gov',
                'super_name': 'Ilda Rizzo',
                'super_phone': '(555) 111-2222'
                        }
        self.random_rows = [fake.socrata_row() for i in range(5)]

    def test_adding_rows(self):
        # can be created with no schema
        loader = SchemaLoader(None)
        # add a row
        index = loader.add( self.sample_row )
        self.assertEqual(index, 0)
        # add another row
        index = loader.add( self.random_rows[0] )
        self.assertEqual(index, 1)
        self.assertEqual( len(loader.raw_data), 2 )
        # adding the same row returns the same index
        index = loader.add( self.sample_row )
        self.assertEqual(index, 0)

    def test_slicing_data(self):
        loader = SchemaLoader(supervisor_schema)
        copy_row = copy.copy(self.sample_row)
        # add a row
        index = loader.slice_and_add( self.sample_row )
        self.assertEqual(index, 0)
        self.assertNotIn('permit_number', loader.raw_data[0])
        # editing unused fields shouldn't matter
        copy_row['inspector_id'] = 'LAKSJDHFL'
        index = loader.slice_and_add( copy_row )
        self.assertEqual(index, 0)

    def test_logs_successful_deserialization(self):
        loader = SchemaLoader(supervisor_schema)
        loader.slice_and_add(self.sample_row)
        with self.assertLogs( current_app.logger, level='INFO' ) as cm:
            loader.save_models_or_report_errors()

    def test_logs_deserialization_errors(self):
        loader = SchemaLoader(supervisor_schema)
        copy_row = copy.copy(self.sample_row)
        copy_row['super_email'] = 'not a valid email'
        loader.slice_and_add(copy_row)
        with self.assertLogs( current_app.logger, level='ERROR' ) as cm:
            loader.save_models_or_report_errors()

