# main.py

from flask import Flask, render_template
from app import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new_distributor')
def new_distributor():
    """
    Add a new distributor
    """
    return render_template('new_distributor.html')


@app.route('/new_booking')
def new_booking():
    """
    Add a new booking
    """
    return render_template('new_booking.html')
