"""
Carbon Emission Prediction — Flask Web Application
Enter vehicle specifications to predict CO2 emissions (g/km) using ML regression.

v2 Improvements:
  - Vehicle weight and model year as input features
  - Hybrid/Electric vehicle support
  - Prediction confidence intervals (from model tree variance)
  - Smart input validation (impossible combinations blocked)
  - Carbon footprint calculator (annual emissions)
  - REST API endpoint (/api/predict)
  - Eco-friendly recommendations

v3 — Multiple prediction modes:
  - Quick Presets: One-click prediction for popular real-world vehicles
  - Vehicle Comparison: Side-by-side compare up to 3 vehicles
  - Batch Prediction: Upload CSV, get predictions for all rows
  - Interactive Sliders: Real-time prediction as you adjust sliders
"""

import os
import io
import csv
import json
import sqlite3
from datetime import datetime
from functools import wraps

import numpy as np
import pandas as pd
import joblib
from flask import (Flask, render_template, request, redirect, url_for,
                   session, flash, jsonify, Response)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'carbon-emission-prediction-secret-2025'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'carbon_emissions.db')
MODEL_PATH = os.path.join(BASE_DIR, 'best_model.pkl')
ENCODERS_PATH = os.path.join(BASE_DIR, 'encoders.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'scaler.pkl')
MODELS_INFO_PATH = os.path.join(BASE_DIR, 'models_info.json')

# Feature definitions
CATEGORICAL_COLS = ['Make', 'Vehicle_Class', 'Transmission', 'Fuel_Type']
NUMERIC_COLS = ['Engine_Size', 'Cylinders', 'Vehicle_Weight', 'Model_Year',
                'Fuel_Consumption_City', 'Fuel_Consumption_Hwy', 'Fuel_Consumption_Comb']

CATEGORICAL_OPTIONS = {
    'Make': ['Toyota', 'Honda', 'Ford', 'BMW', 'Hyundai',
             'Chevrolet', 'Nissan', 'Mercedes-Benz', 'Kia', 'Volkswagen'],
    'Vehicle_Class': ['Compact', 'Mid-size', 'SUV', 'Full-size', 'Pickup',
                      'Subcompact', 'Minicompact', 'Station wagon'],
    'Transmission': ['Automatic', 'Manual', 'CVT'],
    'Fuel_Type': ['Regular Gasoline', 'Premium Gasoline', 'Diesel',
                  'Ethanol (E85)', 'Hybrid', 'Electric'],
}

NUMERIC_RANGES = {
    'Engine_Size': {'min': 0.0, 'max': 6.5, 'step': 0.1, 'default': 2.0, 'unit': 'L'},
    'Cylinders': {'min': 0, 'max': 12, 'step': 1, 'default': 4, 'unit': ''},
    'Vehicle_Weight': {'min': 800, 'max': 3000, 'step': 10, 'default': 1400, 'unit': 'kg'},
    'Model_Year': {'min': 2015, 'max': 2025, 'step': 1, 'default': 2023, 'unit': ''},
    'Fuel_Consumption_City': {'min': 0.0, 'max': 22.0, 'step': 0.1, 'default': 9.0, 'unit': 'L/100km'},
    'Fuel_Consumption_Hwy': {'min': 0.0, 'max': 16.0, 'step': 0.1, 'default': 7.0, 'unit': 'L/100km'},
    'Fuel_Consumption_Comb': {'min': 0.0, 'max': 20.0, 'step': 0.1, 'default': 8.0, 'unit': 'L/100km'},
}

# Valid class → engine/cylinder/weight ranges for input validation
CLASS_CONSTRAINTS = {
    'Subcompact':    {'engine': (1.0, 1.8), 'cyl': (3, 4),  'weight': (800, 1300)},
    'Minicompact':   {'engine': (1.0, 2.0), 'cyl': (3, 4),  'weight': (800, 1250)},
    'Compact':       {'engine': (1.4, 2.5), 'cyl': (3, 4),  'weight': (1000, 1550)},
    'Mid-size':      {'engine': (1.8, 3.5), 'cyl': (4, 6),  'weight': (1200, 1800)},
    'Full-size':     {'engine': (2.5, 5.0), 'cyl': (6, 8),  'weight': (1500, 2200)},
    'SUV':           {'engine': (2.0, 5.5), 'cyl': (4, 8),  'weight': (1400, 2800)},
    'Pickup':        {'engine': (3.0, 6.5), 'cyl': (6, 8),  'weight': (1700, 3000)},
    'Station wagon': {'engine': (1.6, 3.0), 'cyl': (4, 6),  'weight': (1100, 1700)},
}

# Load ML model and preprocessors
model = None
encoders = None
scaler = None
models_info = None


def load_model():
    """Load the trained model, encoders, and scaler."""
    global model, encoders, scaler, models_info

    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print(f'Model loaded from {MODEL_PATH}')
    else:
        print(f'WARNING: Model not found at {MODEL_PATH}')

    if os.path.exists(ENCODERS_PATH):
        encoders = joblib.load(ENCODERS_PATH)
        print(f'Encoders loaded from {ENCODERS_PATH}')

    if os.path.exists(SCALER_PATH):
        scaler = joblib.load(SCALER_PATH)
        print(f'Scaler loaded from {SCALER_PATH}')

    if os.path.exists(MODELS_INFO_PATH):
        with open(MODELS_INFO_PATH) as f:
            models_info = json.load(f)
        print(f'Models info loaded from {MODELS_INFO_PATH}')


def get_co2_rating(co2_value):
    """Convert CO2 g/km to a 1-10 rating."""
    if co2_value <= 0:
        return 10
    elif co2_value < 120:
        return 10
    elif co2_value < 140:
        return 9
    elif co2_value < 160:
        return 8
    elif co2_value < 180:
        return 7
    elif co2_value < 210:
        return 6
    elif co2_value < 250:
        return 5
    elif co2_value < 300:
        return 4
    elif co2_value < 350:
        return 3
    elif co2_value < 400:
        return 2
    else:
        return 1


def get_co2_label(rating):
    """Get environmental impact label from rating."""
    if rating >= 8:
        return 'Excellent'
    elif rating >= 6:
        return 'Good'
    elif rating >= 4:
        return 'Moderate'
    elif rating >= 2:
        return 'High'
    else:
        return 'Very High'


def get_co2_color(rating):
    """Get color for CO2 rating display."""
    if rating >= 8:
        return '#22c55e'   # green
    elif rating >= 6:
        return '#84cc16'   # lime
    elif rating >= 4:
        return '#eab308'   # yellow
    elif rating >= 2:
        return '#f97316'   # orange
    else:
        return '#ef4444'   # red


def validate_inputs(form_data):
    """Validate input combinations. Returns list of warning messages."""
    warnings = []
    fuel_type = form_data.get('Fuel_Type', '')
    vclass = form_data.get('Vehicle_Class', '')

    try:
        engine = float(form_data.get('Engine_Size', 0))
        cyls = int(form_data.get('Cylinders', 0))
        weight = int(form_data.get('Vehicle_Weight', 0))
        fuel_city = float(form_data.get('Fuel_Consumption_City', 0))
    except (ValueError, TypeError):
        return warnings

    # Electric vehicle checks
    if fuel_type == 'Electric':
        if engine > 0:
            warnings.append('Electric vehicles have no combustion engine (Engine Size should be 0).')
        if cyls > 0:
            warnings.append('Electric vehicles have no cylinders (should be 0).')
        if fuel_city > 0:
            warnings.append('Electric vehicles have zero fuel consumption.')
    # Class-specific validation
    elif vclass in CLASS_CONSTRAINTS:
        c = CLASS_CONSTRAINTS[vclass]
        if fuel_type != 'Hybrid' and engine > 0:
            if engine < c['engine'][0] or engine > c['engine'][1]:
                warnings.append(f'{vclass} vehicles typically have {c["engine"][0]}-{c["engine"][1]}L engines.')
            if cyls < c['cyl'][0] or cyls > c['cyl'][1]:
                warnings.append(f'{vclass} vehicles typically have {c["cyl"][0]}-{c["cyl"][1]} cylinders.')
        if weight < c['weight'][0] or weight > c['weight'][1]:
            warnings.append(f'{vclass} vehicles typically weigh {c["weight"][0]}-{c["weight"][1]} kg.')

    return warnings


def predict_co2(form_data):
    """Predict CO2 emissions from form data. Returns (prediction, confidence_low, confidence_high)."""
    fuel_type = form_data.get('Fuel_Type', '')

    # Electric vehicles: always 0 CO2
    if fuel_type == 'Electric':
        return 0.0, 0.0, 0.0

    # Build feature vector
    feature_values = {}

    # Categorical features
    for col in CATEGORICAL_COLS:
        raw_value = form_data.get(col, '')
        if col in encoders and raw_value in list(encoders[col].classes_):
            feature_values[col] = encoders[col].transform([raw_value])[0]
        else:
            feature_values[col] = 0

    # Numeric features
    for col in NUMERIC_COLS:
        try:
            feature_values[col] = float(form_data.get(col, 0))
        except (ValueError, TypeError):
            feature_values[col] = NUMERIC_RANGES[col]['default']

    # Create DataFrame with correct column order
    feature_cols = CATEGORICAL_COLS + NUMERIC_COLS
    df = pd.DataFrame([feature_values], columns=feature_cols)

    # Scale numeric features
    if scaler:
        df[NUMERIC_COLS] = scaler.transform(df[NUMERIC_COLS])

    # Main prediction
    prediction = model.predict(df)[0]
    predicted_co2 = round(float(prediction), 1)
    predicted_co2 = max(0, min(520, predicted_co2))

    # Confidence interval from individual trees
    conf_low, conf_high = predicted_co2, predicted_co2
    if hasattr(model, 'estimators_'):
        # Random Forest: each tree gives independent prediction
        tree_preds = np.array([tree.predict(df)[0] for tree in model.estimators_])
        conf_low = round(max(0, float(np.percentile(tree_preds, 5))), 1)
        conf_high = round(min(520, float(np.percentile(tree_preds, 95))), 1)
    elif hasattr(model, 'get_booster'):
        # XGBoost: use partial predictions from subsets of trees
        import xgboost as xgb
        booster = model.get_booster()
        n_trees = int(booster.num_boosted_rounds())
        if n_trees > 10:
            partial_preds = []
            for frac in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
                n = max(1, int(n_trees * frac))
                p = model.predict(df, iteration_range=(0, n))[0]
                partial_preds.append(float(p))
            spread = max(partial_preds) - min(partial_preds)
            conf_low = round(max(0, predicted_co2 - spread * 1.5), 1)
            conf_high = round(min(520, predicted_co2 + spread * 1.5), 1)

    return predicted_co2, conf_low, conf_high


def get_recommendations(co2_value, fuel_type, engine_size):
    """Generate eco-friendly recommendations based on prediction."""
    recs = []
    if fuel_type in ('Regular Gasoline', 'Premium Gasoline') and co2_value > 200:
        recs.append('Consider switching to a Hybrid variant to reduce emissions by ~40%.')
    if fuel_type != 'Electric' and co2_value > 250:
        recs.append('An Electric vehicle in this class would produce zero tailpipe emissions.')
    if engine_size > 3.0 and co2_value > 200:
        recs.append('A smaller engine (2.0-2.5L) could significantly reduce emissions.')
    if fuel_type == 'Diesel' and co2_value > 180:
        recs.append('Diesel emits more CO2 per litre. Consider gasoline or hybrid alternatives.')
    if co2_value > 300:
        recs.append('This vehicle has high emissions. Regular maintenance and proper tire pressure can improve efficiency by 5-10%.')
    if co2_value <= 120:
        recs.append('Excellent! This is among the cleanest vehicles on the road.')
    if fuel_type == 'Electric':
        recs.append('Zero tailpipe emissions! Consider renewable energy charging for maximum environmental benefit.')
    if fuel_type == 'Hybrid' and co2_value < 150:
        recs.append('Great choice! Hybrid technology provides significant emission reductions.')
    return recs


def calculate_carbon_footprint(co2_gkm, annual_km):
    """Calculate annual carbon footprint."""
    annual_co2_kg = co2_gkm * annual_km / 1000.0
    annual_co2_tonnes = annual_co2_kg / 1000.0
    trees_to_offset = annual_co2_kg / 22.0  # 1 tree absorbs ~22 kg CO2/year
    return {
        'annual_kg': round(annual_co2_kg, 1),
        'annual_tonnes': round(annual_co2_tonnes, 2),
        'trees_needed': int(np.ceil(trees_to_offset)),
        'monthly_kg': round(annual_co2_kg / 12, 1),
    }


# --- Database ---

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        );
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            input_data TEXT NOT NULL,
            predicted_co2 REAL NOT NULL,
            co2_rating INTEGER NOT NULL,
            confidence_low REAL DEFAULT 0,
            confidence_high REAL DEFAULT 0,
            pred_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')

    # Add new columns if upgrading from v1
    try:
        conn.execute('ALTER TABLE predictions ADD COLUMN confidence_low REAL DEFAULT 0')
    except Exception:
        pass
    try:
        conn.execute('ALTER TABLE predictions ADD COLUMN confidence_high REAL DEFAULT 0')
    except Exception:
        pass

    # Seed admin
    existing = conn.execute('SELECT id FROM users WHERE username = ?', ('admin',)).fetchone()
    if not existing:
        conn.execute(
            'INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)',
            ('admin', generate_password_hash('admin123'), 'Administrator', 'admin')
        )
        conn.commit()

    conn.close()


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# --- Routes ---

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        name = request.form.get('name', '').strip()

        if not username or not password or not name:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))

        conn = get_db()
        existing = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        if existing:
            conn.close()
            flash('Username already taken.', 'danger')
            return redirect(url_for('register'))

        conn.execute(
            'INSERT INTO users (username, password, name) VALUES (?, ?, ?)',
            (username, generate_password_hash(password), name)
        )
        conn.commit()
        conn.close()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('login.html', register=True)


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

    return render_template('login.html', register=False)


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    conn = get_db()

    total_preds = conn.execute('SELECT COUNT(*) FROM predictions').fetchone()[0]
    avg_co2 = conn.execute('SELECT AVG(predicted_co2) FROM predictions').fetchone()[0]
    avg_rating = conn.execute('SELECT AVG(co2_rating) FROM predictions').fetchone()[0]

    recent = conn.execute(
        'SELECT p.*, u.username FROM predictions p JOIN users u ON p.user_id = u.id '
        'ORDER BY p.pred_date DESC LIMIT 5'
    ).fetchall()
    conn.close()

    return render_template('home.html',
                           total_preds=total_preds,
                           avg_co2=round(avg_co2, 1) if avg_co2 else 0,
                           avg_rating=round(avg_rating, 1) if avg_rating else 0,
                           recent=recent,
                           get_co2_color=get_co2_color,
                           get_co2_label=get_co2_label,
                           json=json)


