# views.py

from boar import app
from ..db_setup import db_session
from flask import Flask, flash, render_template, request, redirect
from ..models import Booking
from ..tables import Distributors, Results


@app.route('/')
def index():
    return render_template('index.html')


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
        return redirect(url_for('open_bookings'))
    else:
        table = Results(finances)
        table.border = True
        return render_template('results.html', table=table)
