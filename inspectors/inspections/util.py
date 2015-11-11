import datetime as dt

import requests
from flask import current_app
from sqlalchemy import inspect

from inspectors.extensions import db
from inspectors.inspections.serializers import (
            SOCRATA_DATE_FMT,
            supervisor_schema,
            inspector_schema,
            inspection_schema,
        )

def load_rows(rows):
    """Takes rows of raw data from socrata, builds relationships, and passes them
    through deserializers before saving new records.
    """
    relations = []

    supervisors, inspectors, inspections = [SchemaLoader(s) for s in (
            supervisor_schema,
            inspector_schema,
            inspection_schema,
        )]

    for row in rows:
        if row:
            relations.append({
                'supervisor': supervisors.slice_and_add(row),
                'inspector': inspectors.slice_and_add(row),
                'inspection': inspections.slice_and_add(row),
                })

    supervisors.save_models_or_report_errors()

    inspectors.add_foreign_keys_from(
            supervisors,
            [ (r['inspector'], r['supervisor']) for r in relations ],
            'supervisor_id'
            )
    inspectors.save_models_or_report_errors()

    inspections.add_foreign_keys_from(
            inspectors,
            [ (r['inspection'], r['inspector']) for r in relations ],
            'inspector_id'
            )
    inspections.save_models_or_report_errors()


def socrata_query():
    timedelta = dt.timedelta(days=-3)
    now = dt.datetime.now()
    tomorrow = now + dt.timedelta(days=1)
    three_days_ago = now + timedelta
    date_format = SOCRATA_DATE_FMT
    endpoint = "https://opendata.miamidade.gov/resource/ba6h-bksp.json"
    query = "?$where=date > '{three_days_ago}' AND date < '{tomorrow}'".format(
            three_days_ago=three_days_ago.strftime(date_format),
            tomorrow=tomorrow.strftime(date_format),
            )
    request = requests.get( endpoint + query )
    return request.json()


class SchemaLoader:
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
        """Adds data to a raw data set() object
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
        """Adds data to the raw data set, but only the subset of keys used by
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
        current_app.logger.info(
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