@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    result = None

    if request.method == 'POST' and model:
        # Validate inputs
        input_warnings = validate_inputs(request.form)

        predicted_co2, conf_low, conf_high = predict_co2(request.form)
        rating = get_co2_rating(predicted_co2)
        label = get_co2_label(rating)
        color = get_co2_color(rating)

        # Collect input data for display and storage
        input_display = {}
        for col in CATEGORICAL_COLS:
            input_display[col] = request.form.get(col, '')
        for col in NUMERIC_COLS:
            input_display[col] = request.form.get(col, '')

        # Get recommendations
        engine_size = float(input_display.get('Engine_Size', 0))
        recs = get_recommendations(predicted_co2, input_display.get('Fuel_Type', ''), engine_size)

        # Carbon footprint (default 15,000 km/year)
        footprint = calculate_carbon_footprint(predicted_co2, 15000)

        # Save to database
        conn = get_db()
        conn.execute(
            'INSERT INTO predictions (user_id, input_data, predicted_co2, co2_rating, confidence_low, confidence_high, pred_date) '
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (session['user_id'], json.dumps(input_display), predicted_co2, rating,
             conf_low, conf_high,
             datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        conn.commit()
        conn.close()

        result = {
            'co2': predicted_co2,
            'conf_low': conf_low,
            'conf_high': conf_high,
            'rating': rating,
            'label': label,
            'color': color,
            'input': input_display,
            'warnings': input_warnings,
            'recommendations': recs,
            'footprint': footprint,
        }

    return render_template('predict.html',
                           result=result,
                           categorical_options=CATEGORICAL_OPTIONS,
                           numeric_ranges=NUMERIC_RANGES,
                           class_constraints=json.dumps(CLASS_CONSTRAINTS),
                           now=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                           models_info_name=models_info['best_model'] if models_info else 'N/A')


@app.route('/history')
@login_required
def history():
    conn = get_db()
    preds = conn.execute(
        'SELECT p.*, u.username FROM predictions p JOIN users u ON p.user_id = u.id '
        'ORDER BY p.pred_date DESC'
    ).fetchall()
    conn.close()
    return render_template('history.html', predictions=preds,
                           get_co2_color=get_co2_color,
                           get_co2_label=get_co2_label,
                           json=json)


@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()

    total_preds = conn.execute('SELECT COUNT(*) FROM predictions').fetchone()[0]
    avg_co2 = conn.execute('SELECT AVG(predicted_co2) FROM predictions').fetchone()[0]

    # Rating distribution
    rating_dist = {}
    for row in conn.execute('SELECT co2_rating, COUNT(*) as cnt FROM predictions GROUP BY co2_rating'):
        rating_dist[row['co2_rating']] = row['cnt']

    conn.close()

    return render_template('dashboard.html',
                           models_info=models_info,
                           total_preds=total_preds,
                           avg_co2=round(avg_co2, 1) if avg_co2 else 0,
                           rating_dist=json.dumps(rating_dist))


@app.route('/calculator', methods=['GET', 'POST'])
@login_required
def calculator():
    result = None
    if request.method == 'POST':
        try:
            co2_gkm = float(request.form.get('co2_gkm', 0))
            annual_km = float(request.form.get('annual_km', 15000))
            result = calculate_carbon_footprint(co2_gkm, annual_km)
            result['co2_gkm'] = co2_gkm
            result['annual_km'] = annual_km
        except (ValueError, TypeError):
            flash('Please enter valid numbers.', 'danger')
    return render_template('calculator.html', result=result)


@app.route('/about')
@login_required
def about():
    return render_template('about.html', models_info=models_info)


# --- Quick Presets ---

VEHICLE_PRESETS = {
    'Toyota Camry 2024': {
        'Make': 'Toyota', 'Vehicle_Class': 'Mid-size', 'Transmission': 'Automatic',
        'Fuel_Type': 'Regular Gasoline', 'Engine_Size': 2.5, 'Cylinders': 4,
        'Vehicle_Weight': 1590, 'Model_Year': 2024,
        'Fuel_Consumption_City': 8.7, 'Fuel_Consumption_Hwy': 6.3, 'Fuel_Consumption_Comb': 7.6,
    },
    'Toyota Camry Hybrid 2024': {
        'Make': 'Toyota', 'Vehicle_Class': 'Mid-size', 'Transmission': 'CVT',
        'Fuel_Type': 'Hybrid', 'Engine_Size': 2.5, 'Cylinders': 4,
        'Vehicle_Weight': 1620, 'Model_Year': 2024,
        'Fuel_Consumption_City': 5.0, 'Fuel_Consumption_Hwy': 4.6, 'Fuel_Consumption_Comb': 4.8,
    },
    'Honda Civic 2024': {
        'Make': 'Honda', 'Vehicle_Class': 'Compact', 'Transmission': 'CVT',
        'Fuel_Type': 'Regular Gasoline', 'Engine_Size': 2.0, 'Cylinders': 4,
        'Vehicle_Weight': 1390, 'Model_Year': 2024,
        'Fuel_Consumption_City': 7.8, 'Fuel_Consumption_Hwy': 5.9, 'Fuel_Consumption_Comb': 6.9,
    },
    'Ford F-150 2024': {
        'Make': 'Ford', 'Vehicle_Class': 'Pickup', 'Transmission': 'Automatic',
        'Fuel_Type': 'Regular Gasoline', 'Engine_Size': 5.0, 'Cylinders': 8,
        'Vehicle_Weight': 2450, 'Model_Year': 2024,
        'Fuel_Consumption_City': 15.7, 'Fuel_Consumption_Hwy': 11.8, 'Fuel_Consumption_Comb': 13.9,
    },
    'BMW 3 Series 2024': {
        'Make': 'BMW', 'Vehicle_Class': 'Mid-size', 'Transmission': 'Automatic',
        'Fuel_Type': 'Premium Gasoline', 'Engine_Size': 2.0, 'Cylinders': 4,
        'Vehicle_Weight': 1640, 'Model_Year': 2024,
        'Fuel_Consumption_City': 8.4, 'Fuel_Consumption_Hwy': 6.0, 'Fuel_Consumption_Comb': 7.3,
    },
    'Tesla Model 3 (Electric)': {
        'Make': 'Toyota', 'Vehicle_Class': 'Mid-size', 'Transmission': 'Automatic',
        'Fuel_Type': 'Electric', 'Engine_Size': 0, 'Cylinders': 0,
        'Vehicle_Weight': 1760, 'Model_Year': 2024,
        'Fuel_Consumption_City': 0, 'Fuel_Consumption_Hwy': 0, 'Fuel_Consumption_Comb': 0,
    },
    'Hyundai Tucson 2024': {
        'Make': 'Hyundai', 'Vehicle_Class': 'SUV', 'Transmission': 'Automatic',
        'Fuel_Type': 'Regular Gasoline', 'Engine_Size': 2.5, 'Cylinders': 4,
        'Vehicle_Weight': 1680, 'Model_Year': 2024,
        'Fuel_Consumption_City': 9.8, 'Fuel_Consumption_Hwy': 7.4, 'Fuel_Consumption_Comb': 8.7,
    },
    'Mercedes-Benz C-Class 2023': {
        'Make': 'Mercedes-Benz', 'Vehicle_Class': 'Mid-size', 'Transmission': 'Automatic',
        'Fuel_Type': 'Premium Gasoline', 'Engine_Size': 2.0, 'Cylinders': 4,
        'Vehicle_Weight': 1710, 'Model_Year': 2023,
        'Fuel_Consumption_City': 9.0, 'Fuel_Consumption_Hwy': 6.5, 'Fuel_Consumption_Comb': 7.9,
    },
    'Kia Sportage Diesel 2023': {
        'Make': 'Kia', 'Vehicle_Class': 'SUV', 'Transmission': 'Automatic',
        'Fuel_Type': 'Diesel', 'Engine_Size': 2.0, 'Cylinders': 4,
        'Vehicle_Weight': 1650, 'Model_Year': 2023,
        'Fuel_Consumption_City': 7.6, 'Fuel_Consumption_Hwy': 5.8, 'Fuel_Consumption_Comb': 6.8,
    },
    'Chevrolet Silverado 2024': {
        'Make': 'Chevrolet', 'Vehicle_Class': 'Pickup', 'Transmission': 'Automatic',
        'Fuel_Type': 'Regular Gasoline', 'Engine_Size': 6.2, 'Cylinders': 8,
        'Vehicle_Weight': 2600, 'Model_Year': 2024,
        'Fuel_Consumption_City': 18.1, 'Fuel_Consumption_Hwy': 13.1, 'Fuel_Consumption_Comb': 15.9,
    },
    'Volkswagen Golf 2023': {
        'Make': 'Volkswagen', 'Vehicle_Class': 'Compact', 'Transmission': 'Automatic',
        'Fuel_Type': 'Regular Gasoline', 'Engine_Size': 1.5, 'Cylinders': 4,
        'Vehicle_Weight': 1350, 'Model_Year': 2023,
        'Fuel_Consumption_City': 7.4, 'Fuel_Consumption_Hwy': 5.6, 'Fuel_Consumption_Comb': 6.6,
    },
    'Nissan Leaf (Electric)': {
        'Make': 'Nissan', 'Vehicle_Class': 'Compact', 'Transmission': 'Automatic',
        'Fuel_Type': 'Electric', 'Engine_Size': 0, 'Cylinders': 0,
        'Vehicle_Weight': 1600, 'Model_Year': 2024,
        'Fuel_Consumption_City': 0, 'Fuel_Consumption_Hwy': 0, 'Fuel_Consumption_Comb': 0,
    },
}


@app.route('/presets')
@login_required
def presets():
    results = []
    for name, specs in VEHICLE_PRESETS.items():
        predicted_co2, conf_low, conf_high = predict_co2(specs)
        rating = get_co2_rating(predicted_co2)
        label = get_co2_label(rating)
        color = get_co2_color(rating)
        footprint = calculate_carbon_footprint(predicted_co2, 15000)
        results.append({
            'name': name,
            'specs': specs,
            'co2': predicted_co2,
            'conf_low': conf_low,
            'conf_high': conf_high,
            'rating': rating,
            'label': label,
            'color': color,
            'footprint': footprint,
        })
    return render_template('presets.html', presets=results)


# --- Vehicle Comparison ---

@app.route('/compare', methods=['GET', 'POST'])
@login_required
def compare():
    results = []
    preset_names = list(VEHICLE_PRESETS.keys())

    if request.method == 'POST' and model:
        # Up to 3 vehicles to compare
        for i in range(1, 4):
            prefix = f'v{i}_'
            make = request.form.get(f'{prefix}Make', '')
            if not make:
                continue  # Skip empty vehicles
            form_data = {}
            for col in CATEGORICAL_COLS:
                form_data[col] = request.form.get(f'{prefix}{col}', '')
            for col in NUMERIC_COLS:
                form_data[col] = request.form.get(f'{prefix}{col}', '0')

            predicted_co2, conf_low, conf_high = predict_co2(form_data)
            rating = get_co2_rating(predicted_co2)
            label = get_co2_label(rating)
            color = get_co2_color(rating)
            footprint = calculate_carbon_footprint(predicted_co2, 15000)
            warnings = validate_inputs(form_data)
            recs = get_recommendations(predicted_co2, form_data.get('Fuel_Type', ''), float(form_data.get('Engine_Size', 0)))

            results.append({
                'vehicle_num': i,
                'specs': form_data,
                'co2': predicted_co2,
                'conf_low': conf_low,
                'conf_high': conf_high,
                'rating': rating,
                'label': label,
                'color': color,
                'footprint': footprint,
                'warnings': warnings,
                'recommendations': recs,
            })

    return render_template('compare.html',
                           results=results,
                           categorical_options=CATEGORICAL_OPTIONS,
                           numeric_ranges=NUMERIC_RANGES,
                           preset_names=preset_names,
                           presets_json=json.dumps(VEHICLE_PRESETS))


# --- Batch Prediction ---

@app.route('/batch', methods=['GET', 'POST'])
@login_required
def batch():
    results = None
    errors = []

    if request.method == 'POST' and model:
        file = request.files.get('csv_file')
        if not file or not file.filename.endswith('.csv'):
            flash('Please upload a valid CSV file.', 'danger')
            return render_template('batch.html', results=None, errors=[],
                                   categorical_options=CATEGORICAL_OPTIONS,
                                   numeric_ranges=NUMERIC_RANGES)

        try:
            content = file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(content))
            results = []
            required = CATEGORICAL_COLS + NUMERIC_COLS

            for row_num, row in enumerate(reader, start=2):
                missing = [f for f in required if f not in row or not row[f].strip()]
                if missing:
                    errors.append(f'Row {row_num}: Missing fields — {", ".join(missing)}')
                    continue

                predicted_co2, conf_low, conf_high = predict_co2(row)
                rating = get_co2_rating(predicted_co2)
                label = get_co2_label(rating)
                color = get_co2_color(rating)
                warnings = validate_inputs(row)

                results.append({
                    'row': row_num,
                    'make': row.get('Make', ''),
                    'vehicle_class': row.get('Vehicle_Class', ''),
                    'fuel_type': row.get('Fuel_Type', ''),
                    'engine': row.get('Engine_Size', ''),
                    'co2': predicted_co2,
                    'conf_low': conf_low,
                    'conf_high': conf_high,
                    'rating': rating,
                    'label': label,
                    'color': color,
                    'warnings': warnings,
                })

        except Exception as e:
            flash(f'Error processing CSV: {str(e)}', 'danger')

    return render_template('batch.html', results=results, errors=errors,
                           categorical_options=CATEGORICAL_OPTIONS,
                           numeric_ranges=NUMERIC_RANGES)


@app.route('/batch/download', methods=['POST'])
@login_required
def batch_download():
    """Download batch results as CSV."""
    results_json = request.form.get('results_data', '[]')
    try:
        results = json.loads(results_json)
    except json.JSONDecodeError:
        flash('No results to download.', 'danger')
        return redirect(url_for('batch'))

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Row', 'Make', 'Vehicle Class', 'Fuel Type', 'Engine Size',
                      'CO2 (g/km)', 'CI Low', 'CI High', 'Rating', 'Label', 'Warnings'])
    for r in results:
        writer.writerow([r.get('row', ''), r.get('make', ''), r.get('vehicle_class', ''),
                          r.get('fuel_type', ''), r.get('engine', ''),
                          r.get('co2', ''), r.get('conf_low', ''), r.get('conf_high', ''),
                          r.get('rating', ''), r.get('label', ''),
                          '; '.join(r.get('warnings', []))])

    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=batch_predictions.csv'}
    )


