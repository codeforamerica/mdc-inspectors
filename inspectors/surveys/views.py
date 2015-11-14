# -*- coding: utf-8 -*-
from flask import (
    Blueprint, request, json
)

blueprint = Blueprint('surveys', __name__, url_prefix='/surveys', static_folder="../static")


def do_something(json):
    return json


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
            print ("HTTP/1.1 200 OK")
            print (payload)
            return 'OK'
        except:
            pass
    else:
        # Probably raise an error of some sort or redirect
        print ('GETS HERE FWIW')
