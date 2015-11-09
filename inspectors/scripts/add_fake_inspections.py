from inspectors.extensions import db
from inspectors.app import create_app
from pprint import pprint

from inspectors.inspections.models import Inspection
from inspectors.inspections.mock import make_fake
from inspectors.inspections.util import (
            load_rows
        )


def run():
    app = create_app()
    with app.app_context():
        fake = make_fake()
        load_rows(fake.socrata_rows(800))

if __name__ == '__main__':
    run()
