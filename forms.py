# forms.py

from wtforms import Form, StringField, IntegerField, SelectField, validators
from wtforms.fields.html5 import DateField


class DistributorForm(Form):
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


class BookingForm(Form):
    distributor = StringField('Distributor')
    film = StringField('Film')
    program = StringField('Program')
    guarantee = IntegerField('Guarantee')
    percentage = IntegerField('Percentage')
    start_date = DateField('Start Date')
    end_date = DateField('End Date')
    gross = IntegerField('Gross')
