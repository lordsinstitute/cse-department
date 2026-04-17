"""
B6 — Medical Report Management & Distribution System Using Blockchain
Flask application with SQLite database and blockchain simulation.
"""
import os
import sqlite3
import json
from datetime import datetime
from flask import (Flask, render_template, request, redirect, url_for,
                   session, flash, send_from_directory, jsonify)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from blockchain import Blockchain, hash_file

app = Flask(__name__)
app.secret_key = 'medical_blockchain_2025'
app.jinja_env.filters['from_json'] = json.loads

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'medical_blockchain.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

REPORT_TYPES = [
    'Blood Test', 'X-Ray', 'MRI Scan', 'CT Scan', 'Ultrasound',
    'ECG', 'Prescription', 'Pathology', 'Urine Test', 'Other'
]

SPECIALIZATIONS = [
    'General Medicine', 'Cardiology', 'Neurology', 'Orthopedics',
    'Dermatology', 'Pediatrics', 'Radiology', 'Pathology',
    'Ophthalmology', 'ENT', 'Gynecology', 'Psychiatry', 'Other'
]


# ─────────────────── Database ───────────────────

def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    return db


def init_db():
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'patient',
            specialization TEXT,
            email TEXT,
            phone TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS medical_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            report_type TEXT NOT NULL,
            description TEXT,
            file_path TEXT NOT NULL,
            file_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES users(id),
            FOREIGN KEY (doctor_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS access_grants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL,
            patient_id INTEGER NOT NULL,
            granted_to INTEGER NOT NULL,
            is_active INTEGER DEFAULT 1,
            granted_at TEXT DEFAULT CURRENT_TIMESTAMP,
            revoked_at TEXT,
            FOREIGN KEY (report_id) REFERENCES medical_reports(id),
            FOREIGN KEY (patient_id) REFERENCES users(id),
            FOREIGN KEY (granted_to) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS blockchain (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            block_index INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            data TEXT NOT NULL,
            data_hash TEXT NOT NULL,
            previous_hash TEXT NOT NULL,
            block_hash TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            details TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')

    # Seed admin
    existing = db.execute('SELECT id FROM users WHERE username = ?',
                          ('admin',)).fetchone()
    if not existing:
        db.execute('INSERT INTO users (name, username, password, role) VALUES (?, ?, ?, ?)',
                   ('Administrator', 'admin',
                    generate_password_hash('admin123'), 'admin'))

    # Seed sample doctor
    existing = db.execute('SELECT id FROM users WHERE username = ?',
                          ('dr_ahmed',)).fetchone()
    if not existing:
        db.execute('''INSERT INTO users (name, username, password, role, specialization, email, phone)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   ('Dr. Ahmed Haleem', 'dr_ahmed',
                    generate_password_hash('doctor123'), 'doctor',
                    'General Medicine', 'dr.ahmed@hospital.com', '9876543210'))

    # Seed sample patient
    existing = db.execute('SELECT id FROM users WHERE username = ?',
                          ('patient1',)).fetchone()
    if not existing:
        db.execute('''INSERT INTO users (name, username, password, role, email, phone)
                      VALUES (?, ?, ?, ?, ?, ?)''',
                   ('Asiya Ali', 'patient1',
                    generate_password_hash('patient123'), 'patient',
                    'asiya@email.com', '9123456789'))

    db.commit()

    # Initialize blockchain (creates genesis block)
    chain = Blockchain(db)

    # Seed sample reports if none exist
    report_count = db.execute('SELECT COUNT(*) FROM medical_reports').fetchone()[0]
    if report_count == 0:
        doctor = db.execute('SELECT id FROM users WHERE username = ?', ('dr_ahmed',)).fetchone()
        patient = db.execute('SELECT id FROM users WHERE username = ?', ('patient1',)).fetchone()
        if doctor and patient:
            samples = [
                ('Complete Blood Count (CBC)', 'Blood Test',
                 'All values within normal range. Hemoglobin: 14.2 g/dL, WBC: 7500/uL, Platelets: 250000/uL'),
                ('Chest X-Ray Report', 'X-Ray',
                 'No abnormalities detected. Lungs clear. Heart size normal. No fractures observed.'),
                ('General Health Prescription', 'Prescription',
                 'Vitamin D3 60000 IU weekly x 8 weeks. Calcium 500mg daily. Follow up after 2 months.'),
            ]
            for title, rtype, desc in samples:
                # Create a dummy file hash for seeded reports
                dummy_hash = hash_file.__module__  # just need a placeholder
                import hashlib
                file_hash = hashlib.sha256(f"{title}{desc}".encode()).hexdigest()
                db.execute('''INSERT INTO medical_reports
                    (patient_id, doctor_id, title, report_type, description, file_path, file_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (patient['id'], doctor['id'], title, rtype, desc,
                     'sample_report.pdf', file_hash))
                db.commit()

                report = db.execute('SELECT id FROM medical_reports WHERE title = ?',
                                    (title,)).fetchone()
                chain.add_block('REPORT_UPLOADED', {
                    'report_id': report['id'],
                    'title': title,
                    'doctor': 'Dr. Ahmed Haleem',
                    'patient': 'Asiya Ali',
                    'file_hash': file_hash
                })
                db.execute('INSERT INTO audit_log (user_id, action, details) VALUES (?, ?, ?)',
                           (doctor['id'], 'REPORT_UPLOADED',
                            f'Uploaded "{title}" for patient Asiya Ali'))
            db.commit()

    db.close()


def log_audit(db, user_id, action, details):
    db.execute('INSERT INTO audit_log (user_id, action, details) VALUES (?, ?, ?)',
               (user_id, action, details))
    db.commit()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ─────────────────── Auth Routes ───────────────────

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            flash('Please fill in all fields.', 'danger')
            return render_template('login.html')

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?',
                          (username,)).fetchone()
        db.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['name'] = user['name']
            session['role'] = user['role']
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'patient')
        specialization = request.form.get('specialization', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()

        if not name or not username or not password:
            flash('Name, username and password are required.', 'danger')
            return render_template('register.html', specializations=SPECIALIZATIONS)

        if role not in ('patient', 'doctor'):
            flash('Invalid role selected.', 'danger')
            return render_template('register.html', specializations=SPECIALIZATIONS)

        if role == 'doctor' and not specialization:
            flash('Specialization is required for doctors.', 'danger')
            return render_template('register.html', specializations=SPECIALIZATIONS)

        db = get_db()
        try:
            db.execute('''INSERT INTO users (name, username, password, role, specialization, email, phone)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (name, username, generate_password_hash(password),
                        role, specialization if role == 'doctor' else None,
                        email or None, phone or None))
            db.commit()
            log_audit(db, None, 'USER_REGISTERED',
                      f'{role.title()} "{username}" registered')
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'danger')
        finally:
            db.close()

    return render_template('register.html', specializations=SPECIALIZATIONS)


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))


# ─────────────────── Home ───────────────────

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    role = session['role']
    data = {}

    if role == 'admin':
        data['total_users'] = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        data['total_doctors'] = db.execute(
            "SELECT COUNT(*) FROM users WHERE role='doctor'").fetchone()[0]
        data['total_patients'] = db.execute(
            "SELECT COUNT(*) FROM users WHERE role='patient'").fetchone()[0]
        data['total_reports'] = db.execute('SELECT COUNT(*) FROM medical_reports').fetchone()[0]
        data['total_blocks'] = db.execute('SELECT COUNT(*) FROM blockchain').fetchone()[0]
        data['total_grants'] = db.execute(
            'SELECT COUNT(*) FROM access_grants WHERE is_active=1').fetchone()[0]
        data['recent_audit'] = db.execute('''
            SELECT a.*, u.name as user_name FROM audit_log a
            LEFT JOIN users u ON a.user_id = u.id
            ORDER BY a.id DESC LIMIT 8
        ''').fetchall()

    elif role == 'doctor':
        uid = session['user_id']
        data['reports_uploaded'] = db.execute(
            'SELECT COUNT(*) FROM medical_reports WHERE doctor_id=?', (uid,)).fetchone()[0]
        data['patients_served'] = db.execute(
            'SELECT COUNT(DISTINCT patient_id) FROM medical_reports WHERE doctor_id=?',
            (uid,)).fetchone()[0]
        data['shared_with_me'] = db.execute(
            'SELECT COUNT(*) FROM access_grants WHERE granted_to=? AND is_active=1',
            (uid,)).fetchone()[0]
        data['recent_reports'] = db.execute('''
            SELECT r.*, u.name as patient_name FROM medical_reports r
            JOIN users u ON r.patient_id = u.id
            WHERE r.doctor_id = ? ORDER BY r.id DESC LIMIT 5
        ''', (uid,)).fetchall()

    elif role == 'patient':
        uid = session['user_id']
        data['my_reports'] = db.execute(
            'SELECT COUNT(*) FROM medical_reports WHERE patient_id=?', (uid,)).fetchone()[0]
        data['active_shares'] = db.execute(
            'SELECT COUNT(*) FROM access_grants WHERE patient_id=? AND is_active=1',
            (uid,)).fetchone()[0]
        data['doctors_count'] = db.execute(
            'SELECT COUNT(DISTINCT doctor_id) FROM medical_reports WHERE patient_id=?',
            (uid,)).fetchone()[0]
        data['recent_reports'] = db.execute('''
            SELECT r.*, u.name as doctor_name FROM medical_reports r
            JOIN users u ON r.doctor_id = u.id
            WHERE r.patient_id = ? ORDER BY r.id DESC LIMIT 5
        ''', (uid,)).fetchall()

    db.close()
    return render_template('home.html', data=data)


# ─────────────────── Upload Report (Doctor) ───────────────────

@app.route('/upload', methods=['GET', 'POST'])
def upload_report():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session['role'] != 'doctor':
        flash('Only doctors can upload reports.', 'danger')
        return redirect(url_for('home'))

    db = get_db()
    patients = db.execute("SELECT id, name, username FROM users WHERE role='patient' ORDER BY name").fetchall()

    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        title = request.form.get('title', '').strip()
        report_type = request.form.get('report_type', '')
        description = request.form.get('description', '').strip()
        file = request.files.get('report_file')

        if not patient_id or not title or not report_type:
            flash('Patient, title, and report type are required.', 'danger')
            db.close()
            return render_template('upload_report.html', patients=patients,
                                   report_types=REPORT_TYPES)

        if not file or file.filename == '':
            flash('Please select a file to upload.', 'danger')
            db.close()
            return render_template('upload_report.html', patients=patients,
                                   report_types=REPORT_TYPES)

        if not allowed_file(file.filename):
            flash('Only PDF, PNG, JPG files are allowed.', 'danger')
            db.close()
            return render_template('upload_report.html', patients=patients,
                                   report_types=REPORT_TYPES)

        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Compute file hash
        file_hash = hash_file(filepath)

        # Save to database
        db.execute('''INSERT INTO medical_reports
            (patient_id, doctor_id, title, report_type, description, file_path, file_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (patient_id, session['user_id'], title, report_type,
             description, filename, file_hash))
        db.commit()

        report = db.execute('SELECT * FROM medical_reports ORDER BY id DESC LIMIT 1').fetchone()
        patient = db.execute('SELECT name FROM users WHERE id=?', (patient_id,)).fetchone()

        # Add to blockchain
        chain = Blockchain(db)
        chain.add_block('REPORT_UPLOADED', {
            'report_id': report['id'],
            'title': title,
            'type': report_type,
            'doctor': session['name'],
            'patient': patient['name'],
            'file_hash': file_hash
        })

        log_audit(db, session['user_id'], 'REPORT_UPLOADED',
                  f'Uploaded "{title}" ({report_type}) for {patient["name"]}')
        db.close()
        flash(f'Report "{title}" uploaded successfully and recorded on blockchain.', 'success')
        return redirect(url_for('home'))

    db.close()
    return render_template('upload_report.html', patients=patients,
                           report_types=REPORT_TYPES)


# ─────────────────── My Reports (Patient) ───────────────────

@app.route('/my-reports')
def my_reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session['role'] != 'patient':
        flash('This page is for patients only.', 'danger')
        return redirect(url_for('home'))

    db = get_db()
    reports = db.execute('''
        SELECT r.*, u.name as doctor_name, u.specialization
        FROM medical_reports r
        JOIN users u ON r.doctor_id = u.id
        WHERE r.patient_id = ?
        ORDER BY r.id DESC
    ''', (session['user_id'],)).fetchall()
    db.close()
    return render_template('my_reports.html', reports=reports)


# ─────────────────── Patient Reports (Doctor) ───────────────────

@app.route('/patient-reports')
def patient_reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session['role'] != 'doctor':
        flash('This page is for doctors only.', 'danger')
        return redirect(url_for('home'))

    db = get_db()
    uid = session['user_id']

    # Reports uploaded by this doctor
    uploaded = db.execute('''
        SELECT r.*, u.name as patient_name
        FROM medical_reports r
        JOIN users u ON r.patient_id = u.id
        WHERE r.doctor_id = ?
        ORDER BY r.id DESC
    ''', (uid,)).fetchall()

    # Reports shared with this doctor by patients
    shared = db.execute('''
        SELECT r.*, u.name as patient_name, d.name as doctor_name
        FROM access_grants ag
        JOIN medical_reports r ON ag.report_id = r.id
        JOIN users u ON r.patient_id = u.id
        JOIN users d ON r.doctor_id = d.id
        WHERE ag.granted_to = ? AND ag.is_active = 1
        ORDER BY ag.granted_at DESC
    ''', (uid,)).fetchall()

    db.close()
    return render_template('patient_reports.html', uploaded=uploaded, shared=shared)


# ─────────────────── View Single Report ───────────────────

@app.route('/report/<int:report_id>')
def view_report(report_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    report = db.execute('''
        SELECT r.*, p.name as patient_name, d.name as doctor_name, d.specialization
        FROM medical_reports r
        JOIN users u ON r.patient_id = u.id
        JOIN users p ON r.patient_id = p.id
        JOIN users d ON r.doctor_id = d.id
        WHERE r.id = ?
    ''', (report_id,)).fetchone()

    if not report:
        flash('Report not found.', 'danger')
        db.close()
        return redirect(url_for('home'))

    # Access check
    uid = session['user_id']
    role = session['role']
    has_access = False
    if role == 'admin':
        has_access = True
    elif role == 'patient' and report['patient_id'] == uid:
        has_access = True
    elif role == 'doctor' and report['doctor_id'] == uid:
        has_access = True
    elif role == 'doctor':
        grant = db.execute('''SELECT id FROM access_grants
            WHERE report_id=? AND granted_to=? AND is_active=1''',
            (report_id, uid)).fetchone()
        if grant:
            has_access = True

    if not has_access:
        flash('You do not have access to this report.', 'danger')
        db.close()
        return redirect(url_for('home'))

    # Get blockchain record for this report
    blocks = db.execute('''SELECT * FROM blockchain WHERE data LIKE ?
        ORDER BY block_index ASC''',
        (f'%"report_id": {report_id}%',)).fetchall()

    # Log view on blockchain
    chain = Blockchain(db)
    chain.add_block('REPORT_VIEWED', {
        'report_id': report_id,
        'title': report['title'],
        'viewed_by': session['name'],
        'role': session['role']
    })
    log_audit(db, uid, 'REPORT_VIEWED', f'Viewed "{report["title"]}"')

    db.close()
    return render_template('view_report.html', report=report, blocks=blocks)


# ─────────────────── Share / Revoke Access ───────────────────

@app.route('/share/<int:report_id>', methods=['GET', 'POST'])
def share_report(report_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session['role'] != 'patient':
        flash('Only patients can share their reports.', 'danger')
        return redirect(url_for('home'))

    db = get_db()
    report = db.execute('SELECT * FROM medical_reports WHERE id=? AND patient_id=?',
                        (report_id, session['user_id'])).fetchone()
    if not report:
        flash('Report not found or you do not own it.', 'danger')
        db.close()
        return redirect(url_for('my_reports'))

    if request.method == 'POST':
        action = request.form.get('action')
        doctor_id = request.form.get('doctor_id')

        if not doctor_id:
            flash('Please select a doctor.', 'danger')
        elif action == 'grant':
            existing = db.execute('''SELECT id, is_active FROM access_grants
                WHERE report_id=? AND granted_to=?''',
                (report_id, doctor_id)).fetchone()
            if existing and existing['is_active']:
                flash('Access already granted to this doctor.', 'warning')
            else:
                if existing:
                    db.execute('''UPDATE access_grants SET is_active=1, revoked_at=NULL,
                        granted_at=CURRENT_TIMESTAMP WHERE id=?''', (existing['id'],))
                else:
                    db.execute('''INSERT INTO access_grants
                        (report_id, patient_id, granted_to) VALUES (?, ?, ?)''',
                        (report_id, session['user_id'], doctor_id))
                db.commit()

                doctor = db.execute('SELECT name FROM users WHERE id=?', (doctor_id,)).fetchone()
                chain = Blockchain(db)
                chain.add_block('ACCESS_GRANTED', {
                    'report_id': report_id,
                    'title': report['title'],
                    'patient': session['name'],
                    'granted_to': doctor['name']
                })
                log_audit(db, session['user_id'], 'ACCESS_GRANTED',
                          f'Granted access to "{report["title"]}" for {doctor["name"]}')
                flash(f'Access granted to {doctor["name"]}.', 'success')

        elif action == 'revoke':
            db.execute('''UPDATE access_grants SET is_active=0, revoked_at=CURRENT_TIMESTAMP
                WHERE report_id=? AND granted_to=? AND is_active=1''',
                (report_id, doctor_id))
            db.commit()

            doctor = db.execute('SELECT name FROM users WHERE id=?', (doctor_id,)).fetchone()
            chain = Blockchain(db)
            chain.add_block('ACCESS_REVOKED', {
                'report_id': report_id,
                'title': report['title'],
                'patient': session['name'],
                'revoked_from': doctor['name']
            })
            log_audit(db, session['user_id'], 'ACCESS_REVOKED',
                      f'Revoked access to "{report["title"]}" from {doctor["name"]}')
            flash(f'Access revoked from {doctor["name"]}.', 'success')

    # Get all doctors
    doctors = db.execute("SELECT id, name, specialization FROM users WHERE role='doctor' ORDER BY name").fetchall()
    # Get current grants for this report
    grants = db.execute('''SELECT ag.*, u.name as doctor_name, u.specialization
        FROM access_grants ag JOIN users u ON ag.granted_to = u.id
        WHERE ag.report_id = ? AND ag.is_active = 1''',
        (report_id,)).fetchall()

    db.close()
    return render_template('share_report.html', report=report,
                           doctors=doctors, grants=grants)


# ─────────────────── Blockchain Explorer ───────────────────

@app.route('/blockchain')
def blockchain_explorer():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    chain = Blockchain(db)
    blocks = chain.get_chain()
    db.close()
    return render_template('blockchain.html', blocks=blocks)


@app.route('/verify')
def verify_blockchain():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    chain = Blockchain(db)
    is_valid, errors, block_count = chain.verify_chain()

    chain.add_block('INTEGRITY_CHECK', {
        'verified_by': session['name'],
        'result': 'VALID' if is_valid else 'INVALID',
        'blocks_checked': block_count
    })
    log_audit(db, session['user_id'], 'INTEGRITY_CHECK',
              f'Blockchain verification: {"VALID" if is_valid else "INVALID"} ({block_count} blocks)')
    db.close()

    if is_valid:
        flash(f'Blockchain is VALID. All {block_count} blocks verified successfully.', 'success')
    else:
        flash(f'Blockchain INVALID! Errors: {", ".join(errors)}', 'danger')
    return redirect(url_for('blockchain_explorer'))


# ─────────────────── Audit Trail (Admin) ───────────────────

@app.route('/audit')
def audit_trail():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session['role'] != 'admin':
        flash('Admin access required.', 'danger')
        return redirect(url_for('home'))

    db = get_db()
    logs = db.execute('''
        SELECT a.*, u.name as user_name, u.role as user_role
        FROM audit_log a
        LEFT JOIN users u ON a.user_id = u.id
        ORDER BY a.id DESC
    ''').fetchall()
    db.close()
    return render_template('audit.html', logs=logs)


# ─────────────────── Dashboard ───────────────────

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()

    # Reports by type
    by_type = db.execute('''SELECT report_type, COUNT(*) as cnt
        FROM medical_reports GROUP BY report_type ORDER BY cnt DESC''').fetchall()

    # Reports over time (last 7 entries)
    over_time = db.execute('''SELECT DATE(created_at) as day, COUNT(*) as cnt
        FROM medical_reports GROUP BY DATE(created_at)
        ORDER BY day DESC LIMIT 7''').fetchall()
    over_time = list(reversed(over_time))

    # User distribution
    user_dist = db.execute('''SELECT role, COUNT(*) as cnt
        FROM users GROUP BY role''').fetchall()

    # Access grants stats
    grants_active = db.execute('SELECT COUNT(*) FROM access_grants WHERE is_active=1').fetchone()[0]
    grants_revoked = db.execute('SELECT COUNT(*) FROM access_grants WHERE is_active=0').fetchone()[0]

    # Blockchain stats
    total_blocks = db.execute('SELECT COUNT(*) FROM blockchain').fetchone()[0]
    total_reports = db.execute('SELECT COUNT(*) FROM medical_reports').fetchone()[0]
    total_users = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]

    db.close()
    return render_template('dashboard.html',
                           by_type=by_type, over_time=over_time,
                           user_dist=user_dist,
                           grants_active=grants_active,
                           grants_revoked=grants_revoked,
                           total_blocks=total_blocks,
                           total_reports=total_reports,
                           total_users=total_users)


# ─────────────────── About ───────────────────

@app.route('/about')
def about():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('about.html')


# ─────────────────── File Download ───────────────────

@app.route('/download/<filename>')
def download_file(filename):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


# ─────────────────── API: Dashboard Data ───────────────────

@app.route('/api/stats')
def api_stats():
    if 'user_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401

    db = get_db()
    stats = {
        'total_reports': db.execute('SELECT COUNT(*) FROM medical_reports').fetchone()[0],
        'total_users': db.execute('SELECT COUNT(*) FROM users').fetchone()[0],
        'total_blocks': db.execute('SELECT COUNT(*) FROM blockchain').fetchone()[0],
    }
    db.close()
    return jsonify(stats)


# ─────────────────── Run ───────────────────

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5005)