@app.route('/batch/template')
@login_required
def batch_template():
    """Download a sample CSV template for batch prediction."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(CATEGORICAL_COLS + NUMERIC_COLS)
    writer.writerow(['Toyota', 'Compact', 'CVT', 'Regular Gasoline', 2.0, 4, 1350, 2024, 8.0, 6.0, 7.1])
    writer.writerow(['Honda', 'SUV', 'Automatic', 'Hybrid', 2.0, 4, 1650, 2024, 5.5, 4.8, 5.2])
    writer.writerow(['Ford', 'Pickup', 'Automatic', 'Regular Gasoline', 5.0, 8, 2450, 2024, 15.7, 11.8, 13.9])

    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=batch_template.csv'}
    )


# --- Interactive Sliders ---

@app.route('/interactive')
@login_required
def interactive():
    return render_template('interactive.html',
                           categorical_options=CATEGORICAL_OPTIONS,
                           numeric_ranges=NUMERIC_RANGES,
                           class_constraints=json.dumps(CLASS_CONSTRAINTS))


@app.route('/api/predict-live', methods=['POST'])
def api_predict_live():
    """Lightweight API for real-time slider prediction (no DB save)."""
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400

    predicted_co2, conf_low, conf_high = predict_co2(data)
    rating = get_co2_rating(predicted_co2)
    label = get_co2_label(rating)
    color = get_co2_color(rating)
    footprint = calculate_carbon_footprint(predicted_co2, 15000)
    warnings = validate_inputs(data)
    recs = get_recommendations(predicted_co2, data.get('Fuel_Type', ''), float(data.get('Engine_Size', 0)))

    return jsonify({
        'co2': predicted_co2,
        'conf_low': conf_low,
        'conf_high': conf_high,
        'rating': rating,
        'label': label,
        'color': color,
        'footprint': footprint,
        'warnings': warnings,
        'recommendations': recs,
    })


# --- REST API ---

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """REST API endpoint for CO2 prediction. Accepts JSON, returns JSON."""
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400

    # Validate required fields
    required = CATEGORICAL_COLS + NUMERIC_COLS
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    warnings = validate_inputs(data)
    predicted_co2, conf_low, conf_high = predict_co2(data)
    rating = get_co2_rating(predicted_co2)
    label = get_co2_label(rating)
    engine_size = float(data.get('Engine_Size', 0))
    recs = get_recommendations(predicted_co2, data.get('Fuel_Type', ''), engine_size)
    annual_km = float(data.get('annual_km', 15000))
    footprint = calculate_carbon_footprint(predicted_co2, annual_km)

    return jsonify({
        'predicted_co2': predicted_co2,
        'unit': 'g/km',
        'confidence_interval': {'low': conf_low, 'high': conf_high},
        'rating': rating,
        'rating_label': label,
        'warnings': warnings,
        'recommendations': recs,
        'carbon_footprint': footprint,
    })


@app.route('/api/validate', methods=['POST'])
def api_validate():
    """Validate input combinations without predicting."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400
    warnings = validate_inputs(data)
    return jsonify({'valid': len(warnings) == 0, 'warnings': warnings})


# --- Init ---

load_model()
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5012, debug=True)
