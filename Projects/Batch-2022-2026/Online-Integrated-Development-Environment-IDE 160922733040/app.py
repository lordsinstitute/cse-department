"""
CodeForge — Online Integrated Development Environment
Flask Application | Port: 5016
"""
import os
import sqlite3
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

from code_runner import run_python
from ai_assistant import ai_assist, get_mode

load_dotenv()

app = Flask(__name__)
app.secret_key = 'codeforge_secret_key_2025'

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'codeforge.db')


# --- Database ---
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    db.execute('''CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        language TEXT NOT NULL,
        code TEXT NOT NULL,
        output TEXT,
        ai_action TEXT,
        ai_response TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    db.execute('''CREATE TABLE IF NOT EXISTS snippets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        language TEXT NOT NULL,
        code TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    # Seed admin
    existing = db.execute('SELECT id FROM users WHERE username = ?', ('admin',)).fetchone()
    if not existing:
        db.execute('INSERT INTO users (username, password, name, is_admin) VALUES (?, ?, ?, ?)',
                   ('admin', generate_password_hash('admin123'), 'Administrator', 1))
    db.commit()
    db.close()


init_db()


# --- Context processor ---
@app.context_processor
def inject_globals():
    return {'ai_mode': get_mode()}


# --- Auth decorator ---
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# --- Auth Routes ---
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
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['name'] = user['name']
            session['is_admin'] = bool(user['is_admin'])
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
        if not name or not username or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')
        db = get_db()
        existing = db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        if existing:
            flash('Username already exists.', 'danger')
            return render_template('register.html')
        db.execute('INSERT INTO users (username, password, name) VALUES (?, ?, ?)',
                   (username, generate_password_hash(password), name))
        db.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))


# --- Main Routes ---
@app.route('/home')
@login_required
def home():
    db = get_db()
    uid = session['user_id']

    total_sessions = db.execute('SELECT COUNT(*) FROM sessions WHERE user_id = ?', (uid,)).fetchone()[0]
    total_snippets = db.execute('SELECT COUNT(*) FROM snippets WHERE user_id = ?', (uid,)).fetchone()[0]
    ai_queries = db.execute('SELECT COUNT(*) FROM sessions WHERE user_id = ? AND ai_action IS NOT NULL', (uid,)).fetchone()[0]

    recent = db.execute('SELECT * FROM sessions WHERE user_id = ? ORDER BY created_at DESC LIMIT 5', (uid,)).fetchall()

    total_users = 0
    all_sessions = 0
    if session.get('is_admin'):
        total_users = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        all_sessions = db.execute('SELECT COUNT(*) FROM sessions').fetchone()[0]

    return render_template('home.html',
                           total_sessions=total_sessions,
                           total_snippets=total_snippets,
                           ai_queries=ai_queries,
                           recent=recent,
                           total_users=total_users,
                           all_sessions=all_sessions)


@app.route('/editor')
@login_required
def editor():
    return render_template('editor.html')


@app.route('/run', methods=['POST'])
@login_required
def run_code():
    data = request.get_json()
    code = data.get('code', '')
    language = data.get('language', 'python')

    if language != 'python':
        return jsonify({
            'stdout': '',
            'stderr': 'Execution is available for Python only.\nUse AI Assistant to analyze code in other languages.',
            'status': 'info'
        })

    result = run_python(code)

    # Log session
    db = get_db()
    output_text = result['stdout'] + ('\n' + result['stderr'] if result['stderr'] else '')
    db.execute('INSERT INTO sessions (user_id, language, code, output) VALUES (?, ?, ?, ?)',
               (session['user_id'], language, code, output_text))
    db.commit()

    return jsonify(result)


@app.route('/ai', methods=['POST'])
@login_required
def ai_action():
    data = request.get_json()
    code = data.get('code', '')
    language = data.get('language', 'python')
    action = data.get('action', 'analyze')
    prompt = data.get('prompt', '')

    response = ai_assist(code, language, action, prompt)

    # Log session
    db = get_db()
    db.execute('INSERT INTO sessions (user_id, language, code, ai_action, ai_response) VALUES (?, ?, ?, ?, ?)',
               (session['user_id'], language, code, action, response))
    db.commit()

    return jsonify({'response': response, 'mode': get_mode()})


@app.route('/snippets')
@login_required
def snippets():
    db = get_db()
    user_snippets = db.execute('SELECT * FROM snippets WHERE user_id = ? ORDER BY created_at DESC',
                               (session['user_id'],)).fetchall()
    return render_template('snippets.html', snippets=user_snippets)


@app.route('/snippets/save', methods=['POST'])
@login_required
def save_snippet():
    data = request.get_json()
    title = data.get('title', '').strip()
    code = data.get('code', '')
    language = data.get('language', 'python')

    if not title or not code:
        return jsonify({'success': False, 'error': 'Title and code are required'})

    db = get_db()
    db.execute('INSERT INTO snippets (user_id, title, language, code) VALUES (?, ?, ?, ?)',
               (session['user_id'], title, language, code))
    db.commit()

    return jsonify({'success': True})


@app.route('/snippets/load/<int:snippet_id>')
@login_required
def load_snippet(snippet_id):
    db = get_db()
    snippet = db.execute('SELECT * FROM snippets WHERE id = ? AND user_id = ?',
                         (snippet_id, session['user_id'])).fetchone()
    if not snippet:
        return jsonify({'success': False, 'error': 'Snippet not found'})

    return jsonify({
        'success': True,
        'title': snippet['title'],
        'language': snippet['language'],
        'code': snippet['code']
    })


@app.route('/history')
@login_required
def history():
    db = get_db()
    sessions_list = db.execute('SELECT * FROM sessions WHERE user_id = ? ORDER BY created_at DESC',
                               (session['user_id'],)).fetchall()
    return render_template('history.html', sessions=sessions_list)


@app.route('/about')
@login_required
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True, port=5016)
