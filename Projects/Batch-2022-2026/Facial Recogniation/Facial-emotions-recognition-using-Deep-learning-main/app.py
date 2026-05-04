"""
Facial Emotion Recognition — Flask Web Application
Provides image upload, face detection, emotion classification, and analytics dashboard.
"""

import os
import json
import sqlite3
import time
from datetime import datetime
from functools import wraps

import cv2
import numpy as np
import torch
from PIL import Image
from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, send_from_directory
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'facial-emotion-recognition-secret-key-2024'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
SAMPLES_FOLDER = os.path.join(BASE_DIR, 'Dataset', 'samples')
DB_PATH = os.path.join(BASE_DIR, 'emotion.db')
MODEL_PATH = os.path.join(BASE_DIR, 'emotion_cnn_model.pth')
METRICS_PATH = os.path.join(BASE_DIR, 'models_info.json')
CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

EMOTIONS = ['Happy', 'Sad', 'Angry', 'Surprise', 'Fear', 'Disgust', 'Neutral']
EMOTION_COLORS = {
    'Happy': '#22c55e', 'Sad': '#3b82f6', 'Angry': '#ef4444',
    'Surprise': '#f59e0b', 'Fear': '#8b5cf6', 'Disgust': '#84cc16', 'Neutral': '#6b7280'
}
EMOTION_ICONS = {
    'Happy': 'fa-face-smile', 'Sad': 'fa-face-sad-tear', 'Angry': 'fa-face-angry',
    'Surprise': 'fa-face-surprise', 'Fear': 'fa-face-flushed',
    'Disgust': 'fa-face-grimace', 'Neutral': 'fa-face-meh'
}
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ── Load CNN Model ──────────────────────────────────────────────
from train_model import EmotionCNN


def load_model():
    """Load trained CNN model."""
    device = torch.device('cpu')
    model = EmotionCNN(num_classes=7)
    if os.path.exists(MODEL_PATH):
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
        model.eval()
        print("CNN model loaded successfully")
    else:
        print("WARNING: Model file not found. Run train_model.py first.")
    return model


model = load_model()
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)


