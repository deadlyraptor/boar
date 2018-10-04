from flask import Blueprint

errors = Blueprint('errors', __name__)

from boar.errors import handlers
