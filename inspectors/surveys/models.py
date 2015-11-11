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
    rating = Column(db.Integer, nullable=False)
    follow_up = Column(db.Boolean(), default=False)
    token = Column(db.String(100), nullable=True)
    contact = Column(db.String(500), nullable=True)
    more_comments = Column(db.String(2000), nullable=True)
