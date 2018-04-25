# payment.py

from boar import app
from flask import Flask, flash, render_template, request, redirect
from .db_setup import db_session
from .models import Booking, Payment
from .forms import PaymentForm
from .tables import Bookings, Payments


@app.route('/payment/new/<int:id>', methods=['GET', 'POST'])
def new_payment(id):
    """
    Add a payment
    """
    form = PaymentForm(request.form)

    if request.method == 'POST' and form.validate():
        payments = Payment()
        save_payment(payment, form, id, new=True)
        flash('Payment entered successfully!')
        return redirect('/open_bookings')

    return render_template('/payment/new.html', form=form)


def save_payment(payment, form, id, new=False):
    booking = db_session.query(Booking).filter(Booking.id == id).first()

    payment.booking = booking
    payment.date = form.date.data
    payment.check_number = form.check_number.data
    payment.amount = form.amount.data

    if new:
        db_session.add(payment)

    db_session.commit()


@app.route('/payments/<int:id>')
def view_payments(id):
    """
    View payments associated with booking
    """
    payments = []
    qry = db_session.query(Payment).filter(Payment.id == id)
    payments = qry.all()

    if not payments:
        flash('No payments found!')
        return redirect('/open_bookings')
    else:
        table = Payments(payments)
        table.border = True
        return render_template('/payment/payments.html', table=table)
