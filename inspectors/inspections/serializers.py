"""
Marshmallow schemas can be used to serialize and deserialize models easily
"""
from datetime import datetime
import json
from pprint import pprint

from sqlalchemy import inspect
from flask import current_app
from marshmallow import Schema, fields, post_load, pre_load
from inspectors.extensions import ma
from inspectors.extensions import db
from .models import (
        Supervisor,
        Inspector,
        Inspection
        )

SOCRATA_DATE_FMT = "%Y/%m/%d"

class DataLoader:
    """A class that deduplicates raw data dictionaries,
        and then attempts to serialize them,
            either returning successfully validated models
            or reporting deserialization errors
    """
    def __init__(self, schema):
        self.schema = schema
        self.raw_data = []
        self.models = []

    def add(self, data, many=False):
        """adds data to a raw data set() object
        """
        indices = []
        data = data if many else (data,)
        for d in data:
            try:
                indices.append( self.raw_data.index(d) )
            except ValueError:
                indices.append( len(self.raw_data) )
                self.raw_data.append(d)
        return indices if many else indices[0]


    def slice_and_add(self, data):
        """adds data to the raw data set, but only the subset of keys used by
        the serialization schema
        """
        keys = []
        for name, field in self.schema.fields.items():
            if field.load_from:
                keys.append(field.load_from)
            else:
                keys.append(name)
        sliced = {k:data[k] for k in keys if k in data}
        return self.add(sliced)

    def add_foreign_keys_from(self, other, instance_index_pairs, fk_field_name):
        for i, j in instance_index_pairs:
            own = self.raw_data[i]
            foreign_key_instance = other.models[j]
            own[fk_field_name] = foreign_key_instance.id

    def log_errors(self, errors):
        for i, error in errors.items():
            problematic_datum = self.raw_data[i]
            for key, message in error.items():
                bad_input = problematic_datum[key]
                current_app.logger.error(
                "DESERIALIZATIONERROR: '{field}': '{value}', {message}".format(
                    field=key, value=bad_input, message=message))

    def log_success(self, total, new, existing):
        current_app.logger.debug(
            "DESERIALIZED: {total} {cls} instances, {new} new, {existing} existing".format(
                    total = total,
                    cls = self.schema.opts.model.__name__,
                    new = new,
                    existing = existing,
                    ))

    def save_models_or_report_errors(self):
        """Tries to load data using the schema.
        If there are errors, it will log them.
        If there are no errors, it will save the models and return them
        """
        new = 0
        existing = 0
        total = 0

        models, errors = self.schema.load(
                    self.raw_data,
                    many=True,
                    session=db.session,
                )
        if errors:
            self.log_errors(errors)
        else:
            for m in models:
                if inspect(m).persistent:
                    existing += 1
                else:
                    new += 1
                db.session.add(m)
            db.session.commit()
            self.log_success(len(models), new, existing)
            self.models = models
            return models

class LookupMixin(ma.ModelSchema):

    def get_instance(self, data):
        """Overrides ModelSchema.get_instance with custom lookup fields"""
        filters = {
                key: data[key]
                for key in self.fields.keys() if key in self.lookup_fields
                }
        if None not in filters.values():
            return self.session.query(
                self.opts.model
            ).filter_by(
                **filters
            ).first()
        return None


class SocrataInspectionSchema(LookupMixin):

    lookup_fields = (
            "date_inspected",
            "permit_number",
            "display_description",
            "inspector_id"
            )

    date_inspected = fields.DateTime(
            format=SOCRATA_DATE_FMT,
            load_from="date")
    permit_description = fields.String(
            load_from="inspection_description")
    display_description = fields.String(
            load_from="disp_description")

    class Meta:
        model = Inspection
        fields = (
                'permit_number',
                'date_inspected',
                'permit_type',
                'permit_description',
                'display_description',
                'job_site_address',
                'inspector_id',
                )


class SocrataInspectorSchema(LookupMixin):

    lookup_fields = (
            "inspector_key",
            )

    inspector_key = fields.String(load_from="inspector_id")
    photo_url = fields.String(load_from="photo")

    class Meta:
        model = Inspector
        fields = (
                'inspector_key',
                'first_name',
                'last_name',
                'photo_url',
                'supervisor_id',
                )


class SocrataSupervisorSchema(LookupMixin):

    lookup_fields = (
            "email",
            )

    email = fields.Email(load_from="super_email")
    full_name = fields.String(load_from="super_name")

    class Meta:
        model = Supervisor
        fields = (
                'email',
                'full_name',
                )


supervisor_schema = SocrataSupervisorSchema()
inspector_schema = SocrataInspectorSchema()
inspection_schema = SocrataInspectionSchema()
