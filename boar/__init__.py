# __init__.py

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message_category = 'info'

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
