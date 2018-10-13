# forms for bookings

from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired
from boar.bookings.utils import query_distributors, query_programs


class BookingForm(FlaskForm):
    film = StringField('Film', validators=[InputRequired()])
    start_date = DateField('Start Date', default=datetime.utcnow)
    end_date = DateField('End Date', default=datetime.utcnow)
    guarantee = DecimalField('Minimum Guarantee', default=0)
    percentage = DecimalField('Percentage', default=35)
    gross = DecimalField('Gross', default=0)
    program = QuerySelectField(query_factory=query_programs,
                               allow_blank=False, get_label='name')
    distributor = QuerySelectField(query_factory=query_distributors,
                                   allow_blank=True, get_label='company')
    submit = SubmitField('Submit')
