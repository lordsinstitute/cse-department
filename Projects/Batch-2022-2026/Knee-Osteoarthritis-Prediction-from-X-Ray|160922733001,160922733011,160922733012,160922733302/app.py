"""
Knee Osteoarthritis Classification — Flask Web Application
Ensemble of MobileNetV2 + Custom CNN + Random Forest for KL grade classification.
Includes Grad-CAM explainability, PDF report download, and patient progression tracking.
"""

import io
import os
import json
import sqlite3
from datetime import datetime
from functools import wraps

import cv2
import joblib
import torch
import torch.nn as nn
import numpy as np
from PIL import Image
from torchvision import transforms, models
from flask import (Flask, render_template, request, redirect, url_for,
                   session, flash, send_from_directory, send_file)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'knee-oa-classification-secret-2025'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'knee_osteoarthritis.db')
MOBILENET_PATH = os.path.join(BASE_DIR, 'knee_mobilenet_model.pth')
CNN_PATH = os.path.join(BASE_DIR, 'knee_cnn_model.pth')
RF_PATH = os.path.join(BASE_DIR, 'ml_model.pkl')
MODELS_INFO_PATH = os.path.join(BASE_DIR, 'models_info.json')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
GRADCAM_FOLDER = os.path.join(BASE_DIR, 'static', 'gradcam')
SAMPLES_FOLDER = os.path.join(BASE_DIR, 'static', 'test_samples')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tif', 'tiff'}

CLASS_NAMES = ['Normal', 'Doubtful', 'Mild', 'Moderate', 'Severe']
GRADE_COLORS = {
    'Normal': '#22c55e',
    'Doubtful': '#84cc16',
    'Mild': '#eab308',
    'Moderate': '#f97316',
    'Severe': '#ef4444',
}
GRADE_HEX_RGB = {
    'Normal': (34, 197, 94),
    'Doubtful': (132, 204, 22),
    'Mild': (234, 179, 8),
    'Moderate': (249, 115, 22),
    'Severe': (239, 68, 68),
}
NUM_CLASSES = 5

# Ensemble model weights (higher = more trusted, based on overall accuracy)
ENSEMBLE_WEIGHTS = {'mobilenet': 0.55, 'cnn': 0.30, 'rf': 0.15}

# Per-class calibration to compensate for Doubtful under-prediction (7% accuracy → boost)
CALIBRATION_WEIGHTS = np.array([0.85, 2.8, 1.2, 1.3, 0.9])  # Normal/Doubtful/Mild/Moderate/Severe

# KL grade severity index (for progression comparison)
GRADE_SEVERITY = {'Normal': 0, 'Doubtful': 1, 'Mild': 2, 'Moderate': 3, 'Severe': 4}

GRADE_EXPLANATIONS = {
    'Normal': {
        'description': 'No radiographic features of osteoarthritis.',
        'findings': [
            'Normal joint space width maintained',
            'Smooth articular bone surfaces',
            'No osteophytes (bone spurs) detected',
            'No subchondral sclerosis or cysts',
            'Normal bone alignment and density',
        ],
    },
    'Doubtful': {
        'description': 'Doubtful narrowing of joint space with possible osteophytic lipping.',
        'findings': [
            'Possible minor joint space narrowing',
            'Minute osteophytes may be present at joint margins',
            'No significant bone surface changes',
            'Early signs that may require follow-up monitoring',
        ],
    },
    'Mild': {
        'description': 'Definite osteophytes and possible narrowing of joint space.',
        'findings': [
            'Definite osteophytes (bone spurs) visible at joint margins',
            'Mild narrowing of the joint space',
            'Early subchondral sclerosis (bone hardening) near joint surface',
            'Slight irregularity of articular bone surfaces',
            'Cartilage thinning beginning to occur',
        ],
    },
    'Moderate': {
        'description': 'Moderate multiple osteophytes, definite narrowing of joint space, some sclerosis and possible deformity of bone ends.',
        'findings': [
            'Multiple prominent osteophytes at joint margins',
            'Significant narrowing of joint space indicating cartilage loss',
            'Subchondral sclerosis — increased bone density near joint',
            'Possible subchondral cysts (fluid-filled cavities in bone)',
            'Early bone deformity at femoral condyles or tibial plateau',
            'Reduced space between femur and tibia bones',
        ],
    },
    'Severe': {
        'description': 'Large osteophytes, marked narrowing of joint space, severe sclerosis and definite deformity of bone ends.',
        'findings': [
            'Large osteophytes causing visible bone protrusions',
            'Severe joint space narrowing — near bone-on-bone contact',
            'Marked subchondral sclerosis with dense bone formation',
            'Subchondral bone cysts present',
            'Definite deformity of femoral condyles and tibial plateau',
            'Possible angular deformity (varus/valgus malalignment)',
            'Extensive cartilage destruction',
        ],
    },
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GRADCAM_FOLDER, exist_ok=True)

