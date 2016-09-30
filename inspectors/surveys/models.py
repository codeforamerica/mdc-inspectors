# -*- coding: utf-8 -*-
from inspectors.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)


class Survey(Model):
    """Model for a standard feedback inspection survey"""
    __tablename__ = 'surveys'

    id = Column(db.Integer, primary_key=True, index=True)
    lang = Column(db.String(2), nullable=False, default='en')
    method = Column(db.String(3), nullable=False)
    date_submitted = Column(db.DateTime, nullable=False, index=True)
    rating = Column(db.Integer, nullable=False)
    get_done = Column(db.Boolean(), default=False)
    token = Column(db.String(100), nullable=False)
    role = Column(db.Integer, nullable=False)
    contact = Column(db.String(500), nullable=True)
    more_comments = Column(db.String(2000), nullable=True)
    follow_up = Column(db.Boolean(), default=False)
    permit_type = Column(db.String(50), nullable=False)
    know_to_pass = Column(db.Boolean(), default=False)
    typeform_id = Column(db.String(50), nullable=False)
