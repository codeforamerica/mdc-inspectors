# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired, Optional, Email, Length

from .util import is_valid_permit
# from .models import User


class RegisterForm(Form):
    permit_id = TextField('Miami-Dade County Permit or Process Number', validators=[DataRequired(), Length(min=10, max=25)])
    email = TextField('Email address (optional)', validators=[Optional(), Email(), Length(min=6, max=40)])
    sms = TextField('Phone number to get SMS updates (optional)', validators=[Optional(), Length(min=10, max=40)])

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        if not self.email.data and not self.sms.data:
            self.email.errors.append("We need either an e-mail or an SMS to notify you.")
            return False
        if not is_valid_permit(self.permit_id.data):
            self.permit_id.errors.append(self.permit_id.data + " doesn't seem to be a valid Miami-Dade County Permit or Process Number.")
            return False

        '''
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        '''
        return True
