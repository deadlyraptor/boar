# __init__.py

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = app.config['GMAIL_USERNAME']
app.config['MAIL_PASSWORD'] = app.config['GMAIL_PASSWORD']
mail = Mail(app)

from boar.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from .booking import views
from .distributor import views
from .payment import views
from .program import views
from .results import views
from .user import views


@app.route('/')
def index():
    return render_template('index.html', title='Home')
