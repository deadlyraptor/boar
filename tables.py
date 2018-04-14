from flask_table import Table, Col, LinkCol


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