# ─── Model Definitions ────────────────────────────────────────

device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
mobilenet_model = None
cnn_model = None
rf_model = None


class KneeCNN(nn.Module):
    """Custom CNN for knee X-ray classification (grayscale input)."""

    def __init__(self, num_classes=NUM_CLASSES):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.MaxPool2d(2, 2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1), nn.BatchNorm2d(64), nn.ReLU(), nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1), nn.BatchNorm2d(128), nn.ReLU(), nn.MaxPool2d(2, 2),
            nn.Conv2d(128, 256, kernel_size=3, padding=1), nn.BatchNorm2d(256), nn.ReLU(), nn.MaxPool2d(2, 2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256 * 8 * 8, 256), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(256, num_classes),
        )

    def forward(self, x):
        return self.classifier(self.features(x))


def load_models():
    """Load all available models at startup."""
    global mobilenet_model, cnn_model, rf_model

    # MobileNetV2
    m = models.mobilenet_v2(weights=None)
    m.classifier = nn.Sequential(nn.Dropout(0.5), nn.Linear(1280, NUM_CLASSES))
    if os.path.exists(MOBILENET_PATH):
        m.load_state_dict(torch.load(MOBILENET_PATH, map_location=device, weights_only=True))
        m.eval().to(device)
        mobilenet_model = m
        print(f'MobileNetV2 loaded from {MOBILENET_PATH}')
    else:
        print(f'WARNING: MobileNetV2 not found at {MOBILENET_PATH}')

    # Custom CNN
    if os.path.exists(CNN_PATH):
        c = KneeCNN()
        c.load_state_dict(torch.load(CNN_PATH, map_location=device, weights_only=True))
        c.eval().to(device)
        cnn_model = c
        print(f'Custom CNN loaded from {CNN_PATH}')
    else:
        print(f'INFO: Custom CNN not found at {CNN_PATH} — run train_model.py to generate it')

    # Random Forest
    if os.path.exists(RF_PATH):
        rf_model = joblib.load(RF_PATH)
        print(f'Random Forest loaded from {RF_PATH}')
    else:
        print(f'INFO: Random Forest not found at {RF_PATH}')


load_models()

# Image transforms
mobilenet_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

cnn_transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
])

# Load model metrics
models_info = {}
if os.path.exists(MODELS_INFO_PATH):
    with open(MODELS_INFO_PATH) as f:
        models_info = json.load(f)


# ─── Grad-CAM ─────────────────────────────────────────────────

