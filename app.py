from flask import Flask, render_template, g, request
import sqlite3
from config import boar

app = Flask(__name__)

app.database = boar


# renders the home page
@app.route('/')
def home():
    # passes all open bookings in the database to a
    g.db = connect_db()
    cur = g.db.execute('select bookings.film, bookings.program, \
                        bookings.guarantee, bookings.percentage, \
                        bookings.start_date, bookings.end_date, \
                        distributors.distributor from bookings \
                        join distributors on bookings.distributor_id = \
                        distributors.distributor_id \
                        where bookings.settled = 0')

    bookings = [{'film': row[0], 'program': row[1],
                'guarantee': (row[2] / 100), 'percentage': (row[3] * 100),
                 'start_date': row[4], 'end_date': row[5],
                 'distributor': row[6]} for row in cur.fetchall()]
    g.db.close()
    return render_template('index.html', bookings=bookings)


def connect_db():
    return sqlite3.connect(app.database)


if __name__ == '__main__':
    app.run(debug=True)
