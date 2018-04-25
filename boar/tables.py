# tables.py

from flask_table import Table, Col, LinkCol, DateCol


class Distributors(Table):
    id = Col('Id', show=False)
    company = Col('Company')
    payee = Col('Payee')
    address1 = Col('Address Line 1')
    address2 = Col('Address Line 2')
    city = Col('City')
    state = Col('State')
    zip = Col('Zip')
    edit = LinkCol('Edit', 'edit_distributor', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_distributor', url_kwargs=dict(id='id'))


class Bookings(Table):
    id = Col('Id', show=False)
    film = Col('Film')
    start_date = DateCol('Start Date')
    end_date = DateCol('End Date')
    program = Col('Program')
    guarantee = Col('Guarantee')
    percentage = Col('Percentage')
    gross = Col('Gross')
    view_results = LinkCol('View Results', 'view_results',
                           url_kwargs=dict(id='id'))
    distributor = Col('Distributor')
    update = LinkCol('Edit', 'edit_booking', url_kwargs=dict(id='id'))
    enter_payment = LinkCol('Enter Payment', 'new_payment',
                            url_kwargs=dict(id='id'))
    view_payments = LinkCol('View Payments', 'view_payments',
                            url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_booking', url_kwargs=dict(id='id'))


class Payments(Table):
    id = Col('Id', show=False)
    booking = Col('Booking')
    date = DateCol('Date')
    check_number = Col('Check Number')
    amount = Col('Amount')


class Results(Table):
    film = Col('Film')
    overage = Col('Overage')
    owed = Col('Owed')
    net = Col('Net')