class GradCAM:
    """Grad-CAM for MobileNetV2."""

    def __init__(self, model, target_layer):
        self.model = model
        self.gradients = None
        self.activations = None
        target_layer.register_forward_hook(self._forward_hook)
        target_layer.register_full_backward_hook(self._backward_hook)

    def _forward_hook(self, module, input, output):
        self.activations = output.detach()

    def _backward_hook(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def generate(self, input_tensor, class_idx=None):
        self.model.eval()
        output = self.model(input_tensor)
        if class_idx is None:
            class_idx = output.argmax(dim=1).item()
        self.model.zero_grad()
        output[0, class_idx].backward()
        weights = self.gradients.mean(dim=(2, 3), keepdim=True)
        cam = (weights * self.activations).sum(dim=1, keepdim=True)
        cam = torch.relu(cam).squeeze().cpu().numpy()
        if cam.max() > 0:
            cam = cam / cam.max()
        return cam


def generate_gradcam_overlay(image_path, save_name):
    """Generate Grad-CAM heatmap overlay on the original image."""
    if mobilenet_model is None:
        return None
    img = Image.open(image_path).convert('RGB')
    img_tensor = mobilenet_transform(img).unsqueeze(0).to(device)
    target_layer = mobilenet_model.features[-1]
    grad_cam = GradCAM(mobilenet_model, target_layer)
    heatmap = grad_cam.generate(img_tensor)
    img_cv = cv2.imread(image_path)
    img_cv = cv2.resize(img_cv, (224, 224))
    heatmap_resized = cv2.resize(heatmap, (224, 224))
    heatmap_colored = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(img_cv, 0.6, heatmap_colored, 0.4, 0)
    overlay_path = os.path.join(GRADCAM_FOLDER, save_name)
    cv2.imwrite(overlay_path, overlay)
    return f'static/gradcam/{save_name}'


# ─── Ensemble Prediction ──────────────────────────────────────

def predict_ensemble(image_path):
    """Run ensemble prediction combining all available models."""
    img = Image.open(image_path).convert('RGB')

    weighted_probs = np.zeros(NUM_CLASSES)
    total_weight = 0.0
    active_models = []

    # MobileNetV2
    if mobilenet_model is not None:
        t = mobilenet_transform(img).unsqueeze(0).to(device)
        with torch.no_grad():
            probs = torch.softmax(mobilenet_model(t), dim=1)[0].cpu().numpy()
        w = ENSEMBLE_WEIGHTS['mobilenet']
        weighted_probs += w * probs
        total_weight += w
        active_models.append('MobileNetV2')

    # Custom CNN
    if cnn_model is not None:
        t = cnn_transform(img).unsqueeze(0).to(device)
        with torch.no_grad():
            probs = torch.softmax(cnn_model(t), dim=1)[0].cpu().numpy()
        w = ENSEMBLE_WEIGHTS['cnn']
        weighted_probs += w * probs
        total_weight += w
        active_models.append('Custom CNN')

    # Random Forest
    if rf_model is not None:
        t = cnn_transform(img)  # (1, 128, 128)
        X = t.numpy().flatten().reshape(1, -1)
        probs = rf_model.predict_proba(X)[0]
        w = ENSEMBLE_WEIGHTS['rf']
        weighted_probs += w * probs
        total_weight += w
        active_models.append('Random Forest')

    if total_weight == 0:
        raise RuntimeError('No models loaded. Run train_model.py first.')

    ensemble_probs = weighted_probs / total_weight

    # Apply per-class calibration (boosts Doubtful which is under-predicted)
    calibrated = ensemble_probs * CALIBRATION_WEIGHTS
    calibrated /= calibrated.sum()

    predicted_class = int(calibrated.argmax())
    confidence = round(float(calibrated[predicted_class]) * 100, 2)
    all_conf = {CLASS_NAMES[i]: round(float(calibrated[i]) * 100, 2) for i in range(NUM_CLASSES)}

    return CLASS_NAMES[predicted_class], confidence, all_conf, ' + '.join(active_models)


# ─── Database ──────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )''')

    conn.execute('''CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        notes TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    conn.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        patient_id INTEGER,
        image_path TEXT NOT NULL,
        prediction TEXT NOT NULL,
        confidence REAL NOT NULL,
        all_confidences TEXT,
        gradcam_path TEXT,
        explanation TEXT,
        models_used TEXT,
        scan_date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )''')

    # Migration: add columns to existing DBs
    for col, defn in [
        ('gradcam_path', 'TEXT'),
        ('explanation', 'TEXT'),
        ('models_used', 'TEXT'),
        ('patient_id', 'INTEGER'),
    ]:
        try:
            conn.execute(f'ALTER TABLE predictions ADD COLUMN {col} {defn}')
        except sqlite3.OperationalError:
            pass

    existing = conn.execute('SELECT id FROM users WHERE username = ?', ('admin',)).fetchone()
    if not existing:
        conn.execute(
            'INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)',
            ('admin', generate_password_hash('admin123'), 'Administrator', 'admin')
        )
        print('Admin user created (admin / admin123)')

    conn.commit()
    conn.close()


def _pt(text):
    """Sanitize text for fpdf (replaces Unicode chars unsupported by core fonts)."""
    return (str(text)
            .replace('\u2014', '-')   # em-dash
            .replace('\u2013', '-')   # en-dash
            .replace('\u2018', "'")   # left single quote
            .replace('\u2019', "'")   # right single quote
            .replace('\u201c', '"')   # left double quote
            .replace('\u201d', '"')   # right double quote
            .replace('\u2022', '*')   # bullet
            .encode('latin-1', 'replace').decode('latin-1'))


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ─── PDF Report Generation ────────────────────────────────────

def generate_report_pdf(pred_id, user_id):
    """Generate a PDF report for a given prediction."""
    try:
        from fpdf import FPDF
    except ImportError:
        return None, 'fpdf2 not installed. Run: pip install fpdf2'

    conn = get_db()
    pred = conn.execute(
        'SELECT p.*, u.name as doctor_name, pat.name as patient_name, pat.age, pat.gender '
        'FROM predictions p '
        'JOIN users u ON u.id = p.user_id '
        'LEFT JOIN patients pat ON pat.id = p.patient_id '
        'WHERE p.id = ? AND p.user_id = ?',
        (pred_id, user_id)
    ).fetchone()
    conn.close()

    if not pred:
        return None, 'Prediction not found.'

    prediction = pred['prediction']
    confidence = pred['confidence']
    scan_date = pred['scan_date']
    explanation = json.loads(pred['explanation']) if pred['explanation'] else {}
    all_conf = json.loads(pred['all_confidences']) if pred['all_confidences'] else {}
    models_used = pred['models_used'] or 'MobileNetV2'
    grade_num = GRADE_SEVERITY.get(prediction, 0)

    r, g, b = GRADE_HEX_RGB.get(prediction, (20, 184, 166))

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Header bar
    pdf.set_fill_color(10, 10, 40)
    pdf.rect(0, 0, 210, 22, 'F')
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(20, 184, 166)
    pdf.set_xy(10, 6)
    pdf.cell(0, 10, 'Knee Osteoarthritis Classification Report', ln=0)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(180, 180, 180)
    pdf.set_xy(10, 13)
    pdf.cell(0, 6, 'AI-Based Medical Image Analysis Using Deep Learning', ln=0)
    pdf.ln(24)

    # Patient / Doctor info
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 8, 'Report Details', ln=True)
    pdf.set_draw_color(20, 184, 166)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(60, 60, 60)
    info_rows = [
        ('Report ID', f'#{pred_id}'),
        ('Scan Date', scan_date),
        ('Doctor / User', pred['doctor_name']),
        ('Models Used', models_used),
    ]
    if pred['patient_name']:
        info_rows.insert(2, ('Patient Name', pred['patient_name']))
        if pred['age']:
            info_rows.insert(3, ('Age', str(pred['age'])))
        if pred['gender']:
            info_rows.insert(4, ('Gender', pred['gender']))

    for label, value in info_rows:
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(50, 7, _pt(label + ':'), ln=0)
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 7, _pt(value), ln=True)

    pdf.ln(4)

    # Diagnosis result box
    pdf.set_fill_color(r, g, b)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 13)
    pdf.cell(0, 12, _pt(f'  Diagnosis: KL Grade {grade_num} - {prediction}   ({confidence}% confidence)'),
             ln=True, fill=True)
    pdf.ln(2)

    if explanation.get('description'):
        pdf.set_font('Helvetica', 'I', 10)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(0, 6, _pt(explanation['description']))
    pdf.ln(4)

    # X-Ray Images
    xray_abs = os.path.join(BASE_DIR, pred['image_path'])
    gradcam_abs = os.path.join(BASE_DIR, pred['gradcam_path']) if pred['gradcam_path'] else None

    if os.path.exists(xray_abs):
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(0, 8, 'X-Ray Images', ln=True)
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)

        img_w = 85
        x_start = 10
        y_img = pdf.get_y()  # anchor Y before placing images
        try:
            pdf.image(xray_abs, x=x_start, y=y_img, w=img_w)
            pdf.set_font('Helvetica', '', 8)
            pdf.set_text_color(100, 100, 100)
            pdf.set_xy(x_start, y_img + img_w + 1)
            pdf.cell(img_w, 5, 'Original X-Ray', align='C', ln=True)
        except Exception:
            pass

        if gradcam_abs and os.path.exists(gradcam_abs):
            try:
                pdf.image(gradcam_abs, x=x_start + img_w + 10, y=y_img, w=img_w)
                pdf.set_font('Helvetica', '', 8)
                pdf.set_text_color(100, 100, 100)
                pdf.set_xy(x_start + img_w + 10, y_img + img_w + 1)
                pdf.cell(img_w, 5, 'Grad-CAM Heatmap', align='C', ln=True)
            except Exception:
                pass

        # Advance past images
        pdf.set_y(y_img + img_w + 10)

    # Confidence scores
    pdf.set_x(10)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(190, 8, 'Class Confidence Scores', ln=True)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    bar_x = 10       # left margin
    label_w = 38
    bar_full_w = 95
    pct_w = 20
    for cls in CLASS_NAMES:
        conf_val = all_conf.get(cls, 0)
        cr, cg, cb = GRADE_HEX_RGB.get(cls, (100, 100, 100))
        row_y = pdf.get_y()
        # Label
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(60, 60, 60)
        pdf.set_xy(bar_x, row_y)
        pdf.cell(label_w, 6, f'  {cls} (G{GRADE_SEVERITY[cls]})', ln=0)
        # Background bar
        bar_x_pos = bar_x + label_w
        bar_w = max(1, int(bar_full_w * conf_val / 100))
        pdf.set_fill_color(220, 220, 220)
        pdf.rect(bar_x_pos, row_y + 1, bar_full_w, 4, 'F')
        pdf.set_fill_color(cr, cg, cb)
        pdf.rect(bar_x_pos, row_y + 1, bar_w, 4, 'F')
        # Percentage text
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_xy(bar_x_pos + bar_full_w + 3, row_y)
        pdf.cell(pct_w, 6, f'{conf_val}%', ln=True)

    pdf.ln(4)

    # Clinical findings
    findings = explanation.get('findings', [])
    if findings:
        pdf.set_x(10)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(190, 8, 'Clinical Findings', ln=True)
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)

        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(60, 60, 60)
        for finding in findings:
            pdf.set_x(10)
            pdf.cell(8, 6, '*', ln=0)
            pdf.multi_cell(182, 6, _pt(finding))

    pdf.ln(4)

    # Disclaimer
    pdf.set_x(10)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(150, 150, 150)
    pdf.multi_cell(190, 5,
        'DISCLAIMER: This report is generated by an AI system for research and educational purposes only. '
        'It should not be used as a substitute for professional medical diagnosis. '
        'Always consult a qualified medical professional for clinical decisions.')

    # Footer line
    pdf.set_draw_color(20, 184, 166)
    pdf.line(10, 285, 200, 285)
    pdf.set_xy(10, 286)
    pdf.set_font('Helvetica', '', 7)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 5, f'Generated by Knee OA Classification System | {datetime.now().strftime("%Y-%m-%d %H:%M")}',
             align='C')

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return buf, None


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

    total_scans = conn.execute(
        'SELECT COUNT(*) FROM predictions WHERE user_id = ?', (user_id,)
    ).fetchone()[0]

    total_patients = conn.execute(
        'SELECT COUNT(*) FROM patients WHERE user_id = ?', (user_id,)
    ).fetchone()[0]

    grade_counts = {}
    for grade in CLASS_NAMES:
        count = conn.execute(
            'SELECT COUNT(*) FROM predictions WHERE user_id = ? AND prediction = ?',
            (user_id, grade)
        ).fetchone()[0]
        grade_counts[grade] = count

    recent = conn.execute(
        'SELECT p.*, pat.name as patient_name FROM predictions p '
        'LEFT JOIN patients pat ON pat.id = p.patient_id '
        'WHERE p.user_id = ? ORDER BY p.id DESC LIMIT 5',
        (user_id,)
    ).fetchall()

    admin_stats = None
    if session.get('role') == 'admin':
        total_users = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        total_all = conn.execute('SELECT COUNT(*) FROM predictions').fetchone()[0]
        admin_stats = {'total_users': total_users, 'total_scans': total_all}

    conn.close()

    samples = []
    if os.path.exists(SAMPLES_FOLDER):
        samples = sorted([f for f in os.listdir(SAMPLES_FOLDER) if f.endswith('.png')])

    # Active models info
    active_models = []
    if mobilenet_model is not None:
        active_models.append('MobileNetV2')
    if cnn_model is not None:
        active_models.append('Custom CNN')
    if rf_model is not None:
        active_models.append('Random Forest')

    return render_template('home.html',
                           total_scans=total_scans,
                           total_patients=total_patients,
                           grade_counts=grade_counts,
                           grade_colors=GRADE_COLORS,
                           recent=recent,
                           admin_stats=admin_stats,
                           samples=samples,
                           active_models=active_models)


