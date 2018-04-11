# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import database, secret_key

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.secret_key = secret_key

db = SQLAlchemy(app)
