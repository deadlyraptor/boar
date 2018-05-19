# run.py

from boar import app, db
from boar.models import Organization, User, Distributor, Booking, Payment


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Organization': Organization, 'User': User,
            'Distributor': Distributor, 'Booking': Booking, 'Payment': Payment}


if __name__ == '__main__':
    app.run()