@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    result = None
    conn = get_db()
    patients = conn.execute(
        'SELECT id, name FROM patients WHERE user_id = ? ORDER BY name',
        (session['user_id'],)
    ).fetchall()
    conn.close()

    if request.method == 'POST':
        if 'xray_image' not in request.files:
            flash('No file selected.', 'danger')
            return redirect(url_for('predict'))

        file = request.files['xray_image']
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(url_for('predict'))

        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload PNG, JPG, BMP, or TIFF.', 'danger')
            return redirect(url_for('predict'))

        patient_id = request.form.get('patient_id') or None
        if patient_id:
            patient_id = int(patient_id)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = secure_filename(file.filename)
        save_name = f'{session["user_id"]}_{timestamp}_{filename}'
        filepath = os.path.join(UPLOAD_FOLDER, save_name)
        file.save(filepath)

        prediction, confidence, all_conf, models_used = predict_ensemble(filepath)
        scan_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        gradcam_name = f'gradcam_{save_name}'
        gradcam_path = generate_gradcam_overlay(filepath, gradcam_name)

        explanation = GRADE_EXPLANATIONS.get(prediction, {})
        image_path = f'static/uploads/{save_name}'

        conn = get_db()
        cursor = conn.execute(
            'INSERT INTO predictions (user_id, patient_id, image_path, prediction, confidence, '
            'all_confidences, gradcam_path, explanation, models_used, scan_date) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (session['user_id'], patient_id, image_path, prediction, confidence,
             json.dumps(all_conf), gradcam_path, json.dumps(explanation), models_used, scan_date)
        )
        pred_id = cursor.lastrowid
        conn.commit()
        conn.close()

        result = {
            'id': pred_id,
            'prediction': prediction,
            'confidence': confidence,
            'all_confidences': all_conf,
            'image_path': image_path,
            'gradcam_path': gradcam_path,
            'explanation': explanation,
            'scan_date': scan_date,
            'grade_color': GRADE_COLORS.get(prediction, '#3b82f6'),
            'models_used': models_used,
            'patient_id': patient_id,
        }

    return render_template('predict.html', result=result, patients=patients,
                           grade_colors=GRADE_COLORS, class_names=CLASS_NAMES)


