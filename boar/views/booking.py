# booking.py

from boar import app
from flask import Flask, flash, render_template, request, redirect, url_for
from ..db_setup import db_session
from ..models import Booking, Distributor
from ..forms import BookingForm
from ..tables import Bookings


@app.route('/booking/new', methods=['GET', 'POST'])
def new_booking():
    """
    Add a new booking
    """
    form = BookingForm()

    if form.validate_on_submit():
        booking = Booking(distributor=form.distributor.data,
                          film=form.film.data,
                          program=form.program.data,
                          guarantee=form.guarantee.data,
                          percentage=form.percentage.data,
                          start_date=form.start_date.data,
                          end_date=form.end_date.data,
                          gross=form.gross.data)
        db_session.add(booking)
        db_session.commit()
        flash('Booking added successfully!')
        return redirect(url_for('index'))
    return render_template('/booking/new.html', form=form)


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
        if form.validate_on_submit():
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
        if form.validate_on_submit():
            db_session.delete(booking)
            db_session.commit()

            flash('Booking deleted successfully!')
            return redirect('/')
        return render_template('/booking/delete.html', form=form)
    else:
        return 'Error deleting #{id}'.format(id=id)
