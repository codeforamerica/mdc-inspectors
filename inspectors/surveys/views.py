# -*- coding: utf-8 -*-
from flask import (
    Blueprint, request, json, Response
)
from .models import Survey

blueprint = Blueprint(
    'surveys',
    __name__,
    url_prefix='/surveys',
    static_folder="../static")


def parse_payload(resp):

    # FIXME - assumes the schema has been validated. I don't understand why I keep getting "View function did not return a response" errors.
    for row in resp['answers']:
        print (row, row['tags'][0])
        tag = row['tags'][0]
        if tag == 'other_comments':
            pass
        elif tag == 'role':
            pass
        elif tag == 'contact':
            pass
        elif tag == 'role':
            pass
        elif tag == 'rating':
            pass
        elif tag == 'present':
            pass
        else:
            pass

    survey = Survey(
        token=resp['token'],
        uid=resp['uid']
    )

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