@app.route('/history')
@login_required
def history():
    conn = get_db()
    scans = conn.execute(
        'SELECT p.*, pat.name as patient_name FROM predictions p '
        'LEFT JOIN patients pat ON pat.id = p.patient_id '
        'WHERE p.user_id = ? ORDER BY p.id DESC',
        (session['user_id'],)
    ).fetchall()
    conn.close()
    return render_template('history.html', scans=scans, grade_colors=GRADE_COLORS)


@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    user_id = session['user_id']

    grade_counts = {}
    for grade in CLASS_NAMES:
        count = conn.execute(
            'SELECT COUNT(*) FROM predictions WHERE user_id = ? AND prediction = ?',
            (user_id, grade)
        ).fetchone()[0]
        grade_counts[grade] = count

    conn.close()

    return render_template('dashboard.html',
                           models_info=json.dumps(models_info),
                           grade_counts=json.dumps(grade_counts),
                           grade_colors=json.dumps(GRADE_COLORS),
                           class_names=json.dumps(CLASS_NAMES))


# ─── Patients Routes ──────────────────────────────────────────

@app.route('/patients')
@login_required
def patients():
    conn = get_db()
    patient_list = conn.execute(
        '''SELECT pat.*, COUNT(p.id) as scan_count,
           MAX(p.scan_date) as last_scan,
           (SELECT prediction FROM predictions WHERE patient_id = pat.id ORDER BY scan_date DESC LIMIT 1) as latest_grade
           FROM patients pat
           LEFT JOIN predictions p ON p.patient_id = pat.id
           WHERE pat.user_id = ?
           GROUP BY pat.id ORDER BY pat.name''',
        (session['user_id'],)
    ).fetchall()
    conn.close()
    return render_template('patients.html', patients=patient_list, grade_colors=GRADE_COLORS)


