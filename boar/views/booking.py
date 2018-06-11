# booking.py

from boar import app, db
from flask import flash, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models import Booking
from ..forms import BookingForm
from ..tables import Bookings


@app.route('/booking/new', methods=['GET', 'POST'])
@login_required
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
                          gross=form.gross.data,
                          organization_id=current_user.organization_id)
        db.session.add(booking)
        db.session.commit()
        flash('Booking added successfully!')
        return redirect(url_for('open_bookings'))
    return render_template('/forms/booking.html', form=form,
                           title='New Booking', heading='New Booking')


@app.route('/open_bookings')
@login_required
def open_bookings():
    bookings = Booking.query.order_by(
        Booking.start_date).filter(
        Booking.settled == 0,
        Booking.organization_id == current_user.organization_id).all()
    if not bookings:
        flash('No open bookings found!')
        return redirect(url_for('index'))
    else:
        table = Bookings(bookings)
        return render_template('/table.html', table=table,
                               title='Open Bookings', heading='Open Bookings')


@app.route('/booking/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_booking(id):
    # check if current user belongs to booking's organization and if not,
    # render the 404 page because the query returns None
    booking = Booking.query.filter(
              Booking.id == id,
              Booking.organization_id ==
              current_user.organization_id).first_or_404()
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
        return redirect(url_for('open_bookings'))
    return render_template('/forms/booking.html', form=form,
                           title='Edit Booking', heading='Edit Booking')


@app.route('/booking/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_booking(id):
    booking = Booking.query.filter(Booking.id == id).first()
    db.session.delete(booking)
    db.session.commit()
    flash('Booking successfully deleted!')
    return redirect(url_for('open_bookings'))
