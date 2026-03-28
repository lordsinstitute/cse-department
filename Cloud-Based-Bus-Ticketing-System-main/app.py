"""
Cloud-Based Comprehensive Bus Ticketing and Reservation System
Flask application with SQLite database.
"""
from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'bus_ticketing_system_2025'
DB_PATH = 'bus_ticketing.db'


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        role TEXT DEFAULT 'user'
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS buses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bus_number TEXT UNIQUE NOT NULL,
        bus_name TEXT NOT NULL,
        bus_type TEXT NOT NULL,
        source TEXT NOT NULL,
        destination TEXT NOT NULL,
        departure_time TEXT NOT NULL,
        arrival_time TEXT NOT NULL,
        total_seats INTEGER NOT NULL,
        available_seats INTEGER NOT NULL,
        fare REAL NOT NULL,
        status TEXT DEFAULT 'Active'
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        bus_id INTEGER NOT NULL,
        passenger_name TEXT NOT NULL,
        passenger_age INTEGER,
        passenger_gender TEXT,
        seats INTEGER NOT NULL,
        total_fare REAL NOT NULL,
        booking_date TEXT NOT NULL,
        travel_date TEXT NOT NULL,
        status TEXT DEFAULT 'Confirmed',
        payment_method TEXT DEFAULT 'Online',
        payment_status TEXT DEFAULT 'Paid',
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (bus_id) REFERENCES buses(id)
    )''')

    # Seed admin user
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, name, email, phone, role) VALUES (?, ?, ?, ?, ?, ?)",
                  ('admin', 'admin123', 'Administrator', 'admin@busticket.com', '9999999999', 'admin'))

    # Seed sample buses
    c.execute("SELECT COUNT(*) FROM buses")
    if c.fetchone()[0] == 0:
        buses = [
            ('AP-01-1234', 'Express Liner', 'AC Sleeper', 'Hyderabad', 'Bangalore', '22:00', '06:00', 40, 40, 850.00),
            ('AP-02-5678', 'Royal Travels', 'AC Seater', 'Hyderabad', 'Chennai', '20:00', '07:00', 50, 50, 950.00),
            ('AP-03-9012', 'City Connect', 'Non-AC Seater', 'Hyderabad', 'Vijayawada', '06:00', '12:00', 55, 55, 350.00),
            ('AP-04-3456', 'Night Rider', 'AC Sleeper', 'Hyderabad', 'Mumbai', '18:00', '08:00', 36, 36, 1450.00),
            ('AP-05-7890', 'Metro Express', 'AC Seater', 'Hyderabad', 'Pune', '21:00', '09:00', 45, 45, 1100.00),
            ('AP-06-2345', 'South Star', 'Non-AC Sleeper', 'Hyderabad', 'Tirupati', '22:30', '06:30', 40, 40, 550.00),
            ('AP-07-6789', 'Green Line', 'AC Seater', 'Hyderabad', 'Warangal', '07:00', '11:00', 50, 50, 250.00),
            ('AP-08-0123', 'Luxury Coach', 'Volvo AC', 'Hyderabad', 'Goa', '17:00', '07:00', 42, 42, 1800.00),
            ('TS-09-4567', 'Quick Ride', 'Non-AC Seater', 'Hyderabad', 'Karimnagar', '08:00', '12:00', 55, 55, 200.00),
            ('TS-10-8901', 'Premium Bus', 'Volvo AC', 'Hyderabad', 'Delhi', '16:00', '18:00', 40, 40, 2500.00),
        ]
        c.executemany("INSERT INTO buses (bus_number, bus_name, bus_type, source, destination, departure_time, arrival_time, total_seats, available_seats, fare) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", buses)

    conn.commit()
    conn.close()


# Initialize database on startup
init_db()


@app.route('/')
def home():
    stats = {}
    user_bookings = []
    conn = get_db()
    stats['total_buses'] = conn.execute("SELECT COUNT(*) FROM buses WHERE status='Active'").fetchone()[0]
    stats['total_routes'] = conn.execute("SELECT COUNT(DISTINCT destination) FROM buses WHERE status='Active'").fetchone()[0]
    stats['total_seats'] = conn.execute("SELECT COALESCE(SUM(available_seats),0) FROM buses WHERE status='Active'").fetchone()[0]
    if session.get('role') == 'admin':
        stats['total_bookings'] = conn.execute("SELECT COUNT(*) FROM bookings WHERE status='Confirmed'").fetchone()[0]
        stats['total_users'] = conn.execute("SELECT COUNT(*) FROM users WHERE role='user'").fetchone()[0]
        stats['total_revenue'] = conn.execute("SELECT COALESCE(SUM(total_fare),0) FROM bookings WHERE status='Confirmed'").fetchone()[0]
        stats['cancelled'] = conn.execute("SELECT COUNT(*) FROM bookings WHERE status='Cancelled'").fetchone()[0]
    elif session.get('user_id'):
        user_bookings = conn.execute('''
            SELECT b.*, bus.bus_name, bus.source, bus.destination, bus.departure_time
            FROM bookings b JOIN buses bus ON b.bus_id = bus.id
            WHERE b.user_id = ? AND b.status = 'Confirmed'
            ORDER BY b.id DESC LIMIT 3
        ''', (session['user_id'],)).fetchall()
        stats['my_bookings'] = conn.execute("SELECT COUNT(*) FROM bookings WHERE user_id=? AND status='Confirmed'",
                                            (session['user_id'],)).fetchone()[0]
    conn.close()
    return render_template('home.html', stats=stats, user_bookings=user_bookings)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        conn = get_db()
        try:
            conn.execute("INSERT INTO users (username, password, name, email, phone) VALUES (?, ?, ?, ?, ?)",
                         (username, password, name, email, phone))
            conn.commit()
            conn.close()
            flash('Registration successful! Please login.', 'success')
            return redirect('/login')
        except sqlite3.IntegrityError:
            conn.close()
            flash('Username already exists.', 'danger')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?",
                            (username, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['name'] = user['name']
            session['role'] = user['role']
            if user['role'] == 'admin':
                return redirect('/admin')
            return redirect('/search')
        flash('Invalid credentials.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db()
    sources = [r[0] for r in conn.execute("SELECT DISTINCT source FROM buses WHERE status='Active' ORDER BY source").fetchall()]
    destinations = [r[0] for r in conn.execute("SELECT DISTINCT destination FROM buses WHERE status='Active' ORDER BY destination").fetchall()]
    buses = []
    source = ""
    destination = ""
    if request.method == 'POST':
        source = request.form.get('source', '').strip()
        destination = request.form.get('destination', '').strip()
        buses = conn.execute(
            "SELECT * FROM buses WHERE LOWER(source) LIKE ? AND LOWER(destination) LIKE ? AND available_seats > 0 AND status='Active'",
            (f'%{source.lower()}%', f'%{destination.lower()}%')
        ).fetchall()
    conn.close()
    return render_template('search.html', buses=buses, source=source, destination=destination,
                           sources=sources, destinations=destinations)


@app.route('/book/<int:bus_id>', methods=['GET', 'POST'])
def book(bus_id):
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db()
    bus = conn.execute("SELECT * FROM buses WHERE id=?", (bus_id,)).fetchone()
    if not bus:
        conn.close()
        flash('Bus not found.', 'danger')
        return redirect('/search')

    if request.method == 'POST':
        passenger_name = request.form['passenger_name']
        passenger_age = int(request.form.get('passenger_age', 0))
        passenger_gender = request.form.get('passenger_gender', '')
        seats = int(request.form['seats'])
        travel_date = request.form['travel_date']
        payment_method = request.form.get('payment_method', 'Online')

        if seats > bus['available_seats']:
            flash(f'Only {bus["available_seats"]} seats available.', 'danger')
            conn.close()
            return render_template('book.html', bus=bus)

        total_fare = seats * bus['fare']
        booking_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn.execute(
            "INSERT INTO bookings (user_id, bus_id, passenger_name, passenger_age, passenger_gender, seats, total_fare, booking_date, travel_date, payment_method) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (session['user_id'], bus_id, passenger_name, passenger_age, passenger_gender,
             seats, total_fare, booking_date, travel_date, payment_method)
        )
        conn.execute("UPDATE buses SET available_seats = available_seats - ? WHERE id=?", (seats, bus_id))
        conn.commit()
        conn.close()
        flash(f'Booking confirmed! {seats} seat(s) booked. Total: Rs. {total_fare:.2f}', 'success')
        return redirect('/my-bookings')

    conn.close()
    return render_template('book.html', bus=bus)


@app.route('/my-bookings')
def my_bookings():
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db()
    bookings = conn.execute('''
        SELECT b.*, bus.bus_name, bus.bus_number, bus.source, bus.destination,
               bus.departure_time, bus.arrival_time, bus.bus_type
        FROM bookings b
        JOIN buses bus ON b.bus_id = bus.id
        WHERE b.user_id = ?
        ORDER BY b.id DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('my_bookings.html', bookings=bookings)


