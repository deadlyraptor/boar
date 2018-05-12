# booking.py

from boar import app, db
from flask import Flask, flash, render_template, request, redirect, url_for
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
        db.session.add(booking)
        db.session.commit()
        flash('Booking added successfully!')
        return redirect(url_for('index'))
    return render_template('/booking/new.html', form=form)


@app.route('/open_bookings')
def open_bookings():
    bookings = Booking.query.order_by(
        Booking.start_date).filter(Booking.settled == 0)
    if not bookings:
        flash('No open bookings found!')
        return redirect(url_for('index'))
    else:
        table = Bookings(bookings)
        table.border = True
        return render_template('/booking/open_bookings.html', table=table)


@app.route('/booking/edit/<int:id>', methods=['GET', 'POST'])
def edit_booking(id):
    booking = Booking.query.filter(Booking.id == id).first()
    form = BookingForm(obj=booking)
    if form.validate_on_submit():
        booking.distributor = form.distributor.data
        booking.film = form.film.data
        booking.program = form.program.data
        booking.guarantee = form.guarantee.data
        booking.percentage = form.percentage.data
        booking.start_date = form.start_date.data
        booking.end_date = form.end_date.data
        booking.gross = form.gross.data
        db.session.commit()
        flash('Booking updated successfully!')
        return redirect(url_for('index'))
    return render_template('/booking/edit.html', form=form)


@app.route('/booking/delete/<int:id>', methods=['GET', 'POST'])
def delete_booking(id):
    booking = Booking.query.filter(Booking.id == id).first()
    if booking:
        form = BookingForm(obj=booking)
        if form.validate_on_submit():
            db.session.delete(booking)
            db.session.commit()
            flash('Booking deleted successfully!')
            return redirect(url_for('index'))
        return render_template('/booking/delete.html', form=form)
