import datetime

from inspectors.app import db
from inspectors.registration.models import User
from inspectors.inspections.models import (
    Inspection, Feedback,
    Supervisor, Inspector)


def active_users_with_past_inspections():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return db.session.query(User, Inspection).join(
        Inspection, User.permit_number == Inspection.permit_number).\
        filter(Inspection.date_inspected < today).\
        filter(Inspection.display_description != 'INSPECTION CANCELLATION').\
        filter(User.active == True)