@app.route('/cancel/<int:booking_id>')
def cancel_booking(booking_id):
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db()
    booking = conn.execute("SELECT * FROM bookings WHERE id=? AND user_id=?",
                           (booking_id, session['user_id'])).fetchone()
    if booking and booking['status'] == 'Confirmed':
        conn.execute("UPDATE bookings SET status='Cancelled', payment_status='Refunded' WHERE id=?", (booking_id,))
        conn.execute("UPDATE buses SET available_seats = available_seats + ? WHERE id=?",
                     (booking['seats'], booking['bus_id']))
        conn.commit()
        flash('Booking cancelled. Refund initiated.', 'warning')
    conn.close()
    return redirect('/my-bookings')


# ---- Admin Routes ----

@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect('/login')
    conn = get_db()
    total_buses = conn.execute("SELECT COUNT(*) FROM buses").fetchone()[0]
    total_bookings = conn.execute("SELECT COUNT(*) FROM bookings WHERE status='Confirmed'").fetchone()[0]
    total_users = conn.execute("SELECT COUNT(*) FROM users WHERE role='user'").fetchone()[0]
    total_revenue = conn.execute("SELECT COALESCE(SUM(total_fare),0) FROM bookings WHERE status='Confirmed'").fetchone()[0]
    recent_bookings = conn.execute('''
        SELECT b.*, u.name as user_name, bus.bus_name, bus.source, bus.destination
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        JOIN buses bus ON b.bus_id = bus.id
        ORDER BY b.id DESC LIMIT 10
    ''').fetchall()
    conn.close()
    return render_template('admin_dashboard.html', total_buses=total_buses, total_bookings=total_bookings,
                           total_users=total_users, total_revenue=total_revenue, recent_bookings=recent_bookings)


