from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
import re
import json
import joblib
import numpy as np
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'hatespeech_secret_key_2024'

DB_PATH = 'hate_speech.db'
MODEL_PATH = 'hate_speech_model.pkl'
VECTORIZER_PATH = 'tfidf_vectorizer.pkl'
MODELS_INFO_PATH = 'models_info.json'

LABEL_MAP = {0: "Hate Speech", 1: "Offensive", 2: "Clean"}

# Load model and vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# Load models info
with open(MODELS_INFO_PATH, 'r') as f:
    models_info = json.load(f)

# --- NLTK stopwords ---
try:
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
except Exception:
    import nltk
    nltk.download('stopwords', quiet=True)
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))


# --- Text Preprocessing (same as training) ---
def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return ' '.join(words)


# --- Database ---
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        input_text TEXT,
        prediction TEXT,
        confidence REAL,
        text_length INTEGER,
        word_count INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    # Seed admin
    existing = conn.execute("SELECT id FROM users WHERE username = 'admin'").fetchone()
    if not existing:
        conn.execute("INSERT INTO users (name, username, password, is_admin) VALUES (?, ?, ?, 1)",
                     ("Admin", "admin", generate_password_hash("admin123")))
    conn.commit()
    conn.close()


init_db()


# --- Auth decorator ---
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# --- Routes ---

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['name'] = user['name']
            session['is_admin'] = user['is_admin']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        existing = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        if existing:
            conn.close()
            flash('Username already exists.', 'danger')
            return render_template('register.html')
        conn.execute("INSERT INTO users (name, username, password) VALUES (?, ?, ?)",
                     (name, username, generate_password_hash(password)))
        conn.commit()
        conn.close()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    conn = get_db()
    user_predictions = conn.execute(
        "SELECT COUNT(*) as cnt FROM predictions WHERE user_id = ?", (session['user_id'],)
    ).fetchone()['cnt']
    hate_count = conn.execute(
        "SELECT COUNT(*) as cnt FROM predictions WHERE user_id = ? AND prediction = 'Hate Speech'",
        (session['user_id'],)
    ).fetchone()['cnt']
    offensive_count = conn.execute(
        "SELECT COUNT(*) as cnt FROM predictions WHERE user_id = ? AND prediction = 'Offensive'",
        (session['user_id'],)
    ).fetchone()['cnt']
    clean_count = conn.execute(
        "SELECT COUNT(*) as cnt FROM predictions WHERE user_id = ? AND prediction = 'Clean'",
        (session['user_id'],)
    ).fetchone()['cnt']
    recent = conn.execute(
        "SELECT * FROM predictions WHERE user_id = ? ORDER BY created_at DESC LIMIT 5",
        (session['user_id'],)
    ).fetchall()

    admin_stats = None
    if session.get('is_admin'):
        total_users = conn.execute("SELECT COUNT(*) as cnt FROM users").fetchone()['cnt']
        total_predictions = conn.execute("SELECT COUNT(*) as cnt FROM predictions").fetchone()['cnt']
        total_hate = conn.execute(
            "SELECT COUNT(*) as cnt FROM predictions WHERE prediction = 'Hate Speech'"
        ).fetchone()['cnt']
        admin_stats = {
            'total_users': total_users,
            'total_predictions': total_predictions,
            'total_hate': total_hate,
        }

    conn.close()
    return render_template('home.html',
                           user_predictions=user_predictions,
                           hate_count=hate_count,
                           offensive_count=offensive_count,
                           clean_count=clean_count,
                           recent=recent,
                           admin_stats=admin_stats)


@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    result = None
    if request.method == 'POST':
        input_text = request.form['text']
        cleaned = preprocess_text(input_text)
        X = vectorizer.transform([cleaned])
        proba = model.predict_proba(X)[0]
        pred_label = int(np.argmax(proba))
        confidence = round(float(proba[pred_label]) * 100, 2)
        prediction = LABEL_MAP[pred_label]

        text_length = len(input_text)
        word_count = len(input_text.split())

        conn = get_db()
        conn.execute(
            "INSERT INTO predictions (user_id, input_text, prediction, confidence, text_length, word_count) VALUES (?, ?, ?, ?, ?, ?)",
            (session['user_id'], input_text, prediction, confidence, text_length, word_count)
        )
        conn.commit()
        conn.close()

        result = {
            'input_text': input_text,
            'prediction': prediction,
            'confidence': confidence,
            'text_length': text_length,
            'word_count': word_count,
            'pred_label': pred_label,
        }

    return render_template('predict.html', result=result)


@app.route('/history')
@login_required
def history():
    conn = get_db()
    predictions = conn.execute(
        "SELECT * FROM predictions WHERE user_id = ? ORDER BY created_at DESC",
        (session['user_id'],)
    ).fetchall()
    conn.close()
    return render_template('history.html', predictions=predictions)


@app.route('/visualize')
@login_required
def visualize():
    return render_template('visualize.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', models_info=models_info)


@app.route('/about')
@login_required
def about():
    return render_template('about.html', models_info=models_info)


if __name__ == '__main__':
    app.run(debug=True, port=5007)
