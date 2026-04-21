from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify, g
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pickle
import numpy as np
import sqlite3
import random
import csv
import os
import time
import requests as http_requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ddos_detection_secret_2024'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# Replay & Poller state
replay_active = False
poller_active = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database.db')

model = pickle.load(open(os.path.join(BASE_DIR, 'ddos.sav'), 'rb'))

FIELDS = ['switch', 'pktcount', 'bytecount', 'dur', 'dur_nsec', 'flows',
          'pktrate', 'Pairflow', 'port_no', 'tx_bytes', 'rx_bytes', 'tx_kbps', 'rx_kbps']

# Simulation ranges (based on dataset min/max values)
SIM_RANGES = {
    'switch':    (1, 10),
    'pktcount':  (1, 50000),
    'bytecount': (50, 5000000),
    'dur':       (1, 120),
    'dur_nsec':  (100000, 999999999),
    'flows':     (1, 500),
    'pktrate':   (0.1, 5000.0),
    'Pairflow':  (1, 250),
    'port_no':   (1, 65535),
    'tx_bytes':  (0, 5000000),
    'rx_bytes':  (0, 5000000),
    'tx_kbps':   (0.0, 10000.0),
    'rx_kbps':   (0.0, 10000.0),
}


# ─── Database Helpers ───────────────────────────────────────────────

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    db.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        switch REAL, pktcount REAL, bytecount REAL, dur REAL, dur_nsec REAL,
        flows REAL, pktrate REAL, pairflow REAL, port_no REAL,
        tx_bytes REAL, rx_bytes REAL, tx_kbps REAL, rx_kbps REAL,
        result TEXT NOT NULL,
        source TEXT DEFAULT 'manual',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    # Seed admin user
    existing = db.execute("SELECT id FROM users WHERE username = 'admin'").fetchone()
    if not existing:
        db.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)",
                   ('admin', generate_password_hash('admin123'), 'Administrator'))
    db.commit()
    db.close()


