# forms.py

from flask_wtf import FlaskForm
from wtforms import Form, StringField, IntegerField, SelectField, validators
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from datetime import datetime
from .config import programs
from .db_setup import db_session
from .models import Distributor


class DistributorForm(FlaskForm):
    states = [('AK', 'Alaska'), ('AL', 'Alabama'), ('AR', 'Arkansas'),
              ('AZ', 'Arizona'), ('CA', 'California'), ('CO', 'Colorado'),
              ('CT', 'Connecticut'), ('DC', 'District of Columbia'),
              ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'),
              ('HI', 'Hawaii'), ('IA', 'Iowa'), ('ID', 'Idaho'),
              ('IL', 'Illinois'), ('IN', 'Indiana'), ('KS', 'Kansas'),
              ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('MA', 'Massachusetts'),
              ('MD', 'Maryland'), ('ME', 'Maine'), ('MI', 'Michigan'),
              ('MN', 'Minnesota'), ('MO', 'Missouri'), ('MS', 'Mississippi'),
              ('MT', 'Montana'), ('NC', 'North Carolina'),
              ('ND', 'North Dakota'), ('NE', 'Nebraska'),
              ('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
              ('NM', 'New Mexico'), ('NV', 'Nevada'), ('NY', 'New York'),
              ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'),
              ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'),
              ('SC', 'South Carolina'), ('SD', 'South Dakota'),
              ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
              ('VA', 'Virginia'), ('VT', 'Vermont'), ('WA', 'Washington'),
              ('WI', 'Wisconsin'), ('WV', 'West Virginia'), ('WY', 'Wyoming')]

    company = StringField('Company')
    payee = StringField('Payee')
    address1 = StringField('Address 1')
    address2 = StringField('Address 2')
    city = StringField('City')
    state = SelectField('State', choices=states)
    zip = StringField('Zip')


def query_distributor():
    return db_session.query(Distributor).order_by(Distributor.company)


class BookingForm(FlaskForm):
    distributor = StringField('Distributor')
    distributor = QuerySelectField(query_factory=query_distributor,
                                   allow_blank=False, get_label='company')
    film = StringField('Film')
    program = SelectField('Program', choices=programs)
    guarantee = IntegerField('Guarantee', default=0)
    percentage = IntegerField('Percentage', default=0)
    start_date = DateField('Start Date', default=datetime.utcnow)
    end_date = DateField('End Date', default=datetime.utcnow)
    gross = IntegerField('Gross', default=0)


class PaymentForm(FlaskForm):
    booking = StringField('Booking')
    date = DateField('Date', default=datetime.utcnow)
    check_number = StringField('Check Number')
    amount = IntegerField('Amount')
