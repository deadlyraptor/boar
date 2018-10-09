# handlers.py

from flask import render_template
from boar import db
from boar.errors import errors


@errors.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def forbidden_403(error):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