# ─── Auth Decorator ─────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ─── Routes ─────────────────────────────────────────────────────────

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not name or not username or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')

        db = get_db()
        if db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone():
            flash('Username already exists.', 'danger')
            return render_template('register.html')

        db.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)",
                   (username, generate_password_hash(password), name))
        db.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['name'] = user['name']
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('predict'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    prediction_result = None

    if request.method == 'POST':
        try:
            input_data = [float(request.form.get(field, 0)) for field in FIELDS]
            pred = model.predict([input_data])[0]
            label = "DDoS" if pred == 1 else "Normal"
            prediction_result = "DDoS Attack Detected" if label == "DDoS" else "Normal Traffic"

            # Save to database
            db = get_db()
            db.execute(
                """INSERT INTO predictions
                   (user_id, switch, pktcount, bytecount, dur, dur_nsec, flows,
                    pktrate, pairflow, port_no, tx_bytes, rx_bytes, tx_kbps, rx_kbps,
                    result, source)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                [session['user_id']] + input_data + [label, 'manual']
            )
            db.commit()
            emit_dashboard_update()

        except Exception as e:
            prediction_result = f"Error: {str(e)}"

    return render_template('prediction.html', prediction=prediction_result)


@app.route('/suggestion')
@login_required
def suggestion():
    db = get_db()
    last = db.execute(
        "SELECT result FROM predictions WHERE user_id = ? ORDER BY id DESC LIMIT 1",
        (session['user_id'],)
    ).fetchone()

    last_prediction = last['result'] if last else None

    if last_prediction == "DDoS":
        suggestions = [
            ("Monitor abnormal traffic spikes and alert your team immediately.", "danger"),
            ("Use IP blacklisting to restrict suspicious sources.", "danger"),
            ("Apply rate-limiting policies.", "danger"),
            ("Enable deep packet inspection for sensitive applications.", "danger"),
            ("Consider geo-blocking for known malicious regions.", "danger"),
        ]
    else:
        suggestions = [
            ("Network appears stable. Continue monitoring.", "success"),
            ("Maintain your firewall and IDS configurations.", "success"),
            ("Keep security patches up to date.", "success"),
            ("Schedule regular vulnerability scans.", "success"),
            ("Educate users on phishing and social engineering.", "success"),
        ]

    return render_template('suggestion.html', suggestions=suggestions, last_prediction=last_prediction)


@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    total = db.execute("SELECT COUNT(*) as c FROM predictions").fetchone()['c']
    ddos_count = db.execute("SELECT COUNT(*) as c FROM predictions WHERE result='DDoS'").fetchone()['c']
    normal_count = db.execute("SELECT COUNT(*) as c FROM predictions WHERE result='Normal'").fetchone()['c']
    user_count = db.execute("SELECT COUNT(*) as c FROM users").fetchone()['c']

    recent = db.execute(
        """SELECT p.*, u.username FROM predictions p
           JOIN users u ON p.user_id = u.id
           ORDER BY p.id DESC LIMIT 20"""
    ).fetchall()

    # Traffic over time (last 50 predictions)
    traffic_rows = db.execute(
        "SELECT rx_kbps, tx_kbps, result, created_at FROM predictions ORDER BY id DESC LIMIT 50"
    ).fetchall()
    traffic = [dict(t) for t in reversed(traffic_rows)]

    return render_template('dashboard.html',
                           total=total, ddos_count=ddos_count,
                           normal_count=normal_count, user_count=user_count,
                           recent=recent, traffic=traffic)


@app.route('/model-info')
@login_required
def model_info():
    # Hard-coded metrics from the training notebook
    metrics = {
        'algorithm': 'Random Forest Classifier',
        'accuracy': 99.39,
        'precision': 99.40,
        'recall': 99.39,
        'f1_score': 99.39,
        'dataset_size': 104345,
        'train_size': 83476,
        'test_size': 20869,
        'features': len(FIELDS),
        'classes': ['Normal (0)', 'DDoS (1)'],
    }

    confusion_matrix = {
        'tp': 10356, 'fp': 72,
        'fn': 55, 'tn': 10386,
    }

    model_comparison = [
        {'name': 'Random Forest', 'accuracy': 99.39},
        {'name': 'Decision Tree', 'accuracy': 99.25},
        {'name': 'K-Nearest Neighbors', 'accuracy': 98.78},
        {'name': 'Support Vector Machine', 'accuracy': 97.12},
        {'name': 'Logistic Regression', 'accuracy': 94.56},
    ]

    feature_importance = [
        ('bytecount', 0.182), ('pktcount', 0.165), ('tx_bytes', 0.142),
        ('rx_bytes', 0.138), ('pktrate', 0.098), ('flows', 0.072),
        ('tx_kbps', 0.058), ('rx_kbps', 0.051), ('dur', 0.034),
        ('Pairflow', 0.024), ('dur_nsec', 0.018), ('switch', 0.012),
        ('port_no', 0.006),
    ]

    return render_template('model_info.html',
                           metrics=metrics, confusion_matrix=confusion_matrix,
                           model_comparison=model_comparison,
                           feature_importance=feature_importance)


@app.route('/simulate', methods=['POST'])
@login_required
def simulate():
    count = int(request.form.get('count', 5))
    count = max(1, min(count, 20))

    db = get_db()
    results = {'DDoS': 0, 'Normal': 0}

    for _ in range(count):
        input_data = [round(random.uniform(*SIM_RANGES[f]), 4) for f in FIELDS]
        pred = model.predict([input_data])[0]
        label = "DDoS" if pred == 1 else "Normal"
        results[label] += 1

        db.execute(
            """INSERT INTO predictions
               (user_id, switch, pktcount, bytecount, dur, dur_nsec, flows,
                pktrate, pairflow, port_no, tx_bytes, rx_bytes, tx_kbps, rx_kbps,
                result, source)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [session['user_id']] + input_data + [label, 'simulation']
        )

    db.commit()
    emit_dashboard_update()
    flash(f'Simulated {count} packets: {results["DDoS"]} DDoS, {results["Normal"]} Normal', 'info')
    return redirect(url_for('dashboard'))


@app.route('/api/dashboard-data')
@login_required
def dashboard_data():
    db = get_db()
    total = db.execute("SELECT COUNT(*) as c FROM predictions").fetchone()['c']
    ddos_count = db.execute("SELECT COUNT(*) as c FROM predictions WHERE result='DDoS'").fetchone()['c']
    normal_count = db.execute("SELECT COUNT(*) as c FROM predictions WHERE result='Normal'").fetchone()['c']

    traffic = db.execute(
        "SELECT rx_kbps, tx_kbps, result, created_at FROM predictions ORDER BY id DESC LIMIT 50"
    ).fetchall()
    traffic = list(reversed(traffic))

    recent = db.execute(
        """SELECT p.id, p.result, p.source, p.rx_kbps, p.tx_kbps, p.created_at, u.username
           FROM predictions p JOIN users u ON p.user_id = u.id
           ORDER BY p.id DESC LIMIT 10"""
    ).fetchall()

    return jsonify({
        'total': total,
        'ddos_count': ddos_count,
        'normal_count': normal_count,
        'traffic': [{'rx_kbps': t['rx_kbps'], 'tx_kbps': t['tx_kbps'],
                      'result': t['result'], 'created_at': t['created_at']} for t in traffic],
        'recent': [{'id': r['id'], 'result': r['result'], 'source': r['source'],
                     'rx_kbps': round(r['rx_kbps'], 2), 'tx_kbps': round(r['tx_kbps'], 2),
                     'created_at': r['created_at'], 'username': r['username']} for r in recent],
    })


# ─── External API Endpoint ──────────────────────────────────────────

API_KEY = 'sdn_monitor_2024'  # Simple API key for external access

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """External API endpoint for real-time network monitoring.

    Accepts JSON with 13 SDN features, classifies traffic, stores in DB,
    and pushes live update to all dashboard clients via WebSocket.

    Usage:
        curl -X POST http://127.0.0.1:5021/api/predict \
             -H "Content-Type: application/json" \
             -H "X-API-Key: sdn_monitor_2024" \
             -d '{"switch":1,"pktcount":4777,"bytecount":5092282,"dur":10,
                  "dur_nsec":711000000,"flows":3,"pktrate":0,"Pairflow":0,
                  "port_no":2,"tx_bytes":3753,"rx_bytes":1332,"tx_kbps":0,"rx_kbps":0}'
    """
    # API key authentication
    api_key = request.headers.get('X-API-Key', '')
    if api_key != API_KEY:
        return jsonify({'error': 'Invalid or missing API key. Pass X-API-Key header.'}), 401

    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Request body must be JSON with 13 SDN features.'}), 400

    # Extract features
    try:
        input_data = []
        missing = []
        for field in FIELDS:
            if field not in data:
                missing.append(field)
            val = data.get(field, 0)
            input_data.append(float(val) if val is not None else 0.0)

        if missing:
            return jsonify({'error': f'Missing fields: {", ".join(missing)}',
                            'required_fields': FIELDS}), 400

        pred = model.predict([input_data])[0]
        label = "DDoS" if pred == 1 else "Normal"

        # Store in DB (user_id=1 for API/external source)
        db = sqlite3.connect(DATABASE)
        db.execute(
            """INSERT INTO predictions
               (user_id, switch, pktcount, bytecount, dur, dur_nsec, flows,
                pktrate, pairflow, port_no, tx_bytes, rx_bytes, tx_kbps, rx_kbps,
                result, source)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [1] + input_data + [label, 'api']
        )
        db.commit()
        db.close()

        emit_dashboard_update()

        return jsonify({
            'result': label,
            'description': 'DDoS Attack Detected' if label == 'DDoS' else 'Normal Traffic',
            'features': dict(zip(FIELDS, input_data)),
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/batch', methods=['POST'])
def api_predict_batch():
    """Batch prediction endpoint — accepts array of flow records.

    Usage:
        curl -X POST http://127.0.0.1:5021/api/predict/batch \
             -H "Content-Type: application/json" \
             -H "X-API-Key: sdn_monitor_2024" \
             -d '{"records": [{"switch":1,...}, {"switch":2,...}]}'
    """
    api_key = request.headers.get('X-API-Key', '')
    if api_key != API_KEY:
        return jsonify({'error': 'Invalid or missing API key.'}), 401

    data = request.get_json(silent=True)
    if not data or 'records' not in data:
        return jsonify({'error': 'JSON body must contain "records" array.'}), 400

    records = data['records']
    if not isinstance(records, list) or len(records) == 0:
        return jsonify({'error': '"records" must be a non-empty array.'}), 400
    if len(records) > 100:
        return jsonify({'error': 'Maximum 100 records per batch.'}), 400

    db = sqlite3.connect(DATABASE)
    results = []
    ddos_count = 0
    normal_count = 0

    for i, row in enumerate(records):
        try:
            input_data = [float(row.get(field, 0) or 0) for field in FIELDS]
            pred = model.predict([input_data])[0]
            label = "DDoS" if pred == 1 else "Normal"

            if label == "DDoS":
                ddos_count += 1
            else:
                normal_count += 1

            db.execute(
                """INSERT INTO predictions
                   (user_id, switch, pktcount, bytecount, dur, dur_nsec, flows,
                    pktrate, pairflow, port_no, tx_bytes, rx_bytes, tx_kbps, rx_kbps,
                    result, source)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                [1] + input_data + [label, 'api']
            )
            results.append({'index': i, 'result': label})

        except Exception as e:
            results.append({'index': i, 'error': str(e)})

    db.commit()
    db.close()
    emit_dashboard_update()

    return jsonify({
        'total': len(records),
        'ddos_count': ddos_count,
        'normal_count': normal_count,
        'results': results,
    })


# ─── SocketIO Helper ────────────────────────────────────────────────

def emit_dashboard_update():
    """Query current stats and emit to all connected clients."""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row

    total = db.execute("SELECT COUNT(*) as c FROM predictions").fetchone()['c']
    ddos_count = db.execute("SELECT COUNT(*) as c FROM predictions WHERE result='DDoS'").fetchone()['c']
    normal_count = db.execute("SELECT COUNT(*) as c FROM predictions WHERE result='Normal'").fetchone()['c']

    traffic_rows = db.execute(
        "SELECT rx_kbps, tx_kbps, result, created_at FROM predictions ORDER BY id DESC LIMIT 50"
    ).fetchall()
    traffic = [dict(t) for t in reversed(traffic_rows)]

    recent_rows = db.execute(
        """SELECT p.id, p.result, p.source, p.rx_kbps, p.tx_kbps, p.created_at, u.username
           FROM predictions p JOIN users u ON p.user_id = u.id
           ORDER BY p.id DESC LIMIT 10"""
    ).fetchall()
    recent = [{'id': r['id'], 'result': r['result'], 'source': r['source'],
               'rx_kbps': round(r['rx_kbps'], 2), 'tx_kbps': round(r['tx_kbps'], 2),
               'created_at': r['created_at'], 'username': r['username']} for r in recent_rows]

    db.close()

    socketio.emit('dashboard_update', {
        'total': total,
        'ddos_count': ddos_count,
        'normal_count': normal_count,
        'traffic': traffic,
        'recent': recent,
    })


# ─── CSV Upload Routes ───────────────────────────────────────────────

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def process_csv(user_id, csv_path, speed, max_rows):
    """Background task: read uploaded CSV rows, predict, store, and emit live updates."""
    global replay_active
    replay_active = True
    db = sqlite3.connect(DATABASE)
    processed = 0
    ddos = 0
    normal = 0
    total_rows = 0

    # Count total rows first (capped at max_rows)
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for _ in reader:
            total_rows += 1
            if total_rows >= max_rows:
                break

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not replay_active or processed >= max_rows:
                break

            try:
                input_data = []
                for field in FIELDS:
                    val = row.get(field, '0')
                    input_data.append(float(val) if val and val.strip() != '' else 0.0)

                pred = model.predict([input_data])[0]
                label = "DDoS" if pred == 1 else "Normal"
                if label == "DDoS":
                    ddos += 1
                else:
                    normal += 1

                db.execute(
                    """INSERT INTO predictions
                       (user_id, switch, pktcount, bytecount, dur, dur_nsec, flows,
                        pktrate, pairflow, port_no, tx_bytes, rx_bytes, tx_kbps, rx_kbps,
                        result, source)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    [user_id] + input_data + [label, 'csv']
                )
                db.commit()
                processed += 1

                socketio.emit('csv_progress', {
                    'current': processed,
                    'total': total_rows,
                    'result': label,
                    'ddos': ddos,
                    'normal': normal,
                })

                emit_dashboard_update()
                time.sleep(speed)

            except Exception as e:
                print(f"CSV row error: {e}")
                continue

    db.close()
    replay_active = False

    # Clean up uploaded file
    try:
        os.remove(csv_path)
    except OSError:
        pass

    socketio.emit('csv_complete', {
        'processed': processed,
        'ddos': ddos,
        'normal': normal,
    })


@app.route('/upload-csv', methods=['POST'])
@login_required
def upload_csv():
    global replay_active
    if replay_active:
        return jsonify({'error': 'A CSV is already being processed.'}), 409

    file = request.files.get('csv_file')
    if not file or file.filename == '':
        return jsonify({'error': 'Please select a CSV file.'}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only .csv files are supported.'}), 400

    # Validate CSV headers
    import io
    content = file.read().decode('utf-8')
    sample = io.StringIO(content)
    reader = csv.DictReader(sample)
    headers = reader.fieldnames or []
    missing = [f for f in FIELDS if f not in headers]
    if missing:
        return jsonify({'error': f'CSV missing columns: {", ".join(missing)}'}), 400

    # Save the file
    filename = f"upload_{int(time.time())}_{session['user_id']}.csv"
    csv_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(csv_path, 'w') as f:
        f.write(content)

    speed = float(request.form.get('speed', 1.0))
    max_rows = int(request.form.get('max_rows', 500))
    max_rows = max(1, min(max_rows, 5000))
    user_id = session['user_id']

    socketio.start_background_task(process_csv, user_id, csv_path, speed, max_rows)
    return jsonify({'message': f'Processing up to {max_rows} rows at {speed}s/row'})


@app.route('/stop-csv', methods=['POST'])
@login_required
def stop_csv():
    global replay_active
    replay_active = False
    return jsonify({'message': 'CSV processing stopped.'})


# ─── Endpoint Poller Routes ─────────────────────────────────────────

def poll_endpoint(user_id, endpoint_url, interval, max_polls):
    """Background task: poll an external URL for SDN flow data and classify."""
    global poller_active
    poller_active = True
    processed = 0
    ddos = 0
    normal = 0

    db = sqlite3.connect(DATABASE)

    while poller_active and processed < max_polls:
        try:
            resp = http_requests.get(endpoint_url, timeout=5)
            resp.raise_for_status()
            payload = resp.json()

            # Support both single record and array of records
            records = payload if isinstance(payload, list) else [payload]

            for row in records:
                if not poller_active or processed >= max_polls:
                    break

                input_data = [float(row.get(field, 0) or 0) for field in FIELDS]
                pred = model.predict([input_data])[0]
                label = "DDoS" if pred == 1 else "Normal"

                if label == "DDoS":
                    ddos += 1
                else:
                    normal += 1

                db.execute(
                    """INSERT INTO predictions
                       (user_id, switch, pktcount, bytecount, dur, dur_nsec, flows,
                        pktrate, pairflow, port_no, tx_bytes, rx_bytes, tx_kbps, rx_kbps,
                        result, source)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    [user_id] + input_data + [label, 'poller']
                )
                db.commit()
                processed += 1

                socketio.emit('poller_progress', {
                    'current': processed,
                    'total': max_polls,
                    'result': label,
                    'ddos': ddos,
                    'normal': normal,
                })

                emit_dashboard_update()

        except Exception as e:
            socketio.emit('poller_progress', {
                'current': processed,
                'total': max_polls,
                'result': 'error',
                'error': str(e),
                'ddos': ddos,
                'normal': normal,
            })

        time.sleep(interval)

    db.close()
    poller_active = False
    socketio.emit('poller_complete', {
        'processed': processed,
        'ddos': ddos,
        'normal': normal,
    })


@app.route('/start-poller', methods=['POST'])
@login_required
def start_poller():
    global poller_active
    if poller_active:
        return jsonify({'error': 'Poller is already running.'}), 409

    endpoint_url = request.form.get('endpoint_url', '').strip()
    if not endpoint_url:
        return jsonify({'error': 'Endpoint URL is required.'}), 400

    interval = float(request.form.get('poll_interval', 5.0))
    interval = max(1.0, min(interval, 60.0))
    max_polls = int(request.form.get('max_polls', 50))
    max_polls = max(1, min(max_polls, 500))
    user_id = session['user_id']

    socketio.start_background_task(poll_endpoint, user_id, endpoint_url, interval, max_polls)
    return jsonify({'message': f'Polling {endpoint_url} every {interval}s (max {max_polls} records)'})


@app.route('/stop-poller', methods=['POST'])
@login_required
def stop_poller():
    global poller_active
    poller_active = False
    return jsonify({'message': 'Poller stopped.'})


# ─── Init & Run ─────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    socketio.run(app, debug=True, port=5021, allow_unsafe_werkzeug=True)