@app.route('/admin/buses')
def admin_buses():
    if session.get('role') != 'admin':
        return redirect('/login')
    conn = get_db()
    buses = conn.execute("SELECT * FROM buses ORDER BY id").fetchall()
    conn.close()
    return render_template('admin_buses.html', buses=buses)


@app.route('/admin/add-bus', methods=['GET', 'POST'])
def add_bus():
    if session.get('role') != 'admin':
        return redirect('/login')
    if request.method == 'POST':
        conn = get_db()
        total_seats = int(request.form['total_seats'])
        try:
            conn.execute(
                "INSERT INTO buses (bus_number, bus_name, bus_type, source, destination, departure_time, arrival_time, total_seats, available_seats, fare) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (request.form['bus_number'], request.form['bus_name'], request.form['bus_type'],
                 request.form['source'], request.form['destination'], request.form['departure_time'],
                 request.form['arrival_time'], total_seats, total_seats, float(request.form['fare']))
            )
            conn.commit()
            flash('Bus added successfully!', 'success')
        except sqlite3.IntegrityError:
            flash('Bus number already exists.', 'danger')
        conn.close()
        return redirect('/admin/buses')
    return render_template('add_bus.html')


@app.route('/admin/bookings')
def admin_bookings():
    if session.get('role') != 'admin':
        return redirect('/login')
    conn = get_db()
    bookings = conn.execute('''
        SELECT b.*, u.name as user_name, u.phone as user_phone,
               bus.bus_name, bus.bus_number, bus.source, bus.destination
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        JOIN buses bus ON b.bus_id = bus.id
        ORDER BY b.id DESC
    ''').fetchall()
    conn.close()
    return render_template('admin_bookings.html', bookings=bookings)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
