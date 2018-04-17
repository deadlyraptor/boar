from flask_table import Table, Col, LinkCol, DateCol


class DistributorList(Table):
    id = Col('Id', show=False)
    company = Col('Company')
    payee = Col('Payee')
    address1 = Col('Address Line 1')
    address2 = Col('Address Line 2')
    city = Col('City')
    state = Col('State')
    zip = Col('Zip')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))


class Bookings(Table):
    id = Col('Id', show=False)
    film = Col('Film')
    start_date = Col('Start Date')
    end_date = Col('End Date')
    program = Col('Program')
    guarantee = Col('Guarantee')
    percentage = Col('Percentage')
    gross = Col('Gross')
    distributor = Col('Distributor')
    update = LinkCol('Update', 'update', url_kwargs=dict(id='id'))
    enter_payment = LinkCol('Enter Payment', 'enter_payment',
                            url_kwargs=dict(id='id'))
    view_payments = LinkCol('View Payments', 'view_payments',
                            url_kwargs=dict(id='id'))


class Payments(Table):
    id = Col('Id', show=False)
    booking = Col('Booking')
    date = DateCol('Date')
    check_number = Col('Check Number')
    amount = Col('Amount')
