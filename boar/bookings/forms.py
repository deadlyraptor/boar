# forms for bookings

from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired
from boar.bookings.utils import query_distributor, query_program


class BookingForm(FlaskForm):
    distributor = QuerySelectField(query_factory=query_distributor,
                                   allow_blank=False, get_label='company')
    film = StringField('Film', validators=[InputRequired()])
    program = QuerySelectField(query_factory=query_program,
                               allow_blank=False, get_label='name')
    guarantee = IntegerField('Guarantee', default=0)
    percentage = IntegerField('Percentage', default=35)
    start_date = DateField('Start Date', default=datetime.utcnow)
    end_date = DateField('End Date', default=datetime.utcnow)
    gross = IntegerField('Gross', default=0)
    submit = SubmitField('Submit')
