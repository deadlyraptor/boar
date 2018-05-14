# payment.py

from boar import app, db
from flask import Flask, flash, render_template, redirect, url_for
from ..models import Booking, Payment
from ..forms import PaymentForm
from ..tables import Bookings, Payments


@app.route('/payment/new/<int:id>', methods=['GET', 'POST'])
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
    return render_template('/payment/new.html', form=form)


@app.route('/payments/<int:id>')
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
        table.border = True
        return render_template('/payment/payments.html', table=table)
