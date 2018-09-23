# forms.py

from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import InputRequired
from wtforms.fields.html5 import DateField


class PaymentForm(FlaskForm):
    film = StringField('Booking', validators=[InputRequired()])
    date = DateField('Date', default=datetime.utcnow)
    check_number = StringField('Check Number', validators=[InputRequired()])
    amount = IntegerField('Amount', validators=[InputRequired()])
    submit = SubmitField('Submit')
