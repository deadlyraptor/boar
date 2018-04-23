# views.py

from boar import app
from .db_setup import db_session
from flask import Flask, flash, render_template, request, redirect
from .models import Distributor, Booking, Payment
from .forms import DistributorForm, BookingForm, PaymentForm
from .tables import Distributors, Bookings, Payments, Results


@app.route('/')
def index():
    return render_template('index.html')

# distributor routes


@app.route('/new_distributor', methods=['GET', 'POST'])
def new_distributor():
    """
    Add a new distributor
    """
    form = DistributorForm(request.form)

    if request.method == 'POST' and form.validate():
        # save the distributor
        distributor = Distributor()
        save_distributor(distributor, form, new=True)
        flash('Distributor added successfully!')
        return redirect('/')

    return render_template('new_distributor.html', form=form)


def save_distributor(distributor, form, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object

    distributor.company = form.company.data
    distributor.payee = form.payee.data
    distributor.address1 = form.address1.data
    distributor.address2 = form.address2.data
    distributor.city = form.city.data
    distributor.state = form.state.data
    distributor.zip = form.zip.data

    if new:
        # Add the new distributor to the database
        db_session.add(distributor)

    # commit the data to the database
    db_session.commit()


@app.route('/distributors')
def list_distributors():
    distributors = []
    qry = db_session.query(Distributor).order_by(Distributor.company)
    distributors = qry.all()

    if not distributors:
        flash('No distributors found!')
        return redirect('/')
    else:
        # display distributors
        table = Distributors(distributors)
        table.border = True
        return render_template('distributors.html', table=table)


@app.route('/distributor/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db_session.query(Distributor).filter(Distributor.id == id)
    distributor = qry.first()

    if distributor:
        form = DistributorForm(formdata=request.form, obj=distributor)
        if request.method == 'POST' and form.validate():
            # save edits
            save_distributor(distributor, form)
            flash('Distributor updated successfully!')
            return redirect('/')
        return render_template('edit_distributor.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


@app.route('/delete_distributor/<int:id>', methods=['GET', 'POST'])
def delete_distributor(id):
    """
    Delete the item in the database that matches the specified ID in the URL
    """
    qry = db_session.query(Distributor).filter(Distributor.id == id)
    distributor = qry.first()

    if distributor:
        form = DistributorForm(formdata=request.form, obj=distributor)
        if request.method == 'POST' and form.validate():
            # delete the item from the database
            db_session.delete(distributor)
            db_session.commit()

            flash('Distributor deleted successfully!')
            return redirect('/')
        return render_template('delete_distributor.html', form=form)
    else:
        return 'Error deleting #{id}'.format(id=id)

# booking routes


@app.route('/new_booking', methods=['GET', 'POST'])
def new_booking():
    """
    Add a new booking
    """
    form = BookingForm(request.form)

    if request.method == 'POST' and form.validate():
        # save the booking
        booking = Booking()
        save_booking(booking, form, new=True)
        flash('Booking added successfully!')
        return redirect('/')

    return render_template('new_booking.html', form=form)


def save_booking(booking, form, new=False):
    """
    Save changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object

    distributor = db_session.query(Distributor).filter_by(
                                         company=form.distributor.data).first()

    booking.distributor = distributor
    booking.film = form.film.data
    booking.program = form.program.data
    booking.guarantee = form.guarantee.data
    booking.percentage = form.percentage.data
    booking.start_date = form.start_date.data
    booking.end_date = form.end_date.data
    booking.gross = form.gross.data

    if new:
        # Add the new booking to the database
        db_session.add(booking)

    # commit the data to the database
    db_session.commit()

    return render_template('new_booking.html', form=form)


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
        # display open bookings
        table = Bookings(bookings)
        table.border = True
        return render_template('open_bookings.html', table=table)


@app.route('/booking/<int:id>', methods=['GET', 'POST'])
def update(id):
    qry = db_session.query(Booking).filter(Booking.id == id)
    booking = qry.first()

    if booking:
        form = BookingForm(formdata=request.form, obj=booking)
        if request.method == 'POST' and form.validate():
            # save data
            save_booking(booking, form)
            flash('Booking updated successfully!')
            return redirect('/')
        return render_template('update_booking.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


@app.route('/delete_booking/<int:id>', methods=['GET', 'POST'])
def delete_booking(id):
    """
    Delete the item in the database that matches the specified ID in the URL
    """
    qry = db_session.query(Booking).filter(Booking.id == id)
    booking = qry.first()

    if booking:
        form = BookingForm(formdata=request.form, obj=booking)
        if request.method == 'POST' and form.validate():
            # delete the item from the database
            db_session.delete(booking)
            db_session.commit()

            flash('Booking deleted successfully!')
            return redirect('/')
        return render_template('delete_booking.html', form=form)
    else:
        return 'Error deleting #{id}'.format(id=id)

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
