# views.py

from boar import app
from .db_setup import db_session
from flask import Flask, flash, render_template, request, redirect
from .models import Booking, Payment
from .forms import PaymentForm
from .tables import Distributors, Bookings, Payments, Results


@app.route('/')
def index():
    return render_template('index.html')

# payment routes


@app.route('/enter_payment/<int:id>', methods=['GET', 'POST'])
def enter_payment(id):
    """
    Enter a payment.
    """
    form = PaymentForm(request.form)

    if request.method == 'POST' and form.validate():
        # save the payment
        payment = Payment()
        save_payment(payment, form, id, new=True)
        flash('Payment entered successfully!')
        return redirect('/open_bookings')

    return render_template('enter_payment.html', form=form)


def save_payment(payment, form, id, new=False):
    """
    Save changes to the database
    """
    # booking = db_session.query(Booking).filter_by(
    #                                film=form.booking.data).first()
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
    View payments.
    """
    payments = []
    qry = db_session.query(Payment).filter(Payment.booking_id == id)
    payments = qry.all()

    if not payments:
        flash('No payments found!')
        return redirect('/open_bookings')
    else:
        table = Payments(payments)
        table.border = True
        return render_template('payments.html', table=table)


@app.route('/results/<int:id>')
def view_results(id):
    """
    View results.
    """
    results = []
    qry = db_session.query(Booking).filter(Booking.id == id)
    results = qry.all()

    film = results[0].film
    percentage = results[0].percentage
    guarantee = results[0].guarantee
    gross = results[0].gross

    # overage
    def overage(percentage, guarantee, gross):
        if (percentage / 100) * gross > guarantee:
            overage = (percentage / 100) * gross - guarantee
            return round(overage, 2)
        else:
            overage = 0
            return overage

    overage = overage(percentage, guarantee, gross)

    # total owed
    def total_owed(guarantee, overage):
        owed = guarantee + overage
        return owed

    owed = total_owed(guarantee, overage)

    # net
    def net(gross, owed):
        if gross == 0:
            net = 0
        else:
            net = gross - owed
        return net

    net = net(gross, owed)

    finances = [{'film': film, 'overage': overage, 'owed': owed, 'net': net}]

    if not results:
        flash('No results found!')
        return redirect('/open_bookings')
    else:
        table = Results(finances)
        table.border = True
        return render_template('results.html', table=table)
