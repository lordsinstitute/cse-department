"""
Brain Hemorrhage Detection - Flask Web Application
Deep Learning & ML approaches for brain CT scan analysis.
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import numpy as np
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'brain_hemorrhage_detection_2025'
DB_PATH = 'hemorrhage.db'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tif', 'tiff'}
IMG_SIZE = 128

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---- CNN Model Definition (must match train_model.py) ----

class BrainCNN(nn.Module):
    def __init__(self):
        super(BrainCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256 * (IMG_SIZE // 16) * (IMG_SIZE // 16), 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


# ---- Load Model ----

model = None
models_info = {}

def load_model():
    global model, models_info
    model_path = 'brain_cnn_model.pth'
    if os.path.exists(model_path):
        model = BrainCNN()
        model.load_state_dict(torch.load(model_path, map_location='cpu', weights_only=True))
        model.eval()
        print('CNN model loaded successfully.')
    else:
        print('WARNING: brain_cnn_model.pth not found. Run train_model.py first.')

    info_path = 'models_info.json'
    if os.path.exists(info_path):
        with open(info_path, 'r') as f:
            models_info = json.load(f)

load_model()


# ---- Database ----

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
        role TEXT DEFAULT 'user'
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        image_path TEXT NOT NULL,
        prediction TEXT NOT NULL,
        confidence REAL NOT NULL,
        scan_date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)",
                  ('admin', generate_password_hash('admin123'), 'Administrator', 'admin'))

    conn.commit()
    conn.close()

init_db()


# ---- Helpers ----

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def predict_image(image_path):
    """Run CNN prediction on a brain CT image."""
    if model is None:
        return 'Error', 0.0

    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
    ])

    img = Image.open(image_path).convert('RGB')
    img_tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        output = model(img_tensor)
        prob = output.item()

    # class_to_idx: hemorrhage=0, normal=1 (alphabetical)
    # So output near 0 = hemorrhage, near 1 = normal
    if prob < 0.5:
        prediction = 'Hemorrhage Detected'
        confidence = (1 - prob) * 100
    else:
        prediction = 'Normal (No Hemorrhage)'
        confidence = prob * 100

    return prediction, round(confidence, 2)


# ---- Auth Routes ----

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        name = request.form['name'].strip()
        conn = get_db()
        try:
            conn.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)",
                         (username, generate_password_hash(password), name))
            conn.commit()
            conn.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            flash('Username already exists.', 'danger')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['name'] = user['name']
            session['role'] = user['role']
            flash(f'Welcome, {user["name"]}!', 'success')
            return redirect(url_for('home'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---- Main Routes ----

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('home'))


@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    total_scans = conn.execute("SELECT COUNT(*) FROM predictions WHERE user_id=?",
                               (session['user_id'],)).fetchone()[0]
    hemorrhage_count = conn.execute(
        "SELECT COUNT(*) FROM predictions WHERE user_id=? AND prediction LIKE '%Hemorrhage%'",
        (session['user_id'],)).fetchone()[0]
    normal_count = total_scans - hemorrhage_count

    recent = conn.execute('''
        SELECT * FROM predictions WHERE user_id=? ORDER BY id DESC LIMIT 3
    ''', (session['user_id'],)).fetchall()

    # Admin stats
    admin_stats = {}
    if session.get('role') == 'admin':
        admin_stats['total_users'] = conn.execute("SELECT COUNT(*) FROM users WHERE role='user'").fetchone()[0]
        admin_stats['total_scans'] = conn.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
        admin_stats['total_hemorrhage'] = conn.execute(
            "SELECT COUNT(*) FROM predictions WHERE prediction LIKE '%Hemorrhage%'").fetchone()[0]

    conn.close()

    # Get test samples
    sample_dir = 'static/test_samples'
    test_samples = []
    if os.path.exists(sample_dir):
        test_samples = sorted([f for f in os.listdir(sample_dir) if f.endswith('.png')])

    return render_template('home.html',
                           total_scans=total_scans,
                           hemorrhage_count=hemorrhage_count,
                           normal_count=normal_count,
                           recent=recent,
                           admin_stats=admin_stats,
                           test_samples=test_samples)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    result = None

    if request.method == 'POST':
        if 'ct_image' not in request.files:
            flash('No image file uploaded.', 'danger')
            return redirect(url_for('predict'))

        file = request.files['ct_image']
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(url_for('predict'))

        if file and allowed_file(file.filename):
            filename = secure_filename(f"{session['user_id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            prediction, confidence = predict_image(filepath)

            # Save to database
            conn = get_db()
            conn.execute(
                "INSERT INTO predictions (user_id, image_path, prediction, confidence, scan_date) VALUES (?, ?, ?, ?, ?)",
                (session['user_id'], filepath, prediction, confidence,
                 datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            )
            conn.commit()
            conn.close()

            result = {
                'image': filepath,
                'prediction': prediction,
                'confidence': confidence,
                'is_hemorrhage': 'Hemorrhage' in prediction
            }
        else:
            flash('Invalid file type. Please upload PNG, JPG, JPEG, BMP, or TIF.', 'danger')

    return render_template('predict.html', result=result)


@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    predictions = conn.execute('''
        SELECT * FROM predictions WHERE user_id=? ORDER BY id DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('history.html', predictions=predictions)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    user_preds = conn.execute("SELECT * FROM predictions WHERE user_id=?",
                              (session['user_id'],)).fetchall()

    # Prediction distribution
    pred_counts = {'Hemorrhage Detected': 0, 'Normal (No Hemorrhage)': 0}
    for p in user_preds:
        if 'Hemorrhage' in p['prediction']:
            pred_counts['Hemorrhage Detected'] += 1
        else:
            pred_counts['Normal (No Hemorrhage)'] += 1

    # Confidence distribution
    conf_ranges = {'90-100%': 0, '80-90%': 0, '70-80%': 0, '60-70%': 0, '50-60%': 0}
    for p in user_preds:
        c = p['confidence']
        if c >= 90: conf_ranges['90-100%'] += 1
        elif c >= 80: conf_ranges['80-90%'] += 1
        elif c >= 70: conf_ranges['70-80%'] += 1
        elif c >= 60: conf_ranges['60-70%'] += 1
        else: conf_ranges['50-60%'] += 1

    conn.close()

    return render_template('dashboard.html',
                           models_info=models_info,
                           pred_data=json.dumps(pred_counts),
                           conf_data=json.dumps(conf_ranges),
                           total_scans=len(user_preds))


@app.route('/about')
def about():
    return render_template('about.html', models_info=models_info)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
