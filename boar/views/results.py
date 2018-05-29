# results.py

from boar import app
from flask import flash, render_template, redirect, url_for
from flask_login import login_required
from ..models import Booking
from ..tables import Results


@app.route('/results/<int:id>')
@login_required
def view_results(id):
    """
    View results.
    """
    booking = Booking.query.filter(Booking.id == id).first()

    film = booking.film
    percentage = booking.percentage
    guarantee = booking.guarantee
    gross = booking.gross

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

    if not booking:
        flash('No booking found!')
        return redirect(url_for('open_bookings'))
    else:
        table = Results(finances)
        table.border = True
        return render_template('results.html', table=table)
