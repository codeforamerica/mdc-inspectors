from flask import render_template

from inspectors.app import create_app

from inspectors.inspections.models import Feedback
from inspectors.surveys.util import send_email

from inspectors.inspections.queries import (
    active_users_with_past_inspections
)


def print_inspection(i):
    return "\n    ".join([
        "about",
        i.permit_description + "(" + i.permit_type + ") inspection at",
        i.job_site_address,
        "on " + i.date_inspected.strftime("%Y/%m/%d"),
        "at " + i.tf_url])


def email_inspection(u, i):
    subj = 'We want to hear about your recent inspection!'
    template = render_template('email/email-notification.txt', i=i)
    send_email(subj, [u.email], template)


def get_or_create_feedback(user, inspection):
    ''' Mark in the inspection_feedback table the user ID,
    inspection ID, send date and the typeform ID of the survey.
    We'll need this to get metadata about the survey as well.
    '''
    created = False
    data = dict(
        user_id=user.id,
        inspection_id=inspection.id,
        typeform_key=inspection.generate_tf_id())

    feedback = Feedback.query.filter_by(**data).first()
    if not feedback:
        feedback = Feedback.create(**data)
        created = True

    return created, feedback


def send_request_for_feedback(user, inspection):
    if user.email:
        print("email", user.email, print_inspection(inspection))
        email_inspection(user, inspection)

    if user.phone_number:
        print("text", user.phone_number, print_inspection(inspection))


def send_requests():
    # filter inspections to those that have recently happened.
    q = active_users_with_past_inspections()

    # create all necessary records
    for user, inspection in q.all():
        created, feedback_record = get_or_create_feedback(user, inspection)
        if created:
            send_request_for_feedback(user, inspection)


def run():
    ''' This is a script run daily that will do the following:
    Find activate users with past inspections
    Send requests for feedback, either by e-mail or sms
    '''
    app = create_app()
    with app.app_context():
        send_requests()

if __name__ == '__main__':
    run()
