"""
Marshmallow schemas can be used to serialize and deserialize models easily
"""
from marshmallow import Schema, fields, post_load, pre_load
from inspectors.extensions import ma
from .models import Survey

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


class InspectionSurveySchema(LookupMixin):
    lookup_fields = ("token")

    class Meta:
        model = Survey
