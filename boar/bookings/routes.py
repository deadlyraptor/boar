# routes for bookings

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from ..models import Booking
from .forms import BookingForm
from ..tables import Bookings, Results
from boar import db
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
        flash('Booking successfully created.', 'success')
        return redirect(url_for('booking_bp.open_bookings'))
    return render_template('/booking/booking.html', form=form,
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
        return redirect(url_for('booking_bp.open_bookings'))
    return render_template('/booking/booking.html', form=form,
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
    return redirect(url_for('booking_bp.open_bookings'))


@booking_bp.route('/open-bookings')
@login_required
def open_bookings():
    """
    Renders a template with a table containing all unsettled bookings
    """
    bookings = Booking.query.order_by(
        Booking.start_date).filter_by(
            settled=0, organization_id=current_user.organization_id).all()
    if not bookings:
        flash('No open bookings found.', 'warning')
        return redirect(url_for('main.index'))
    else:
        table = Bookings(bookings)
        return render_template('table.html', table=table,
                               title='Open Bookings', heading='Open Bookings')


@booking_bp.route('/booking/results/<int:id>', methods=['GET'])
@login_required
def booking_results(id):
    """
    Renders a template containing a booking's box office performance.
    """
    finances = results(id)
    if finances is None:
        flash('No booking found!')
        return redirect(url_for('booking_bp.open_bookings'))
    else:
        table = Results(finances)
        return render_template('table.html', table=table,
                               title='Results', heading='Results')
