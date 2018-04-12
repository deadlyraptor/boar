from flask_table import Table, Col, LinkCol


class DistributorList(Table):
    id = Col('Id', show=False)
    company = Col('Company')
    payee = Col('Payee')
    address1 = Col('Address1')
    address2 = Col('Address2')
    city = Col('City')
    state = Col('State')
    zip = Col('Zip')