# ── Database ────────────────────────────────────────────────────
def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables and seed admin user."""
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            emotion TEXT NOT NULL,
            confidence REAL NOT NULL,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    # Seed admin user
    existing = conn.execute('SELECT id FROM users WHERE username = ?', ('admin',)).fetchone()
    if not existing:
        conn.execute(
            'INSERT INTO users (username, password, name) VALUES (?, ?, ?)',
            ('admin', generate_password_hash('admin123'), 'Administrator')
        )
    conn.commit()
    conn.close()


init_db()


# ── Auth Decorator ──────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ── Prediction Pipeline ────────────────────────────────────────
def predict_emotion(image_path):
    """
    Detect face in image, classify emotion.
    Returns (emotion, confidence) or (None, None) if no face detected.
    """
    img = cv2.imread(image_path)
    if img is None:
        return None, None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        # Try with more relaxed parameters
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(20, 20))

    if len(faces) == 0:
        return None, None

    # Use the largest detected face
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    face_roi = gray[y:y + h, x:x + w]
    face_resized = cv2.resize(face_roi, (48, 48))
    face_normalized = face_resized.astype(np.float32) / 255.0

    # Predict
    input_tensor = torch.FloatTensor(face_normalized).unsqueeze(0).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.softmax(output, dim=1)
        confidence, predicted = torch.max(probabilities, 1)

    emotion = EMOTIONS[predicted.item()]
    conf = confidence.item() * 100

    return emotion, round(conf, 2)


# ── Routes ──────────────────────────────────────────────────────

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))

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
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        name = request.form.get('name', '').strip()

        if not username or not password or not name:
            flash('All fields are required.', 'danger')
            return render_template('register.html')

        if len(password) < 4:
            flash('Password must be at least 4 characters.', 'danger')
            return render_template('register.html')

        conn = get_db()
        existing = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        if existing:
            conn.close()
            flash('Username already exists.', 'danger')
            return render_template('register.html')

        conn.execute(
            'INSERT INTO users (username, password, name) VALUES (?, ?, ?)',
            (username, generate_password_hash(password), name)
        )
        conn.commit()
        conn.close()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    conn = get_db()

    # Total predictions by this user
    total = conn.execute(
        'SELECT COUNT(*) as cnt FROM predictions WHERE user_id = ?',
        (session['user_id'],)
    ).fetchone()['cnt']

    # Emotion distribution
    distribution = conn.execute(
        'SELECT emotion, COUNT(*) as cnt FROM predictions WHERE user_id = ? GROUP BY emotion ORDER BY cnt DESC',
        (session['user_id'],)
    ).fetchall()

    # Recent predictions (last 5)
    recent = conn.execute(
        'SELECT * FROM predictions WHERE user_id = ? ORDER BY created_at DESC LIMIT 5',
        (session['user_id'],)
    ).fetchall()

    # Most detected emotion
    top_emotion = distribution[0]['emotion'] if distribution else 'N/A'

    # Total users
    total_users = conn.execute('SELECT COUNT(*) as cnt FROM users').fetchone()['cnt']

    conn.close()

    return render_template('home.html',
                           total_predictions=total,
                           distribution=distribution,
                           recent=recent,
                           top_emotion=top_emotion,
                           total_users=total_users,
                           emotion_colors=EMOTION_COLORS,
                           emotion_icons=EMOTION_ICONS)


@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    result = None
    error = None
    uploaded_image = None

    if request.method == 'POST':
        if 'image' not in request.files:
            error = 'No image file uploaded.'
        else:
            file = request.files['image']
            if file.filename == '':
                error = 'No file selected.'
            elif not allowed_file(file.filename):
                error = 'Invalid file type. Please upload JPG, PNG, GIF, BMP, or WEBP.'
            else:
                # Save with secure naming
                ext = file.filename.rsplit('.', 1)[1].lower()
                timestamp = int(time.time() * 1000)
                safe_name = f"{session['user_id']}_{timestamp}_{secure_filename(file.filename)}"
                filepath = os.path.join(UPLOAD_FOLDER, safe_name)
                file.save(filepath)
                uploaded_image = safe_name

                # Predict emotion
                emotion, confidence = predict_emotion(filepath)

                if emotion is None:
                    error = 'No face detected in the image. Please upload a clearer face image with good lighting and a front-facing pose.'
                else:
                    # Save to database
                    conn = get_db()
                    conn.execute(
                        'INSERT INTO predictions (user_id, image_path, emotion, confidence) VALUES (?, ?, ?, ?)',
                        (session['user_id'], safe_name, emotion, confidence)
                    )
                    conn.commit()
                    conn.close()

                    result = {
                        'emotion': emotion,
                        'confidence': confidence,
                        'color': EMOTION_COLORS.get(emotion, '#8b5cf6'),
                        'icon': EMOTION_ICONS.get(emotion, 'fa-face-meh')
                    }

    return render_template('predict.html', result=result, error=error,
                           uploaded_image=uploaded_image, emotions=EMOTIONS,
                           emotion_colors=EMOTION_COLORS, emotion_icons=EMOTION_ICONS)


@app.route('/history')
@login_required
def history():
    conn = get_db()
    predictions = conn.execute(
        'SELECT * FROM predictions WHERE user_id = ? ORDER BY created_at DESC',
        (session['user_id'],)
    ).fetchall()
    conn.close()

    return render_template('history.html', predictions=predictions,
                           emotion_colors=EMOTION_COLORS, emotion_icons=EMOTION_ICONS)


@app.route('/dashboard')
@login_required
def dashboard():
    # Load model metrics
    metrics = {}
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, 'r') as f:
            metrics = json.load(f)

    # Check which charts exist
    charts = []
    chart_files = [
        ('accuracy.png', 'Training & Validation Accuracy'),
        ('loss.png', 'Training & Validation Loss'),
        ('confusion_matrix.png', 'Confusion Matrix'),
        ('per_class_accuracy.png', 'Per-Class Accuracy'),
        ('classification_report.png', 'Classification Report'),
    ]
    charts_dir = os.path.join(BASE_DIR, 'static', 'charts')
    for fname, title in chart_files:
        if os.path.exists(os.path.join(charts_dir, fname)):
            charts.append({'file': fname, 'title': title})

    return render_template('dashboard.html', metrics=metrics, charts=charts)


@app.route('/download_sample/<filename>')
@login_required
def download_sample(filename):
    return send_from_directory(SAMPLES_FOLDER, filename, as_attachment=True)


@app.route('/about')
@login_required
def about():
    # Get sample files
    samples = []
    if os.path.exists(SAMPLES_FOLDER):
        samples = sorted([f for f in os.listdir(SAMPLES_FOLDER) if f.endswith('.png')])

    return render_template('about.html', emotions=EMOTIONS,
                           emotion_colors=EMOTION_COLORS, emotion_icons=EMOTION_ICONS,
                           samples=samples)


# ── Error Handlers ──────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    flash('Page not found.', 'warning')
    return redirect(url_for('home'))


@app.errorhandler(500)
def server_error(e):
    flash('An internal error occurred. Please try again.', 'danger')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5018)
