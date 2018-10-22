# routes for bookings

import decimal
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from boar import db
from boar.models import Booking
from boar.bookings.forms import BookingForm
from boar.bookings.utils import results

booking_bp = Blueprint('booking_bp', __name__)


@booking_bp.route('/booking/new', methods=['GET', 'POST'])
@login_required
def new_booking():
    """
    Adds a new booking
    """
    form = BookingForm()
    if form.validate_on_submit():
        booking = Booking(film=form.film.data,
                          start_date=form.start_date.data,
                          end_date=form.end_date.data,
                          guarantee=decimal.Decimal(form.guarantee.data),
                          percentage=decimal.Decimal(form.percentage.data),
                          gross=decimal.Decimal(form.gross.data),
                          program=form.program.data,
                          distributor=form.distributor.data,
                          organization_id=current_user.organization_id)
        db.session.add(booking)
        db.session.commit()
        flash('Booking successfully created.', 'success')
        return redirect(url_for('booking_bp.list_bookings'))
    return render_template('/bookings/new_booking.html', form=form,
                           title='New Booking', legend='New Booking')


@booking_bp.route('/booking/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_booking(id):
    """
    Updates a booking
    """
    # check if current user belongs to booking's organization and if not,
    # render the 404 page because the query returns None
    booking = Booking.query.filter_by(
        id=id, organization_id=current_user.organization_id).first_or_404()
    form = BookingForm(obj=booking)
    if form.validate_on_submit():
        form.populate_obj(booking)
        db.session.commit()
        flash('Booking successfully updated.', 'success')
        return redirect(url_for('booking_bp.list_bookings'))
    return render_template('/bookings/new_booking.html', form=form,
                           title='Update Booking', legend='Update Booking')


@booking_bp.route('/booking/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_booking(id):
    """
    Deletes a booking
    """
    booking = Booking.query.filter_by(id=id).first()
    db.session.delete(booking)
    db.session.commit()
    flash('Booking successfully deleted.', 'success')
    return redirect(url_for('booking_bp.list_bookings'))


@booking_bp.route('/bookings')
@login_required
def list_bookings():
    """
    Renders a template with a table containing all unsettled bookings
    """
    bookings = Booking.query.order_by(
        Booking.start_date).filter_by(
                        organization_id=current_user.organization_id).all()
    if not bookings:
        flash('No open bookings found.', 'warning')
        return redirect(url_for('main.index'))
    else:
        return render_template('/bookings/booking_table.html',
                               bookings=bookings, title='Bookings',
                               heading='Bookings')


@booking_bp.route('/booking/results/<int:id>', methods=['GET'])
@login_required
def booking_results(id):
    """
    Renders a template containing a booking's box office performance.
    """
    finances = results(id)
    if not finances:
        flash('No booking found!')
        return redirect(url_for('booking_bp.list_bookings'))
    else:
        return render_template('/bookings/results.html', finances=finances,
                               title='Results', heading='Results')
