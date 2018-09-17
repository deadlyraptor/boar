# payment.py

from boar import app, db
from flask import flash, redirect, render_template, url_for
from flask_login import login_required
from ..models import Booking, Payment
from ..forms import PaymentForm
from ..tables import Payments


@app.route('/payment/new/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for('open_bookings'))
    return render_template('/forms/payment.html', form=form,
                           title='New Payment', heading='New Payment')


@app.route('/payments/<int:id>')
@login_required
def view_payments(id):
    """
    View payments associated with booking
    """
    payments = Payment.query.filter(Payment.booking_id == id).all()
    if not payments:
        flash('No payments found!')
        return redirect(url_for('open_bookings'))
    else:
        table = Payments(payments)
        return render_template('/table.html', table=table,
                               title='Payments', heading='Payments')
