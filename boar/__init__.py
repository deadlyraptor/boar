# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from config import database, secret_key

app = Flask(__name__)
app.config.from_pyfile('config.py')
# app.config['SQLALCHEMY_DATABASE_URI'] = database
# app.secret_key = secret_key

db = SQLAlchemy(app)

from . import views

if __name__ == '__main__':
    app.run()
