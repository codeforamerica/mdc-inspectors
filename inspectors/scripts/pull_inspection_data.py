"""
This script should run daily to:
    pull new data from Socrata
"""
import datetime as dt
import json
import os
from pprint import pprint

import requests

from inspectors.extensions import db
from inspectors.app import create_app
from inspectors.inspections.serializers import (
            supervisor_schema,
            inspector_schema,
            inspection_schema
        )


USE_JSON_CACHE = False
json_cache_path = "data.json"

def slice_data(schema, data):
    keys = []
    for name, field in schema.fields.items():
        if field.load_from:
            keys.append(field.load_from)
        else:
            keys.append(name)
    sliced = {k:data[k] for k in keys if k in data}
    return sliced


def json_cache_exists():
    return os.path.exists(json_cache_path)


def socrata_query():
    timedelta = dt.timedelta(days=-3)
    now = dt.datetime.now()
    three_days_ago = now + timedelta
    date_format = "%Y/%m/%d"
    endpoint = "https://opendata.miamidade.gov/resource/ba6h-bksp.json"
    query = "?$where=date > '{three_days_ago}' AND date < '{now}'".format(
            three_days_ago=three_days_ago.strftime(date_format),
            now=now.strftime(date_format),
            )
    request = requests.get( endpoint + query )
    return request.json()


def get_data():
    if USE_JSON_CACHE:
        if json_cache_exists():
            with open(json_cache_path, 'r') as f:
                data = json.load(f)
        else:
            data = socrata_query()
            with open(json_cache_path, 'w') as f:
                json.dump(data, f)
    else:
        data = socrata_query()

    return data


def index_or_add(items, new_item):
    try:
        index = items.index(new_item)
    except ValueError:
        index = len(items)
        items.append(new_item)
    return index


def load_data():
    data = get_data()

    supervisors = []
    inspectors = []
    inspections = []

    # build up unique raw data instances for each data type
    for row in data:
        supervisor_data = slice_data(supervisor_schema, row)
        inspector_data = slice_data(inspector_schema, row)
        inspection_data = slice_data(inspection_schema, row)

        index_or_add(supervisors, supervisor_data)
        index_or_add(inspectors, inspector_data)
        index_or_add(inspections, inspection_data)

    # parse, validate and get instances if they exist
    supervisors, errors = supervisor_schema.load(supervisors, many=True,
            session=db.session)
    inspectors, errors = inspector_schema.load(inspectors, many=True,
            session=db.session)
    inspections, errors = inspection_schema.load(inspections, many=True,
            session=db.session)

    # save data
    for group in [supervisors, inspectors, inspections]:
        for instance in group:
            db.session.add(instance)
    db.session.commit()


def run():
    app = create_app()
    with app.app_context():
        load_data()

if __name__ == '__main__':
    run()

