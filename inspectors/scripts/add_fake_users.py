from inspectors.extensions import db
from inspectors.app import create_app
from pprint import pprint

from inspectors.inspections.models import Inspection
from inspectors.registration.models import User
from inspectors.registration.mock import make_generator


def run():
    app = create_app()
    with app.app_context():
        fake = make_generator()
        users = fake.inspections_users(40)
        for u in users:
            db.session.add(u)
        db.session.commit()

if __name__ == '__main__':
    run()
