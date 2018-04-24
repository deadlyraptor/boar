# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from . import views
from . import distributor
from . import booking

if __name__ == '__main__':
    app.run()
