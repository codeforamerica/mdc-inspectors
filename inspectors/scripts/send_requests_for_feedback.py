from pprint import pprint

from inspectors.app import create_app
from inspectors.app import db

from inspectors.inspections.models import Inspection, InspectionFeedback
from inspectors.registration.models import User

from inspectors.inspections.queries import (
        active_users_with_past_inspections
        )


def print_inspection(i):
    return "\n    ".join(["about",
                i.permit_description + i.permit_type + " inspection at",
                i.job_site_address,
                "on " + i.date_inspected.strftime("%Y/%m/%d")
            ])


def get_or_create_feedback_record(user, inspection):
    created = False
    data = dict(
            user_id = user.id,
            inspection_id = inspection.id
            )
    feedback_record = db.session.query(
                InspectionFeedback
            ).filter_by( **data ).first()
    if not feedback_record:
        feedback_record = InspectionFeedback( **data )
        db.session.add(feedback_record)
        created = True
    return created, feedback_record

def send_request_for_feedback(user, inspection):
    if user.email:
        print( "email", user.email, print_inspection(inspection) )
    if user.phone_number:
        print( "text", user.phone_number, print_inspection(inspection) )


def send_requests():
    # filter inspections to those that have recently happened.
    q = active_users_with_past_inspections()
    # create all necessary records
    for user, inspection in q.all():
        send_request_for_feedback(user, inspection)

def run():
    app = create_app()
    with app.app_context():
        send_requests()

if __name__ == '__main__':
    run()
