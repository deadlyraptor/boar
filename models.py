# models.py

from app import db


class Distributor(db.Model):
    __tablename__ = 'distributors'

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String)
    payee = db.Column(db.String)
    address1 = db.Column(db.String)
    address2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.String)

    bookings = db.relationship('Booking', backref='distributor', lazy=True)

    def __repr__(self):
        return '<Distributor {}>'.format(self.company)


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    film = db.Column(db.String)
    program = db.Column(db.String)
    guarantee = db.Column(db.Integer)
    percentage = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    gross = db.Column(db.Integer)
    settled = db.Column(db.Boolean, default=0)

    distributor_id = db.Column(db.Integer, db.ForeignKey('distributors.id'))

    payments = db.relationship('Payment', backref='booking', lazy=True)

    def __repr__(self):
        return '<Booking {}>'.format(self.film)


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    check_number = db.Column(db.String)
    amount = db.Column(db.Integer)

    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'))
