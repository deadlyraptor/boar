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


# renders the page to enter a new booking
@app.route('/booking')
def booking():
    return render_template('booking.html')


@app.route('/booking', methods=['POST'])
def insert_booking():
    g.db = connect_db()
    film = request.form['film']
    program = request.form['program']
    guarantee = request.form['guarantee']
    percentage = request.form['percentage']
    start = request.form['start_date']
    end = request.form['end_date']
    distributor = request.form['distributor']

    def distrib_to_id():
        cur = g.db.execute('select distributor_id from distributors where \
                            distributor = \'{0}\''.format(distributor))
        dID = [{'id': row[0]} for row in cur.fetchall()]
        return dID[0]['id']

    cur = g.db.execute('insert into bookings (film, program, guarantee, \
                       percentage, start_date, end_date, distributor_id) \
                       values (?, ?, ?, ?, ?, ?, ?)',
                       (film, program, (int(guarantee) * 100),
                        (int(percentage) / 100), start, end, distrib_to_id()))
    g.db.commit()
    g.db.close()
    return home()


def connect_db():
    return sqlite3.connect(app.database)


if __name__ == '__main__':
    app.run(debug=True)
