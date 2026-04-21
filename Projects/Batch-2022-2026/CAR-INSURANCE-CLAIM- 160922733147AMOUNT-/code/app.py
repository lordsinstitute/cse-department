"""
Car Insurance Claim Prediction - Flask Web Application
Predicts whether a customer will file an insurance claim based on profile data.
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import pickle
import numpy as np
import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'car_insurance_claim_2025'
DB_PATH = 'insurance.db'

# ---- Load Model and Encoders ----

model = None
encoders = {}
models_info = {}
feature_order = []

# Categorical feature options (for dropdowns)
CATEGORICAL_OPTIONS = {
    'AGE': ['16-25', '26-39', '40-64', '65+'],
    'GENDER': ['male', 'female'],
    'RACE': ['majority', 'minority'],
    'DRIVING_EXPERIENCE': ['0-9y', '10-19y', '20-29y', '30y+'],
    'EDUCATION': ['none', 'high school', 'university'],
    'INCOME': ['poverty', 'working class', 'middle class', 'upper class'],
    'VEHICLE_YEAR': ['before 2015', 'after 2015'],
    'VEHICLE_TYPE': ['sedan', 'sports car'],
}


def load_model():
    global model, encoders, models_info, feature_order

    if os.path.exists('claim_model.pkl'):
        with open('claim_model.pkl', 'rb') as f:
            model = pickle.load(f)
        print('Model loaded successfully.')

    if os.path.exists('encoders.pkl'):
        with open('encoders.pkl', 'rb') as f:
            encoders = pickle.load(f)

    if os.path.exists('models_info.json'):
        with open('models_info.json', 'r') as f:
            models_info = json.load(f)
        feature_order = models_info.get('features', [])


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
        input_data TEXT NOT NULL,
        prediction TEXT NOT NULL,
        confidence REAL NOT NULL,
        pred_date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)",
                  ('admin', generate_password_hash('admin123'), 'Administrator', 'admin'))

    conn.commit()
    conn.close()


init_db()


# ---- Prediction Helper ----

def predict_claim(form_data):
    """Run prediction based on form input."""
    if model is None:
        return 'Error', 0.0, {}

    input_values = []
    display_data = {}

    for feat in feature_order:
        val = form_data.get(feat, '0')
        display_data[feat] = val

        if feat in encoders:
            # Categorical: encode using saved LabelEncoder
            try:
                encoded = encoders[feat].transform([val])[0]
            except ValueError:
                encoded = 0
            input_values.append(encoded)
        else:
            # Numeric
            try:
                input_values.append(float(val))
            except ValueError:
                input_values.append(0.0)

    arr = np.array([input_values])

    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(arr)[0]
        pred_class = int(np.argmax(proba))
        confidence = round(proba[pred_class] * 100, 2)
    else:
        pred_class = int(model.predict(arr)[0])
        confidence = 85.0  # default for models without probability

    prediction = 'Claim Likely' if pred_class == 1 else 'No Claim Expected'
    return prediction, confidence, display_data


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
    total = conn.execute("SELECT COUNT(*) FROM predictions WHERE user_id=?",
                         (session['user_id'],)).fetchone()[0]
    claims = conn.execute(
        "SELECT COUNT(*) FROM predictions WHERE user_id=? AND prediction LIKE '%Claim Likely%'",
        (session['user_id'],)).fetchone()[0]
    no_claims = total - claims
    recent = conn.execute("SELECT * FROM predictions WHERE user_id=? ORDER BY id DESC LIMIT 5",
                          (session['user_id'],)).fetchall()

    admin_stats = {}
    if session.get('role') == 'admin':
        admin_stats['total_users'] = conn.execute("SELECT COUNT(*) FROM users WHERE role='user'").fetchone()[0]
        admin_stats['total_predictions'] = conn.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
        admin_stats['total_claims'] = conn.execute(
            "SELECT COUNT(*) FROM predictions WHERE prediction LIKE '%Claim Likely%'").fetchone()[0]

    conn.close()

    return render_template('home.html',
                           total=total, claims=claims, no_claims=no_claims,
                           recent=recent, admin_stats=admin_stats)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    result = None

    if request.method == 'POST':
        prediction, confidence, display_data = predict_claim(request.form)

        if prediction != 'Error':
            conn = get_db()
            conn.execute(
                "INSERT INTO predictions (user_id, input_data, prediction, confidence, pred_date) VALUES (?, ?, ?, ?, ?)",
                (session['user_id'], json.dumps(display_data), prediction, confidence,
                 datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            )
            conn.commit()
            conn.close()

            result = {
                'prediction': prediction,
                'confidence': confidence,
                'is_claim': 'Claim Likely' in prediction,
                'input': display_data
            }
        else:
            flash('Model not loaded. Run train_model.py first.', 'danger')

    return render_template('predict.html',
                           categorical_options=CATEGORICAL_OPTIONS,
                           feature_order=feature_order,
                           result=result)


@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    predictions = conn.execute("SELECT * FROM predictions WHERE user_id=? ORDER BY id DESC",
                               (session['user_id'],)).fetchall()
    conn.close()
    return render_template('history.html', predictions=predictions, json=json)


@app.route('/visualize')
def visualize():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    vis_files = []
    vis_dir = 'static/vis'
    if os.path.exists(vis_dir):
        vis_files = sorted([f for f in os.listdir(vis_dir) if f.endswith('.png')])

    return render_template('visualize.html', vis_files=vis_files)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    user_preds = conn.execute("SELECT * FROM predictions WHERE user_id=?",
                              (session['user_id'],)).fetchall()

    pred_counts = {'Claim Likely': 0, 'No Claim Expected': 0}
    for p in user_preds:
        if 'Claim Likely' in p['prediction']:
            pred_counts['Claim Likely'] += 1
        else:
            pred_counts['No Claim Expected'] += 1

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
                           total=len(user_preds))


@app.route('/about')
def about():
    return render_template('about.html', models_info=models_info)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
