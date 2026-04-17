"""
Brain Stroke Detection — Flask Web Application
Upload CT brain images for AI-powered stroke detection using CNN.
"""

import os
import json
import sqlite3
from datetime import datetime
from functools import wraps

import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from flask import (Flask, render_template, request, redirect, url_for,
                   session, flash, send_from_directory)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from train_model import StrokeCNN

app = Flask(__name__)
app.secret_key = 'stroke-detection-secret-key-2025'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'stroke_detection.db')
MODEL_PATH = os.path.join(BASE_DIR, 'stroke_cnn_model.pth')
MODELS_INFO_PATH = os.path.join(BASE_DIR, 'models_info.json')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
SAMPLES_FOLDER = os.path.join(BASE_DIR, 'static', 'test_samples')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tif', 'tiff'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load CNN model
device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
model = StrokeCNN().to(device)
if os.path.exists(MODEL_PATH):
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
    model.eval()
    print(f'CNN model loaded from {MODEL_PATH}')
else:
    print(f'WARNING: Model not found at {MODEL_PATH}. Run train_model.py first.')

# Load model metrics
models_info = {}
if os.path.exists(MODELS_INFO_PATH):
    with open(MODELS_INFO_PATH) as f:
        models_info = json.load(f)


def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables and seed admin user."""
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        image_path TEXT NOT NULL,
        prediction TEXT NOT NULL,
        confidence REAL NOT NULL,
        scan_date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    # Seed admin user
    existing = conn.execute('SELECT id FROM users WHERE username = ?', ('admin',)).fetchone()
    if not existing:
        conn.execute(
            'INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)',
            ('admin', generate_password_hash('admin123'), 'Administrator', 'admin')
        )
        print('Admin user created (admin / admin123)')

    conn.commit()
    conn.close()


def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def allowed_file(filename):
    """Check if uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def predict_image(image_path):
    """Run CNN prediction on a CT brain image."""
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
    ])

    img = Image.open(image_path)
    img_tensor = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(img_tensor).item()

    # Class mapping: ImageFolder sorts alphabetically
    # normal=0, stroke=1
    # output >= 0.5 -> class 1 (stroke), output < 0.5 -> class 0 (normal)
    if output >= 0.5:
        prediction = 'Stroke Detected'
        confidence = output * 100
    else:
        prediction = 'Normal (No Stroke)'
        confidence = (1 - output) * 100

    return prediction, round(confidence, 2)


# ─── Routes ───────────────────────────────────────────────────

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not name or not username or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))

        conn = get_db()
        existing = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        if existing:
            conn.close()
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))

        conn.execute(
            'INSERT INTO users (username, password, name) VALUES (?, ?, ?)',
            (username, generate_password_hash(password), name)
        )
        conn.commit()
        conn.close()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['name'] = user['name']
            session['role'] = user['role']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))

        flash('Invalid username or password.', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    conn = get_db()
    user_id = session['user_id']

    # User stats
    total_scans = conn.execute(
        'SELECT COUNT(*) FROM predictions WHERE user_id = ?', (user_id,)
    ).fetchone()[0]
    stroke_count = conn.execute(
        'SELECT COUNT(*) FROM predictions WHERE user_id = ? AND prediction = ?',
        (user_id, 'Stroke Detected')
    ).fetchone()[0]
    normal_count = conn.execute(
        'SELECT COUNT(*) FROM predictions WHERE user_id = ? AND prediction = ?',
        (user_id, 'Normal (No Stroke)')
    ).fetchone()[0]

    # Recent scans
    recent = conn.execute(
        'SELECT * FROM predictions WHERE user_id = ? ORDER BY id DESC LIMIT 5',
        (user_id,)
    ).fetchall()

    # Admin stats
    admin_stats = None
    if session.get('role') == 'admin':
        total_users = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        total_all_scans = conn.execute('SELECT COUNT(*) FROM predictions').fetchone()[0]
        all_stroke = conn.execute(
            "SELECT COUNT(*) FROM predictions WHERE prediction = 'Stroke Detected'"
        ).fetchone()[0]
        admin_stats = {
            'total_users': total_users,
            'total_scans': total_all_scans,
            'stroke_count': all_stroke,
            'normal_count': total_all_scans - all_stroke
        }

    conn.close()

    # Sample images
    samples = []
    if os.path.exists(SAMPLES_FOLDER):
        samples = sorted([f for f in os.listdir(SAMPLES_FOLDER) if f.endswith('.png')])

    return render_template('home.html',
                           total_scans=total_scans,
                           stroke_count=stroke_count,
                           normal_count=normal_count,
                           recent=recent,
                           admin_stats=admin_stats,
                           samples=samples)


@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    result = None

    if request.method == 'POST':
        if 'ct_image' not in request.files:
            flash('No file selected.', 'danger')
            return redirect(url_for('predict'))

        file = request.files['ct_image']
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(url_for('predict'))

        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload PNG, JPG, BMP, or TIFF.', 'danger')
            return redirect(url_for('predict'))

        # Save uploaded file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = secure_filename(file.filename)
        save_name = f'{session["user_id"]}_{timestamp}_{filename}'
        filepath = os.path.join(UPLOAD_FOLDER, save_name)
        file.save(filepath)

        # Run prediction
        prediction, confidence = predict_image(filepath)
        scan_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Save to database
        image_path = f'static/uploads/{save_name}'
        conn = get_db()
        conn.execute(
            'INSERT INTO predictions (user_id, image_path, prediction, confidence, scan_date) '
            'VALUES (?, ?, ?, ?, ?)',
            (session['user_id'], image_path, prediction, confidence, scan_date)
        )
        conn.commit()
        conn.close()

        result = {
            'prediction': prediction,
            'confidence': confidence,
            'image_path': image_path,
            'scan_date': scan_date,
            'is_stroke': prediction == 'Stroke Detected'
        }

    return render_template('predict.html', result=result)


@app.route('/history')
@login_required
def history():
    conn = get_db()
    scans = conn.execute(
        'SELECT * FROM predictions WHERE user_id = ? ORDER BY id DESC',
        (session['user_id'],)
    ).fetchall()
    conn.close()
    return render_template('history.html', scans=scans)


@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    user_id = session['user_id']

    # User prediction distribution
    stroke_count = conn.execute(
        'SELECT COUNT(*) FROM predictions WHERE user_id = ? AND prediction = ?',
        (user_id, 'Stroke Detected')
    ).fetchone()[0]
    normal_count = conn.execute(
        'SELECT COUNT(*) FROM predictions WHERE user_id = ? AND prediction = ?',
        (user_id, 'Normal (No Stroke)')
    ).fetchone()[0]

    # Confidence distribution
    confidence_ranges = []
    for low, high in [(90, 100), (80, 90), (70, 80), (60, 70), (50, 60)]:
        count = conn.execute(
            'SELECT COUNT(*) FROM predictions WHERE user_id = ? AND confidence >= ? AND confidence < ?',
            (user_id, low, high if high < 100 else 101)
        ).fetchone()[0]
        confidence_ranges.append({'range': f'{low}-{high}%', 'count': count})

    conn.close()

    return render_template('dashboard.html',
                           models_info=json.dumps(models_info),
                           stroke_count=stroke_count,
                           normal_count=normal_count,
                           confidence_ranges=json.dumps(confidence_ranges))


@app.route('/about')
@login_required
def about():
    return render_template('about.html')


@app.route('/download_sample/<filename>')
@login_required
def download_sample(filename):
    return send_from_directory(SAMPLES_FOLDER, filename, as_attachment=True)


# ─── Main ─────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5010)
