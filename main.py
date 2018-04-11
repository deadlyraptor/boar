# main.py

from flask import Flask, render_template, request, redirect
from app import app
from forms import DistributorForm
from models import Distributor, Booking, Payment


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new_distributor', methods=['GET', 'POST'])
def new_distributor():
    """
    Add a new distributor
    """
    form = DistributorForm(request.form)

    if request.method == 'POST' and form.validate():
        # save the distributor
        distributor = Distributor()
        save_changes(distributor, form, new=True)
        flash('Distributor added successfully!')
        return redirect('/')

    return render_template('new_distributor.html', form=form)


def save_changes(distributor, form, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object

    distributor.company = form.company.data
    distributor.payee = form.payee.data
    distributor.address1 = form.address1.data
    distributor.address2 = form.address2.data
    distributor.city = form.city.data
    distributor.state = form.state.data
    distributor.zip = form.zip.data


@app.route('/new_booking')
def new_booking():
    """
    Add a new booking
    """
    return render_template('new_booking.html')
