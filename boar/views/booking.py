# booking.py

from boar import app
from flask import Flask, flash, render_template, request, redirect
from ..db_setup import db_session
from ..models import Booking, Distributor
from ..forms import BookingForm
from ..tables import Bookings


@app.route('/booking/new', methods=['GET', 'POST'])
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

    return render_template('/booking/new.html', form=form)


def save_booking(booking, form, new=False):
    """
    Save changes to the database
    """
    # Get data from form and assign it to the correct attributes of the
    # SQLAlchemy table object

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
        db_session.add(booking)

    db_session.commit()


@app.route('/open_bookings')
def open_bookings():
    bookings = []
    qry = db_session.query(Booking).order_by(
                            Booking.start_date).filter(Booking.settled == 0)
    bookings = qry.all()

    if not bookings:
        flash('No open bookings found!')
        return redirect('/')
    else:
        table = Bookings(bookings)
        table.border = True
        return render_template('/booking/open_bookings.html', table=table)


@app.route('/booking/edit/<int:id>', methods=['GET', 'POST'])
def edit_booking(id):
    qry = db_session.query(Booking).filter(Booking.id == id)
    booking = qry.first()

    if booking:
        form = BookingForm(formdata=request.form, obj=booking)
        if request.method == 'POST' and form.validate():
            save_booking(booking, form)
            flash('Booking updated successfully!')
            return redirect('/')
        return render_template('/booking/edit.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


@app.route('/booking/delete/<int:id>', methods=['GET', 'POST'])
def delete_booking(id):
    qry = db_session.query(Booking).filter(Booking.id == id)
    booking = qry.first()

    if booking:
        form = BookingForm(formdata=request.form, obj=booking)
        if request.method == 'POST' and form.validate():
            db_session.delete(booking)
            db_session.commit()

            flash('Booking deleted successfully!')
            return redirect('/')
        return render_template('/booking/delete.html', form=form)
    else:
        return 'Error deleting #{id}'.format(id=id)
