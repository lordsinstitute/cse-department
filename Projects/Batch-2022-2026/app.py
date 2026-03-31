"""Smart Property Hub — Real Estate Management System (Flask + SQLite)"""

import os
import sqlite3
from datetime import datetime
from functools import wraps

from flask import (Flask, flash, redirect, render_template, request,
                   session, url_for, g)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'smart-property-hub-secret-2025'
DB_PATH = os.path.join(os.path.dirname(__file__), 'smart_property.db')

# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop('db', None)
    if db:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.execute('PRAGMA foreign_keys = ON')
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            role TEXT NOT NULL CHECK(role IN ('admin','seller','buyer')),
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seller_id INTEGER NOT NULL REFERENCES users(id),
            title TEXT NOT NULL,
            property_type TEXT NOT NULL,
            location TEXT NOT NULL,
            landmark TEXT,
            price REAL NOT NULL,
            bedrooms INTEGER,
            bathrooms INTEGER,
            area_sqft INTEGER,
            amenities TEXT,
            description TEXT,
            status TEXT DEFAULT 'available' CHECK(status IN ('available','booked','sold')),
            image_file TEXT DEFAULT 'pic01.jpg',
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id INTEGER NOT NULL REFERENCES properties(id),
            buyer_id INTEGER NOT NULL REFERENCES users(id),
            message TEXT,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending','confirmed','cancelled')),
            booking_date TEXT DEFAULT (datetime('now'))
        );
    ''')
    db.commit()
    # Seed data on first run
    cur = db.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        seed_data(db)
    db.close()


def seed_data(db):
    """Insert admin, sample sellers, and sample properties."""
    # Admin
    db.execute("INSERT INTO users (username, password, name, email, phone, role) VALUES (?,?,?,?,?,?)",
               ('admin', generate_password_hash('admin123'), 'Administrator',
                'admin@smartproperty.com', '9000000000', 'admin'))
    # Sellers
    db.execute("INSERT INTO users (username, password, name, email, phone, role) VALUES (?,?,?,?,?,?)",
               ('seller1', generate_password_hash('seller123'), 'Rajesh Kumar',
                'rajesh@email.com', '9100000001', 'seller'))
    db.execute("INSERT INTO users (username, password, name, email, phone, role) VALUES (?,?,?,?,?,?)",
               ('seller2', generate_password_hash('seller123'), 'Priya Sharma',
                'priya@email.com', '9100000002', 'seller'))

    # 8 sample properties
    props = [
        ('Sunrise Apartment', 'Apartment', 'Hyderabad', 'Near HITEC City', 45.0,
         2, 2, 1100, 'Lift, Parking, Security', 'Modern 2BHK apartment in prime location.', 'pic01.jpg', 2),
        ('Green Valley Villa', 'Villa', 'Gachibowli', 'Near ISB Road', 120.0,
         4, 3, 3200, 'Garden, Pool, Gym, Parking', 'Luxurious 4BHK villa with private pool.', 'pic02.jpg', 2),
        ('Royal Heights Flat', 'Apartment', 'Bangalore', 'Whitefield Main Road', 65.0,
         3, 2, 1500, 'Lift, Gym, Club House', 'Spacious 3BHK with city skyline views.', 'pic03.jpg', 3),
        ('Lake View Villa', 'Villa', 'Jubilee Hills', 'Near KBR Park', 250.0,
         5, 4, 5000, 'Lake View, Garden, Home Theatre', 'Premium villa overlooking Hussain Sagar.', 'pic01.jpg', 3),
        ('Skyline Plot', 'Plot', 'Shamshabad', 'Near Airport', 18.0,
         0, 0, 2400, 'Gated Community, Roads', 'Investment plot near Rajiv Gandhi Airport.', 'pic02.jpg', 2),
        ('Meadow Lands', 'Plot', 'Kompally', 'Near ORR Junction', 12.0,
         0, 0, 1800, 'Boundary Wall, Electricity', 'Affordable plot in developing area.', 'pic03.jpg', 2),
        ('TechPark Office', 'Commercial', 'Madhapur', 'Cyber Towers Area', 85.0,
         0, 2, 2000, 'AC, Power Backup, Parking', 'Ready-to-move office space in IT hub.', 'pic01.jpg', 3),
        ('Business Plaza', 'Commercial', 'Banjara Hills', 'Road No. 12', 150.0,
         0, 3, 3500, 'Conference Room, Cafeteria, CCTV', 'Premium commercial space on main road.', 'pic02.jpg', 3),
    ]
    for t, pt, loc, lm, pr, bed, bath, area, amen, desc, img, sid in props:
        db.execute(
            "INSERT INTO properties (seller_id, title, property_type, location, landmark, "
            "price, bedrooms, bathrooms, area_sqft, amenities, description, image_file) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (sid, t, pt, loc, lm, pr, bed, bath, area, amen, desc, img))
    db.commit()

# ---------------------------------------------------------------------------
# Auth decorators
# ---------------------------------------------------------------------------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if session.get('role') not in roles:
                flash('Access denied.', 'danger')
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated
    return decorator

# ---------------------------------------------------------------------------
# Context processor
# ---------------------------------------------------------------------------

@app.context_processor
def inject_user():
    return dict(
        current_user=session.get('name'),
        current_role=session.get('role'),
        current_user_id=session.get('user_id'),
    )

# ---------------------------------------------------------------------------
# Auth routes
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['name'] = user['name']
            session['role'] = user['role']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        name = request.form['name'].strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        role = request.form['role']
        if role not in ('seller', 'buyer'):
            flash('Invalid role selected.', 'danger')
            return redirect(url_for('register'))
        db = get_db()
        if db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        db.execute(
            "INSERT INTO users (username, password, name, email, phone, role) VALUES (?,?,?,?,?,?)",
            (username, generate_password_hash(password), name, email, phone, role))
        db.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('login'))

# ---------------------------------------------------------------------------
# Home (role-based dashboard)
# ---------------------------------------------------------------------------

@app.route('/home')
@login_required
def home():
    db = get_db()
    role = session['role']
    ctx = {}
    if role == 'admin':
        ctx['total_users'] = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        ctx['total_sellers'] = db.execute("SELECT COUNT(*) FROM users WHERE role='seller'").fetchone()[0]
        ctx['total_buyers'] = db.execute("SELECT COUNT(*) FROM users WHERE role='buyer'").fetchone()[0]
        ctx['total_properties'] = db.execute("SELECT COUNT(*) FROM properties").fetchone()[0]
        ctx['total_bookings'] = db.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]
        ctx['recent_properties'] = db.execute(
            "SELECT p.*, u.name AS seller_name FROM properties p "
            "JOIN users u ON p.seller_id = u.id ORDER BY p.created_at DESC LIMIT 4").fetchall()
    elif role == 'seller':
        uid = session['user_id']
        ctx['my_property_count'] = db.execute(
            "SELECT COUNT(*) FROM properties WHERE seller_id = ?", (uid,)).fetchone()[0]
        ctx['my_booking_count'] = db.execute(
            "SELECT COUNT(*) FROM bookings b JOIN properties p ON b.property_id = p.id "
            "WHERE p.seller_id = ?", (uid,)).fetchone()[0]
        ctx['my_properties'] = db.execute(
            "SELECT * FROM properties WHERE seller_id = ? ORDER BY created_at DESC LIMIT 4",
            (uid,)).fetchall()
    else:  # buyer
        ctx['total_available'] = db.execute(
            "SELECT COUNT(*) FROM properties WHERE status='available'").fetchone()[0]
        ctx['my_bookings_count'] = db.execute(
            "SELECT COUNT(*) FROM bookings WHERE buyer_id = ?", (session['user_id'],)).fetchone()[0]
        ctx['featured'] = db.execute(
            "SELECT p.*, u.name AS seller_name FROM properties p "
            "JOIN users u ON p.seller_id = u.id WHERE p.status='available' "
            "ORDER BY p.price DESC LIMIT 4").fetchall()
    return render_template('home.html', **ctx)

# ---------------------------------------------------------------------------
# Properties (browse + search)
# ---------------------------------------------------------------------------

@app.route('/properties')
@login_required
def properties():
    db = get_db()
    query = "SELECT p.*, u.name AS seller_name FROM properties p JOIN users u ON p.seller_id = u.id WHERE 1=1"
    params = []
    # Filters
    search = request.args.get('search', '').strip()
    prop_type = request.args.get('type', '')
    location = request.args.get('location', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    bedrooms = request.args.get('bedrooms', '')

    if search:
        query += " AND (p.title LIKE ? OR p.location LIKE ? OR p.landmark LIKE ?)"
        params.extend([f'%{search}%'] * 3)
    if prop_type:
        query += " AND p.property_type = ?"
        params.append(prop_type)
    if location:
        query += " AND p.location LIKE ?"
        params.append(f'%{location}%')
    if min_price:
        query += " AND p.price >= ?"
        params.append(float(min_price))
    if max_price:
        query += " AND p.price <= ?"
        params.append(float(max_price))
    if bedrooms:
        query += " AND p.bedrooms >= ?"
        params.append(int(bedrooms))

    query += " ORDER BY p.created_at DESC"
    props = db.execute(query, params).fetchall()

    # Get unique locations for filter dropdown
    locations = db.execute("SELECT DISTINCT location FROM properties ORDER BY location").fetchall()
    return render_template('properties.html', properties=props, locations=locations,
                           filters={'search': search, 'type': prop_type, 'location': location,
                                    'min_price': min_price, 'max_price': max_price, 'bedrooms': bedrooms})


@app.route('/property/<int:pid>')
@login_required
def property_detail(pid):
    db = get_db()
    prop = db.execute(
        "SELECT p.*, u.name AS seller_name, u.email AS seller_email, u.phone AS seller_phone "
        "FROM properties p JOIN users u ON p.seller_id = u.id WHERE p.id = ?", (pid,)).fetchone()
    if not prop:
        flash('Property not found.', 'danger')
        return redirect(url_for('properties'))
    # Check if buyer already booked
    already_booked = False
    if session['role'] == 'buyer':
        already_booked = db.execute(
            "SELECT id FROM bookings WHERE property_id = ? AND buyer_id = ?",
            (pid, session['user_id'])).fetchone() is not None
    # Get bookings for this property (seller/admin)
    bookings = []
    if session['role'] in ('seller', 'admin'):
        bookings = db.execute(
            "SELECT b.*, u.name AS buyer_name, u.email AS buyer_email, u.phone AS buyer_phone "
            "FROM bookings b JOIN users u ON b.buyer_id = u.id WHERE b.property_id = ? "
            "ORDER BY b.booking_date DESC", (pid,)).fetchall()
    return render_template('property_detail.html', property=prop,
                           already_booked=already_booked, bookings=bookings)

# ---------------------------------------------------------------------------
# Seller: property CRUD
# ---------------------------------------------------------------------------

@app.route('/add-property', methods=['GET', 'POST'])
@login_required
@role_required('seller')
def add_property():
    if request.method == 'POST':
        images = ['pic01.jpg', 'pic02.jpg', 'pic03.jpg']
        db = get_db()
        count = db.execute("SELECT COUNT(*) FROM properties").fetchone()[0]
        db.execute(
            "INSERT INTO properties (seller_id, title, property_type, location, landmark, "
            "price, bedrooms, bathrooms, area_sqft, amenities, description, image_file) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (session['user_id'],
             request.form['title'].strip(),
             request.form['property_type'],
             request.form['location'].strip(),
             request.form.get('landmark', '').strip(),
             float(request.form['price']),
             int(request.form.get('bedrooms', 0)),
             int(request.form.get('bathrooms', 0)),
             int(request.form.get('area_sqft', 0)),
             request.form.get('amenities', '').strip(),
             request.form.get('description', '').strip(),
             images[count % 3]))
        db.commit()
        flash('Property added successfully!', 'success')
        return redirect(url_for('my_properties'))
    return render_template('add_property.html')


@app.route('/edit-property/<int:pid>', methods=['GET', 'POST'])
@login_required
@role_required('seller')
def edit_property(pid):
    db = get_db()
    prop = db.execute("SELECT * FROM properties WHERE id = ? AND seller_id = ?",
                      (pid, session['user_id'])).fetchone()
    if not prop:
        flash('Property not found or access denied.', 'danger')
        return redirect(url_for('my_properties'))
    if request.method == 'POST':
        db.execute(
            "UPDATE properties SET title=?, property_type=?, location=?, landmark=?, "
            "price=?, bedrooms=?, bathrooms=?, area_sqft=?, amenities=?, description=?, status=? "
            "WHERE id=? AND seller_id=?",
            (request.form['title'].strip(),
             request.form['property_type'],
             request.form['location'].strip(),
             request.form.get('landmark', '').strip(),
             float(request.form['price']),
             int(request.form.get('bedrooms', 0)),
             int(request.form.get('bathrooms', 0)),
             int(request.form.get('area_sqft', 0)),
             request.form.get('amenities', '').strip(),
             request.form.get('description', '').strip(),
             request.form['status'],
             pid, session['user_id']))
        db.commit()
        flash('Property updated successfully!', 'success')
        return redirect(url_for('my_properties'))
    return render_template('edit_property.html', property=prop)


@app.route('/delete-property/<int:pid>', methods=['POST'])
@login_required
@role_required('seller', 'admin')
def delete_property(pid):
    db = get_db()
    if session['role'] == 'seller':
        db.execute("DELETE FROM bookings WHERE property_id IN (SELECT id FROM properties WHERE id=? AND seller_id=?)",
                   (pid, session['user_id']))
        db.execute("DELETE FROM properties WHERE id = ? AND seller_id = ?", (pid, session['user_id']))
    else:
        db.execute("DELETE FROM bookings WHERE property_id = ?", (pid,))
        db.execute("DELETE FROM properties WHERE id = ?", (pid,))
    db.commit()
    flash('Property deleted.', 'info')
    if session['role'] == 'admin':
        return redirect(url_for('properties'))
    return redirect(url_for('my_properties'))


@app.route('/my-properties')
@login_required
@role_required('seller')
def my_properties():
    db = get_db()
    props = db.execute(
        "SELECT p.*, (SELECT COUNT(*) FROM bookings WHERE property_id = p.id) AS booking_count "
        "FROM properties p WHERE p.seller_id = ? ORDER BY p.created_at DESC",
        (session['user_id'],)).fetchall()
    return render_template('my_properties.html', properties=props)

# ---------------------------------------------------------------------------
# Buyer: booking
# ---------------------------------------------------------------------------

@app.route('/book/<int:pid>', methods=['POST'])
@login_required
@role_required('buyer')
def book_property(pid):
    db = get_db()
    prop = db.execute("SELECT * FROM properties WHERE id = ? AND status = 'available'", (pid,)).fetchone()
    if not prop:
        flash('Property not available for booking.', 'danger')
        return redirect(url_for('properties'))
    existing = db.execute("SELECT id FROM bookings WHERE property_id = ? AND buyer_id = ?",
                          (pid, session['user_id'])).fetchone()
    if existing:
        flash('You have already booked this property.', 'warning')
        return redirect(url_for('property_detail', pid=pid))
    message = request.form.get('message', '').strip()
    db.execute("INSERT INTO bookings (property_id, buyer_id, message) VALUES (?,?,?)",
               (pid, session['user_id'], message))
    db.execute("UPDATE properties SET status = 'booked' WHERE id = ?", (pid,))
    db.commit()
    flash('Booking request submitted successfully!', 'success')
    return redirect(url_for('my_bookings'))


@app.route('/my-bookings')
@login_required
@role_required('buyer')
def my_bookings():
    db = get_db()
    bookings = db.execute(
        "SELECT b.*, p.title, p.location, p.price, p.property_type, p.image_file, "
        "u.name AS seller_name FROM bookings b "
        "JOIN properties p ON b.property_id = p.id "
        "JOIN users u ON p.seller_id = u.id "
        "WHERE b.buyer_id = ? ORDER BY b.booking_date DESC",
        (session['user_id'],)).fetchall()
    return render_template('my_bookings.html', bookings=bookings)

# ---------------------------------------------------------------------------
# Admin
# ---------------------------------------------------------------------------

@app.route('/admin/users')
@login_required
@role_required('admin')
def admin_users():
    db = get_db()
    users = db.execute("SELECT * FROM users ORDER BY role, created_at DESC").fetchall()
    return render_template('admin_users.html', users=users)


@app.route('/admin/delete-user/<int:uid>', methods=['POST'])
@login_required
@role_required('admin')
def admin_delete_user(uid):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone()
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin_users'))
    if user['role'] == 'admin':
        flash('Cannot delete admin user.', 'danger')
        return redirect(url_for('admin_users'))
    # Delete related data
    if user['role'] == 'seller':
        db.execute("DELETE FROM bookings WHERE property_id IN (SELECT id FROM properties WHERE seller_id=?)", (uid,))
        db.execute("DELETE FROM properties WHERE seller_id = ?", (uid,))
    elif user['role'] == 'buyer':
        db.execute("DELETE FROM bookings WHERE buyer_id = ?", (uid,))
    db.execute("DELETE FROM users WHERE id = ?", (uid,))
    db.commit()
    flash(f'User "{user["username"]}" deleted.', 'info')
    return redirect(url_for('admin_users'))


@app.route('/admin/bookings')
@login_required
@role_required('admin')
def admin_bookings():
    db = get_db()
    bookings = db.execute(
        "SELECT b.*, p.title AS property_title, p.location, p.price, "
        "buyer.name AS buyer_name, seller.name AS seller_name "
        "FROM bookings b "
        "JOIN properties p ON b.property_id = p.id "
        "JOIN users buyer ON b.buyer_id = buyer.id "
        "JOIN users seller ON p.seller_id = seller.id "
        "ORDER BY b.booking_date DESC").fetchall()
    return render_template('admin_bookings.html', bookings=bookings)

# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------

@app.route('/about')
@login_required
def about():
    return render_template('about.html')

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5013)