@app.route('/patients/new', methods=['GET', 'POST'])
@login_required
def new_patient():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        gender = request.form.get('gender', '').strip()
        notes = request.form.get('notes', '').strip()

        if not name:
            flash('Patient name is required.', 'danger')
            return redirect(url_for('new_patient'))

        age_val = int(age) if age.isdigit() else None
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = get_db()
        conn.execute(
            'INSERT INTO patients (user_id, name, age, gender, notes, created_at) VALUES (?, ?, ?, ?, ?, ?)',
            (session['user_id'], name, age_val, gender or None, notes or None, created_at)
        )
        conn.commit()
        conn.close()
        flash(f'Patient "{name}" created successfully.', 'success')
        return redirect(url_for('patients'))

    return render_template('new_patient.html')


@app.route('/patients/<int:patient_id>')
@login_required
def patient_detail(patient_id):
    conn = get_db()

    patient = conn.execute(
        'SELECT * FROM patients WHERE id = ? AND user_id = ?',
        (patient_id, session['user_id'])
    ).fetchone()

    if not patient:
        conn.close()
        flash('Patient not found.', 'danger')
        return redirect(url_for('patients'))

    scans = conn.execute(
        'SELECT * FROM predictions WHERE patient_id = ? ORDER BY scan_date ASC',
        (patient_id,)
    ).fetchall()
    conn.close()

    # Build progression timeline
    progression = []
    for i, scan in enumerate(scans):
        entry = dict(scan)
        entry['grade_severity'] = GRADE_SEVERITY.get(scan['prediction'], 0)
        if i > 0:
            prev = scans[i - 1]
            prev_sev = GRADE_SEVERITY.get(prev['prediction'], 0)
            curr_sev = entry['grade_severity']
            if curr_sev < prev_sev:
                entry['trend'] = 'improvement'
                entry['trend_text'] = f'Improved from {prev["prediction"]} to {scan["prediction"]}'
            elif curr_sev > prev_sev:
                entry['trend'] = 'worsening'
                entry['trend_text'] = f'Worsened from {prev["prediction"]} to {scan["prediction"]}'
            else:
                entry['trend'] = 'stable'
                entry['trend_text'] = f'Stable — {scan["prediction"]}'
        else:
            entry['trend'] = 'initial'
            entry['trend_text'] = 'Initial scan'
        progression.append(entry)

    return render_template('patient_detail.html',
                           patient=patient,
                           progression=progression,
                           grade_colors=GRADE_COLORS,
                           class_names=CLASS_NAMES)


