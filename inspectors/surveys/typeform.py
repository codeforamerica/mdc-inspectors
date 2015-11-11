# -*- coding: utf-8 -*-
import requests
from flask import current_app


class ApiTokenNotDefinedException (Exception):
    pass


class TypeformIOClass (object):

    def __init__(self, api_token=None, user_agent='pyformio'):
        self.api_token = None
        self.user_agent = user_agent
        if api_token:
            self.api_token = api_token
        else:
            try:
                self.api_token = current_app.config.get('TYPEFORMIO_KEY')
            except KeyError:
                raise ApiTokenNotDefinedException

        self.headers = {
            'User-Agent': self.user_agent,
            'X-API-TOKEN': self.api_token
        }

    def make_call(self, json):
        URL = 'https://api.typeform.io/v0.4/forms'
        r = requests.post(
            URL,
            headers=self.headers,
            json=json)

        # FIXME: uh, what if this isn't Reponse OK? Add error checking.
        print ("Response: %s" % r.status_code)
        print (r.raw.read())
        return r.json()
