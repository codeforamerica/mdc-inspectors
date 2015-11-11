# -*- coding: utf-8 -*-
import datetime as dt
from pprint import pprint
from flask import json, render_template

from inspectors.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)

from inspectors.surveys.typeform import TypeformIOClass

REPR_DATE_FMT = "%Y/%m/%d"


class Supervisor(Model):
    """A person who supervises building inspectors"""
    __tablename__ = 'supervisor'

    id = Column(db.Integer, primary_key=True, index=True)
    email = Column(db.String(80), index=True, nullable=False)
    full_name = Column(db.String(150), nullable=False)
    active = Column(db.Boolean, default=True)
    inspectors = db.relationship('Inspector', backref='supervisor')
    last_report = Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Supervisor({0})>'.format(self.full_name)

    def send_report(self):
        raise NotImplementedError

    def unsubscribe(self):
        raise NotImplementedError


class Inspector(Model):
    """A person who does inspections."""
    __tablename__ = 'inspector'

    id = Column(db.Integer, primary_key=True, index=True)
    inspector_key = Column(db.String(25), nullable=False, index=True)
    first_name = Column(db.String(80), nullable=False)
    last_name = Column(db.String(80), nullable=False)
    photo_url = Column(db.String(80), nullable=True)
    supervisor_id = Column(db.Integer, db.ForeignKey('supervisor.id'), nullable=False)
    inspections = db.relationship('Inspection', backref='inspector')

    @property
    def full_name(self):
        ''' The format of the inspector name which
        shows in all surveys. For now, keep it to
        the first name (John) rather than the full
        name (John Jones) or John J.
        '''
        return "{0}".format(self.first_name)

    def __repr__(self):
        return '<Inspector(id:{0}, name:{1})>'.format(self.inspector_key, " ".join([self.first_name, self.last_name]))


class Inspection(Model):
    """An inspection of a some construction by an inspector"""
    __tablename__ = 'inspection'
    id = Column(db.Integer, primary_key=True, index=True)
    permit_number = Column(db.String(25), nullable=False)
    date_inspected = Column(db.DateTime, nullable=False)
    permit_type = Column(db.String(10), nullable=False)
    permit_description = Column(db.String(50), nullable=True)
    display_description = Column(db.String(50), nullable=False)
    job_site_address = Column(db.String(200), nullable=False)
    inspector_id = Column(db.Integer, db.ForeignKey('inspector.id'), nullable=False)
    users_feedback = db.relationship('InspectionFeedback', backref='inspection')

    @property
    def permit_type_full(self):
        return {
            'BLDG': 'Building',
            'ROOF': 'Roofing',
            'ELEC': 'Electrical',
            'PLUM': 'Plumbing',
            'MECH': 'Mechanical',
            'ZONE': 'Zoning'
        }.get(self.permit_type, self.permit_type)

    def generate_typeform_url(self):
        ''' Generate the Typeform URL of the personalized
        form - necessary for the inspection_feedback table
        '''
        tf = TypeformIOClass()
        inspector = Inspector.query.get(self.inspector_id).full_name
        str_quiz = render_template(
            'typeform/template.json',
            inspector=inspector,
            permit_number=self.permit_number,
            itype=self.permit_type_full,
            description=self.permit_description,
            result=self.display_description,
            addr=self.job_site_address)

        json_quiz = json.loads(str_quiz)
        result = tf.make_call(json_quiz)
        return result['_links'][1]['href']

    def __repr__(self):
        return '<Inspection({0}:{1})>'.format(self.permit_number, self.date_inspected.strftime(REPR_DATE_FMT))


class Feedback(Model):
    """A many to many relation table between inspections and users that records
    whether or not we've already asked a user for feedback on one particular
    inspection.
    """
    __tablename__ = 'feedback'
    id = Column(db.Integer, primary_key=True, index=True)
    inspection_id = Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)
    user_id = Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_sent = Column(db.DateTime, nullable=True, default=True)
    typeform_key = Column(db.String(50), nullable=True)

    def __repr__(self):
        d = self.date_sent
        return '<InspectionFeedback({})>'.format(
            "sent on: " + d.strftime(REPR_DATE_FMT) if d else "unsent")
