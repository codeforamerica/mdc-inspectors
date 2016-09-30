# -*- coding: utf-8 -*-
from flask import (
    Blueprint, request, json, Response
)
from .models import Survey
from .constants import ROLES
from inspectors.app import db
from inspectors.inspections.models import Feedback, Inspection

blueprint = Blueprint(
    'surveys',
    __name__,
    url_prefix='/surveys',
    static_folder="../static")


def parse_payload(resp):
    ''' Argument: resp
    Returns: resp
    '''
    typeform_id = resp['uid']
    data = dict(
        token=resp['token'],
        typeform_id=typeform_id
    )

    # FIXME - assumes the schema has been validated. I don't understand why I keep getting "View function did not return a response" errors.
    for row in resp['answers']:
        # print (row, row['tags'][0])
        tag = row['tags'][0]
        if tag == 'other_comments':
            data['more_comments'] = row['value']

        elif tag == 'contact':
            data['contact'] = row['value']

        elif tag == 'role':
            data['role'] = ROLES[row['value']['label']]

        elif tag == 'rating':
            data['rating'] = row['value']['amount']

        elif tag == 'present':
            pass

        else:
            pass

    feedback, inspection = db.session.query(Feedback, Inspection).\
        join(Inspection).filter(Feedback.typeform_key == typeform_id).first()
    if inspection:
        data['permit_type'] = inspection.permit_type
        data['get_done'] = inspection.is_passed()

    print(inspection.id, inspection.permit_type, feedback.inspection_id, feedback.typeform_key)

    print (data)

    # survey = Survey(**data)

    return resp


@blueprint.route("/webhook", methods=['GET', 'POST'])
def webhook():
    ''' How to test this on localhost, since I had to do some digging:
    1. Run the server locally in one tab (pythong manage.py server)
    2. In another tab try curl -H "Content-Type: application/json" -X POST -d typeform-request.json http://127.0.0.1:5000/surveys/webhook
    TIP: Resty may help: https://github.com/micha/resty. Once you do that you can do the following:
    Tab 1: resty http://127.0.0.1:5000 -H "Content-Type: application/json"
    Tab 2: POST /surveys/webhook < typeform-request.json
    '''
    if request.method == 'POST':
        try:
            payload = json.loads(request.data)
            parse_payload(payload)
            # FIXME: Get schema to work - I don't know why it doesn't

            return 'OK', 202
        except:
            pass
    else:
        # Probably raise an error of some sort or redirect
        resp = Response(status=200)
        return resp
