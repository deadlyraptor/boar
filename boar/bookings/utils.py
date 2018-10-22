from flask_login import current_user
from boar.models import Booking, Distributor, Program


def query_distributors():
    """Returns query on distributors

    This query factory is used to populate the distributors in the
    booking form.
    """
    distributors = Distributor.query.order_by(Distributor.company).filter_by(
        organization_id=current_user.organization_id)
    return distributors


def query_programs():
    """Returns query on programs

    This query factory is used to populate the programs in the booking form.
    """
    programs = Program.query.order_by(Program.name).filter_by(
        organization_id=current_user.organization_id, active=1)
    return programs


def results(id):
    """Returns a dictionary with values pertaining to the performance
    of a booking
    """
    booking = Booking.query.filter_by(id=id).first_or_404()

    film = booking.film
    percentage = (booking.percentage / 100)
    guarantee = booking.guarantee
    gross = booking.gross

    # overage
    def overage(percentage, guarantee, gross):
        if percentage * gross > guarantee:
            overage = percentage * gross - guarantee
            return round(overage, 2)
        else:
            overage = 0
            return overage

    overage = overage(percentage, guarantee, gross)

    # total owed
    def total_owed(guarantee, overage):
        owed = guarantee + overage
        return round(owed, 2)

    owed = total_owed(guarantee, overage)

    # net
    def net(gross, owed):
        if gross == 0:
            net = 0
        else:
            net = gross - owed
        return round(net, 2)

    net = net(gross, owed)

    results = [{'film': film, 'gross': gross, 'guarantee': guarantee,
                'overage': overage, 'owed': owed, 'net': net}]
    return results
