# routes for payments

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required
from ..models import Booking, Payment
from .forms import PaymentForm
from ..tables import Payments
from boar import db

payments_bp = Blueprint('payments_bp', __name__)


@payments_bp.route('/payment/new/<int:id>', methods=['GET', 'POST'])
@login_required
def new_payment(id):
    """
    Add a payment
    """
    booking = Booking.query.filter(Booking.id == id).first()
    form = PaymentForm(obj=booking)
    if form.validate_on_submit():
        payment = Payment(booking=booking,
                          date=form.date.data,
                          check_number=form.check_number.data,
                          amount=form.amount.data)
        db.session.add(payment)
        db.session.commit()
        flash('Payment entered successfully!')
        return redirect(url_for('booking_bp.list_bookings'))
    return render_template('/payment/payment.html', form=form,
                           title='New Payment', legend='New Payment')


@payments_bp.route('/payments/<int:id>')
@login_required
def view_payments(id):
    """
    View payments associated with booking
    """
    payments = Payment.query.filter(Payment.booking_id == id).all()
    if not payments:
        flash('No payments found!', 'warning')
        return redirect(url_for('booking_bp.list_bookings'))
    else:
        table = Payments(payments)
        return render_template('/table.html', table=table,
                               title='Payments', heading='Payments')
