"""
Marshmallow schemas can be used to serialize and deserialize models easily
"""
from marshmallow import Schema, fields, post_load, pre_load
from inspectors.extensions import ma
from .models import (
    Supervisor, Inspector, Inspection
)

SOCRATA_DATE_FMT = "%Y/%m/%d"


class LookupMixin(ma.ModelSchema):

    def get_instance(self, data):
        """Overrides ModelSchema.get_instance with custom lookup fields"""
        filters = {
            key: data[key]
            for key in self.fields.keys() if key in self.lookup_fields}

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
        "inspector_id")

    date_inspected = fields.DateTime(
        format=SOCRATA_DATE_FMT,
        load_from="date",
        required=True)
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
            'inspector_id')


class SocrataInspectorSchema(LookupMixin):

    lookup_fields = ("inspector_key")

    inspector_key = fields.String(load_from="inspector_id", required=True)
    photo_url = fields.String(load_from="photo")

    class Meta:
        model = Inspector
        fields = (
            'inspector_key',
            'first_name',
            'last_name',
            'photo_url',
            'supervisor_id')


class SocrataSupervisorSchema(LookupMixin):

    # comma is required; this is a tuple!
    lookup_fields = ("email",)

    email = fields.Email(load_from="super_email", required=True)
    full_name = fields.String(load_from="super_name", required=True)

    class Meta:
        model = Supervisor
        fields = (
            'email',
            'full_name')


supervisor_schema = SocrataSupervisorSchema()
inspector_schema = SocrataInspectorSchema()
inspection_schema = SocrataInspectionSchema()
