# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from .views import results, distributor, booking, payment
