# models.py

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from boar import db, login


class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address1 = db.Column(db.String)
    address2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.String)

    org_bookings = db.relationship('Booking',
                                   backref='organization', lazy=True)
    org_programs = db.relationship('Program',
                                   backref='organization', lazy=True)
    org_users = db.relationship('User', backref='organization', lazy=True)
    org_distributors = db.relationship('Distributor',
                                       backref='organization', lazy=True)

    def __repr__(self):
        return '<Organization {}>'.format(self.name)

    def __str__(self):
        return '{}'.format(self.name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    password_hash = db.Column(db.String)

    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __str__(self):
        return '{}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Program(db.Model):
    __tablename__ = 'programs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=1)

    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))

    program_bookings = db.relationship('Booking', backref='program', lazy=True)

    def __repr__(self):
        return '<Program {}>'.format(self.name)

    def __str__(self):
        return '{}'.format(self.name)

    def activate(self):
        self.active = 1

    def deactivate(self):
        self.active = 0


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

    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))

    bookings = db.relationship('Booking', backref='distributor', lazy=True)

    def __repr__(self):
        return '<Distributor {}>'.format(self.company)

    def __str__(self):
        return '{}'.format(self.company)


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    film = db.Column(db.String)
    guarantee = db.Column(db.Integer)
    percentage = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    gross = db.Column(db.Integer)
    settled = db.Column(db.Boolean, default=0)

    distributor_id = db.Column(db.Integer, db.ForeignKey('distributors.id'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'))

    payments = db.relationship('Payment', backref='booking', lazy=True)

    def __repr__(self):
        return '<Booking {}>'.format(self.film)

    def __str__(self):
        return '{}'.format(self.film)


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    check_number = db.Column(db.String)
    amount = db.Column(db.Integer)

    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'))

    def __repr__(self):
        return '<Payment {}>'.format(self.booking_id)
