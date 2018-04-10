# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database

db = SQLAlchemy(app)
