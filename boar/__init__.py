# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'users.login'
login.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    from boar.bookings.routes import booking_bp
    from boar.distributor.routes import distributors_bp
    from boar.errors import errors
    from boar.payment.routes import payments_bp
    from boar.program.routes import programs_bp
    from boar.user.routes import users
    from boar.main.routes import main
    from boar.utils.filters import filters
    app.register_blueprint(booking_bp)
    app.register_blueprint(distributors_bp)
    app.register_blueprint(errors)
    app.register_blueprint(payments_bp)
    app.register_blueprint(programs_bp)
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(filters)

    return app
