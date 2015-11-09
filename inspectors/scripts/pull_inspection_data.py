"""
This script should run daily to:
    pull new data from Socrata
"""
import json
import os

from inspectors.app import create_app
from inspectors.inspections.util import (
            socrata_query,
            load_rows
        )

USE_JSON_CACHE = False
json_cache_path = "data.json"


def json_cache_exists():
    return os.path.exists(json_cache_path)


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


def run():
    app = create_app()
    with app.app_context():
        data = get_data()
        load_rows(data)

if __name__ == '__main__':
    run()

