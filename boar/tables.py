# tables.py

from flask_table import Table, Col, LinkCol, DateCol, ButtonCol


class Distributors(Table):
    classes = ['table', 'table-bordered', 'table-striped']
    company = Col('Company')
    payee = Col('Payee')
    address1 = Col('Address Line 1')
    address2 = Col('Address Line 2')
    city = Col('City')
    state = Col('State')
    zip = Col('Zip')
    edit = LinkCol('Edit', 'edit_distributor', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_distributor', url_kwargs=dict(id='id'),
                     anchor_attrs={'type': 'button',
                                   'class': 'btn btn-danger'})


class Bookings(Table):
    classes = ['table', 'table-bordered', 'table-striped']
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
    delete = LinkCol('Delete', 'delete_booking', url_kwargs=dict(id='id'),
                     anchor_attrs={'type': 'button',
                                   'class': 'btn btn-danger'})


class Payments(Table):
    classes = ['table', 'table-bordered', 'table-striped']
    booking = Col('Booking')
    date = DateCol('Date')
    check_number = Col('Check Number')
    amount = Col('Amount')


class Results(Table):
    classes = ['table', 'table-bordered', 'table-striped']
    film = Col('Film')
    gross = Col('Gross')
    guarantee = Col('Guarantee')
    overage = Col('Overage')
    owed = Col('Owed')
    net = Col('Net')


class Programs(Table):
    classes = ['table', 'table-bordered', 'table-striped', 'table-sm']
    name = Col('Name')
    active = ButtonCol('Deactivate', 'deactivate', url_kwargs=dict(id='id'))
