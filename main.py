# main.py

from app import app
from db_setup import db_session
from flask import Flask, flash, render_template, request, redirect
from forms import DistributorForm, BookingForm
from models import Distributor, Booking, Payment
from tables import DistributorList


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list_of_distributors')
def list_distributors():
    distributors = []
    qry = db_session.query(Distributor)
    distributors = qry.all()

    if not distributors:
        flash('No distributors found!')
        return redirect('/')
    else:
        # display distributors
        table = DistributorList(distributors)
        table.border = True
        return render_template('list_of_distributors.html', table=table)


@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db_session.query(Distributor).filter(Distributor.id == id)
    distributor = qry.first()

    if distributor:
        form = DistributorForm(formdata=request.form, obj=distributor)
        if request.method == 'POST' and form.validate():
            # save edits
            save_distributor(distributor, form)
            flash('Distributor updated successfully!')
            return redirect('/')
        return render_template('edit_distributor.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


@app.route('/new_distributor', methods=['GET', 'POST'])
def new_distributor():
    """
    Add a new distributor
    """
    form = DistributorForm(request.form)

    if request.method == 'POST' and form.validate():
        # save the distributor
        distributor = Distributor()
        save_distributor(distributor, form, new=True)
        flash('Distributor added successfully!')
        return redirect('/')

    return render_template('new_distributor.html', form=form)


def save_distributor(distributor, form, new=False):
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

    if new:
        # Add the new distributor to the database
        db_session.add(distributor)

    # commit the data to the database
    db_session.commit()


@app.route('/new_booking', methods=['GET', 'POST'])
def new_booking():
    """
    Add a new booking
    """
    form = BookingForm(request.form)

    if request.method == 'POST' and form.validate():
        # save the booking
        booking = Booking()
        save_booking(booking, form, new=True)
        flash('Booking added successfully!')
        return redirect('/')

    return render_template('new_booking.html', form=form)


def save_booking(booking, form, new=False):
    """
    Save changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object

    distributor = db_session.query(Distributor).filter_by(
                                         company=form.distributor.data).first()

    booking.distributor = distributor
    booking.film = form.film.data
    booking.program = form.program.data
    booking.guarantee = form.guarantee.data
    booking.percentage = form.percentage.data
    booking.start_date = form.start_date.data
    booking.end_date = form.end_date.data
    booking.gross = form.gross.data

    if new:
        # Add the new booking to the database
        db_session.add(booking)

    # commit the data to the database
    db_session.commit()

    return render_template('new_booking.html', form=form)
