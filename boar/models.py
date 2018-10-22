# models.py

from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from boar import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    profile_photo = db.Column(db.String(20), nullable=False,
                              default='default.jpg')

    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))

    def __repr__(self):
        return f'<User {self.username}>'

    def __str__(self):
        return '{}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_organization(self, name):
        """
        If the user enters an existing organization, this function will add the
        appropriate relationship.

        If the user does not enter an existing organization, this function will
        create it and add the appropriate relationship. Note that only the
        organization's name is added to the model. The user must update the
        other fields separetly.
        """
        organization = Organization.query.filter_by(name=name).first()
        if organization is None:
            organization = Organization(name=name)
            db.session.add(organization)
            db.session.commit()
            self.organization_id = organization.id
        else:
            self.organization_id = organization.id

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    address1 = db.Column(db.String, nullable=False)
    address2 = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    zip = db.Column(db.String, nullable=False)

    org_bookings = db.relationship('Booking',
                                   backref='organization', lazy=True)
    org_programs = db.relationship('Program',
                                   backref='organization', lazy=True)
    org_users = db.relationship('User', backref='organization', lazy=True)
    org_distributors = db.relationship('Distributor',
                                       backref='organization', lazy=True)

    def __repr__(self):
        return f'<Organization {self.name}>'

    def __str__(self):
        return f'{self.name}'


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    film = db.Column(db.String, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    guarantee = db.Column(db.Numeric, nullable=False)
    percentage = db.Column(db.Numeric, nullable=False)
    gross = db.Column(db.Numeric, nullable=False)
    settled = db.Column(db.Boolean, default=0)

    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'))
    distributor_id = db.Column(db.Integer, db.ForeignKey('distributors.id'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))

    payments = db.relationship('Payment', backref='booking', lazy=True)

    def __repr__(self):
        return f'<Booking {self.film} {self.start_date}>'

    def __str__(self):
        return f'{self.film}'


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    check_number = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'))

    def __repr__(self):
        return f'<Payment {self.booking_id}>'


class Program(db.Model):
    __tablename__ = 'programs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=1)

    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))

    program_bookings = db.relationship('Booking', backref='program', lazy=True)

    def __repr__(self):
        return f'<Program {self.name}>'

    def __str__(self):
        return f'{self.name}'

    def activate(self):
        self.active = 1

    def deactivate(self):
        self.active = 0


class Distributor(db.Model):
    __tablename__ = 'distributors'

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String, nullable=False)
    payee = db.Column(db.String, nullable=False)
    address1 = db.Column(db.String, nullable=False)
    address2 = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    zip = db.Column(db.String, nullable=False)

    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))

    bookings = db.relationship('Booking', backref='distributor', lazy=True)

    def __repr__(self):
        return f'<Distributor {self.company}>'

    def __str__(self):
        return f'{self.company}'
