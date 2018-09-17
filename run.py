# run.py

from boar import app, db
from boar.models import Booking, Distributor, Organization, Payment, User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Booking': Booking, 'Distributor': Distributor,
            'Organization': Organization, 'Payment': Payment, 'User': User}


if __name__ == '__main__':
    app.run()
