"""
Malicious URL Detection — Flask Web Application
Detects whether a URL is legitimate or malicious using ML.
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle
import numpy as np
import json
import re
import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'malicious-url-detect-2024-secret'

# ───────────── Load model and config ─────────────
with open('url_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models_info.json', 'r') as f:
    models_info = json.load(f)

FEATURE_ORDER = models_info['features']

SUSPICIOUS_WORDS = [
    'login', 'verify', 'secure', 'account', 'update', 'confirm', 'bank',
    'signin', 'password', 'credential', 'security', 'alert', 'suspended',
    'unlock', 'restore', 'wallet', 'payment', 'billing', 'invoice',
]


# ───────────── Database ─────────────
def get_db():
    db = sqlite3.connect('url_detect.db')
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    db.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        url TEXT NOT NULL,
        prediction TEXT NOT NULL,
        confidence REAL NOT NULL,
        url_length INTEGER,
        has_https INTEGER,
        has_ip INTEGER,
        n_suspicious_words INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    # Seed admin
    existing = db.execute('SELECT id FROM users WHERE username = ?', ('admin',)).fetchone()
    if not existing:
        db.execute('INSERT INTO users (name, username, password, is_admin) VALUES (?, ?, ?, ?)',
                   ('Administrator', 'admin', generate_password_hash('admin123'), 1))
    db.commit()
    db.close()


init_db()


# ───────────── Feature Extraction ─────────────
def extract_features(url):
    """Extract numerical features from a URL string."""
    features = {}

    features['url_length'] = len(url)
    features['n_dots'] = url.count('.')
    features['n_hyphens'] = url.count('-')
    features['n_underscores'] = url.count('_')
    features['n_slashes'] = url.count('/')
    features['n_question_marks'] = url.count('?')
    features['n_equal'] = url.count('=')
    features['n_at'] = url.count('@')
    features['n_ampersand'] = url.count('&')
    features['n_percent'] = url.count('%')
    features['n_digits'] = sum(c.isdigit() for c in url)
    features['n_letters'] = sum(c.isalpha() for c in url)
    features['n_special'] = sum(not c.isalnum() for c in url)

    features['has_https'] = 1 if url.lower().startswith('https://') else 0

    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    features['has_ip'] = 1 if re.search(ip_pattern, url) else 0

    try:
        after_protocol = url.split('://')[-1]
        domain_part = after_protocol.split('/')[0].split('?')[0].split('@')[-1]
        features['domain_length'] = len(domain_part)
        features['n_subdomains'] = domain_part.count('.')
    except Exception:
        features['domain_length'] = 0
        features['n_subdomains'] = 0

    try:
        after_domain = url.split('://')[-1]
        path_part = '/'.join(after_domain.split('/')[1:])
        features['path_length'] = len(path_part)
        features['url_depth'] = path_part.count('/') + 1 if path_part else 0
    except Exception:
        features['path_length'] = 0
        features['url_depth'] = 0

    features['has_at_symbol'] = 1 if '@' in url else 0
    features['double_slash_redirect'] = 1 if url.count('//') > 1 else 0
    features['prefix_suffix'] = 1 if '-' in url.split('://')[-1].split('/')[0] else 0

    url_lower = url.lower()
    features['n_suspicious_words'] = sum(1 for word in SUSPICIOUS_WORDS if word in url_lower)
    features['is_shortened'] = 1 if any(s in url_lower for s in
                                        ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'is.gd', 'ow.ly']) else 0

    suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club', '.work', '.buzz']
    features['suspicious_tld'] = 1 if any(url_lower.endswith(t) or (t + '/') in url_lower
                                          for t in suspicious_tlds) else 0

    total_chars = len(url) if len(url) > 0 else 1
    features['digit_ratio'] = round(features['n_digits'] / total_chars, 4)
    features['letter_ratio'] = round(features['n_letters'] / total_chars, 4)
    features['special_ratio'] = round(features['n_special'] / total_chars, 4)

    return features


def predict_url(url):
    """Extract features from a URL and predict if malicious."""
    features = extract_features(url)
    feature_values = [features[f] for f in FEATURE_ORDER]
    arr = np.array([feature_values])

    proba = model.predict_proba(arr)[0]
    pred_class = int(np.argmax(proba))
    confidence = round(proba[pred_class] * 100, 2)

    prediction = 'Malicious' if pred_class == 1 else 'Legitimate'
    return prediction, confidence, features


# ───────────── Auth Routes ─────────────
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
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        db.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['name'] = user['name']
            session['is_admin'] = user['is_admin']
            flash('Welcome back, ' + user['name'] + '!', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')


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
        existing = db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        if existing:
            db.close()
            flash('Username already exists.', 'danger')
            return render_template('register.html')
        db.execute('INSERT INTO users (name, username, password) VALUES (?, ?, ?)',
                   (name, username, generate_password_hash(password)))
        db.commit()
        db.close()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))


# ───────────── Main Routes ─────────────
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    user_preds = db.execute('SELECT COUNT(*) as cnt FROM predictions WHERE user_id = ?',
                            (session['user_id'],)).fetchone()['cnt']
    user_malicious = db.execute(
        "SELECT COUNT(*) as cnt FROM predictions WHERE user_id = ? AND prediction = 'Malicious'",
        (session['user_id'],)).fetchone()['cnt']
    recent = db.execute(
        'SELECT url, prediction, confidence, created_at FROM predictions WHERE user_id = ? ORDER BY id DESC LIMIT 5',
        (session['user_id'],)).fetchall()

    admin_stats = None
    if session.get('is_admin'):
        total_users = db.execute('SELECT COUNT(*) as cnt FROM users').fetchone()['cnt']
        total_preds = db.execute('SELECT COUNT(*) as cnt FROM predictions').fetchone()['cnt']
        total_malicious = db.execute(
            "SELECT COUNT(*) as cnt FROM predictions WHERE prediction = 'Malicious'").fetchone()['cnt']
        admin_stats = {'users': total_users, 'predictions': total_preds, 'malicious': total_malicious}

    db.close()
    return render_template('home.html', user_preds=user_preds, user_malicious=user_malicious,
                           recent=recent, admin_stats=admin_stats)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    result = None
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if not url:
            flash('Please enter a URL to analyze.', 'warning')
        elif not ('://' in url or '.' in url):
            flash('Please enter a valid URL (e.g., https://example.com).', 'warning')
        else:
            # Add protocol if missing
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'http://' + url

            prediction, confidence, features = predict_url(url)

            # Save to database
            db = get_db()
            db.execute('''INSERT INTO predictions
                (user_id, url, prediction, confidence, url_length, has_https, has_ip, n_suspicious_words)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (session['user_id'], url, prediction, confidence,
                        features['url_length'], features['has_https'],
                        features['has_ip'], features['n_suspicious_words']))
            db.commit()
            db.close()

            result = {
                'url': url,
                'prediction': prediction,
                'confidence': confidence,
                'features': {
                    'URL Length': features['url_length'],
                    'Domain Length': features['domain_length'],
                    'Path Length': features['path_length'],
                    'HTTPS': 'Yes' if features['has_https'] else 'No',
                    'IP Address': 'Yes' if features['has_ip'] else 'No',
                    'Subdomains': features['n_subdomains'],
                    'URL Depth': features['url_depth'],
                    'Dots': features['n_dots'],
                    'Hyphens': features['n_hyphens'],
                    'Digits': features['n_digits'],
                    'Special Chars': features['n_special'],
                    'Suspicious Words': features['n_suspicious_words'],
                    'At Symbol': 'Yes' if features['has_at_symbol'] else 'No',
                    'Shortened URL': 'Yes' if features['is_shortened'] else 'No',
                    'Suspicious TLD': 'Yes' if features['suspicious_tld'] else 'No',
                    'Double Slash Redirect': 'Yes' if features['double_slash_redirect'] else 'No',
                    'Digit Ratio': f"{features['digit_ratio']:.2%}",
                    'Special Char Ratio': f"{features['special_ratio']:.2%}",
                }
            }

    return render_template('predict.html', result=result)


@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    rows = db.execute(
        '''SELECT url, prediction, confidence, url_length, has_https, has_ip,
                  n_suspicious_words, created_at
           FROM predictions WHERE user_id = ? ORDER BY id DESC''',
        (session['user_id'],)).fetchall()
    db.close()
    return render_template('history.html', predictions=rows)


@app.route('/visualize')
def visualize():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('visualize.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', models_info=models_info)


@app.route('/about')
def about():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('about.html', models_info=models_info)


if __name__ == '__main__':
    app.run(debug=True, port=5004)