@app.route('/patients/<int:patient_id>/delete', methods=['POST'])
@login_required
def delete_patient(patient_id):
    conn = get_db()
    patient = conn.execute(
        'SELECT id FROM patients WHERE id = ? AND user_id = ?',
        (patient_id, session['user_id'])
    ).fetchone()
    if patient:
        conn.execute('UPDATE predictions SET patient_id = NULL WHERE patient_id = ?', (patient_id,))
        conn.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
        conn.commit()
        flash('Patient record deleted.', 'info')
    conn.close()
    return redirect(url_for('patients'))


# ─── PDF Download ─────────────────────────────────────────────

@app.route('/download_report/<int:pred_id>')
@login_required
def download_report(pred_id):
    buf, error = generate_report_pdf(pred_id, session['user_id'])
    if error:
        flash(f'Could not generate PDF: {error}', 'danger')
        return redirect(url_for('history'))
    return send_file(
        buf,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'knee_oa_report_{pred_id}.pdf'
    )


# ─── Misc Routes ──────────────────────────────────────────────

@app.route('/about')
@login_required
def about():
    return render_template('about.html')


@app.route('/download_sample/<filename>')
@login_required
def download_sample(filename):
    return send_from_directory(SAMPLES_FOLDER, filename, as_attachment=True)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5011)
