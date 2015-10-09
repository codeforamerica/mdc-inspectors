# -*- coding: utf-8 -*-
import datetime as dt

from inspectors.database import (
    Column,
    db,
    Model,
    relationship,
)


class User(Model):
    """A greatly simplified user model that does not log in
        This is someone who is subscribing to requests for feedback on
        inspections about a certain permit number.
    """
    __tablename__ = 'user'

    id = Column(db.Integer, primary_key=True, index=True)
    permit_number = Column(db.String(25), nullable=False, index=True)
    date_registered = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    email = Column(db.String(80), nullable=True)
    phone_number = Column(db.String(15), nullable=True)
    active = Column(db.Boolean(), default=True)

    def __repr__(self):
        return '<User({0})>'.format(self.permit_number)

