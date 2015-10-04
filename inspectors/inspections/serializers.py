"""
Marshmallow schemas can be used to serialize and deserialize models easily
"""
from datetime import datetime

from marshmallow import Schema, fields, post_load, pre_load
from inspectors.extensions import ma
from inspectors.extensions import db
from .models import (
        Supervisor,
        Inspector,
        Inspection
        )

class SocrataInspectionSchema(ma.ModelSchema):

    date_inspected = fields.DateTime(
            format="%Y/%m/%d",
            load_from="date")
    permit_description = fields.String(
            load_from="inspection_description")
    display_description = fields.String(
            load_from="disp_description")
    inspector_key = fields.String(load_from="inspector_id")

    def get_instance(self, data):
        """Overrides ModelSchema.get_instance with custom lookup fields"""
        lookup_cols = (
                "date_inspected",
                "permit_number",
                "display_description",
                "inspector_key"
                )
        filters = {
                key: data[key]
                for key in self.fields.keys() if key in lookup_cols
                }
        if None not in filters.values():
            return self.session.query(
                self.opts.model
            ).filter_by(
                **filters
            ).first()
        return None

    class Meta:
        model = Inspection


class SocrataInspectorSchema(ma.ModelSchema):

    inspector_key = fields.String(load_from="inspector_id")
    photo_url = fields.String(load_from="photo")
    supervisor_email = fields.String(load_from="super_email")

    class Meta:
        model = Inspector


class SocrataSupervisorSchema(ma.ModelSchema):

    email = fields.Email(load_from="super_email")
    full_name = fields.String(load_from="super_name")

    class Meta:
        model = Supervisor


supervisor_schema = SocrataSupervisorSchema()
inspector_schema = SocrataInspectorSchema()
inspection_schema = SocrataInspectionSchema()
