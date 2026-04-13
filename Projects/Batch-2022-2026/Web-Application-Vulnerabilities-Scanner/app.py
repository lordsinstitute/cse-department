"""
A Simple Scanner for Identifying Web Application Vulnerabilities
Flask application with SQLite database.
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import os
import json
from urllib.parse import urlparse
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import csv

app = Flask(__name__)
app.secret_key = 'web_vuln_scanner_2025'
DB_PATH = 'scanner.db'
CSV_PATH = 'vulnerability_fix_dataset.csv'


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
        role TEXT DEFAULT 'user',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS scan_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        website TEXT NOT NULL,
        vulnerability TEXT NOT NULL,
        description TEXT NOT NULL,
        severity TEXT DEFAULT 'Medium',
        scan_date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    # Seed admin user
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)",
                  ('admin', generate_password_hash('admin123'), 'Administrator', 'admin'))

    conn.commit()
    conn.close()


def load_fix_dataset():
    """Load vulnerability fix suggestions from CSV."""
    fixes = {}
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                fixes[row['vulnerability_type'].lower()] = {
                    'vulnerable_code': row['vulnerable_code'],
                    'fixed_code': row['fixed_code'],
                    'description': row.get('fix_description', '')
                }
    return fixes


FIX_DATA = load_fix_dataset()

SEVERITY_MAP = {
    'sql injection': 'Critical',
    'cross-site scripting': 'High',
    'missing security header': 'Medium',
    'missing csp': 'Medium',
    'clickjacking': 'Medium',
    'directory listing': 'High',
    'csrf vulnerability': 'High',
    'insecure cookies': 'Medium',
    'information disclosure': 'Low',
    'mixed content': 'Low',
    'server version exposed': 'Low',
}


def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_fix(vuln_type):
    """Fetch fix info from loaded CSV data."""
    key = vuln_type.lower()
    if key in FIX_DATA:
        return FIX_DATA[key]['vulnerable_code'], FIX_DATA[key]['fixed_code']
    return "N/A", "N/A"


def get_severity(vuln_type):
    return SEVERITY_MAP.get(vuln_type.lower(), 'Medium')


def scan_website(url):
    """Scan a website for common vulnerabilities."""
    result = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        resp_headers = response.headers

        # 1. Check forms for XSS potential
        forms = soup.find_all('form')
        for form in forms:
            action = form.get('action', '')
            inputs = form.find_all('input')
            has_validation = form.get('onsubmit') or any(
                inp.get('pattern') or inp.get('required') for inp in inputs
            )
            if not has_validation:
                vuln_code, fix_code = get_fix("Cross-Site Scripting")
                result.append({
                    'type': 'Cross-Site Scripting',
                    'description': f'Form without input validation found (action: {action or "self"}).',
                    'severity': 'High',
                    'vuln_code': vuln_code,
                    'fix_code': fix_code
                })

        # 2. Check for missing X-Content-Type-Options
        if 'X-Content-Type-Options' not in resp_headers:
            vuln_code, fix_code = get_fix("Missing Security Header")
            result.append({
                'type': 'Missing Security Header',
                'description': 'X-Content-Type-Options header is missing. MIME-sniffing attacks possible.',
                'severity': 'Medium',
                'vuln_code': vuln_code,
                'fix_code': fix_code
            })

        # 3. Check for missing Content-Security-Policy
        if 'Content-Security-Policy' not in resp_headers:
            vuln_code, fix_code = get_fix("Missing CSP")
            result.append({
                'type': 'Missing CSP',
                'description': 'Content-Security-Policy header is missing. Inline script injection possible.',
                'severity': 'Medium',
                'vuln_code': vuln_code,
                'fix_code': fix_code
            })

        # 4. Check for Clickjacking (X-Frame-Options)
        if 'X-Frame-Options' not in resp_headers:
            vuln_code, fix_code = get_fix("Clickjacking")
            result.append({
                'type': 'Clickjacking',
                'description': 'X-Frame-Options header is missing. Page can be embedded in iframes.',
                'severity': 'Medium',
                'vuln_code': vuln_code,
                'fix_code': fix_code
            })

        # 5. Check for directory listing
        if re.search(r'Index of /', html):
            vuln_code, fix_code = get_fix("Directory Listing")
            result.append({
                'type': 'Directory Listing',
                'description': 'Open directory listing found. Server files are exposed.',
                'severity': 'High',
                'vuln_code': vuln_code,
                'fix_code': fix_code
            })

        # 6. Check for SQL injection (if URL has parameters)
        if '?' in url:
            test_url = url + "'"
            try:
                test_response = requests.get(test_url, headers=headers, timeout=5, verify=False)
                sql_errors = ['SQL syntax', 'mysql_fetch', 'ORA-', 'PostgreSQL', 'sqlite3',
                              'unclosed quotation', 'unterminated string', 'ODBC Driver']
                if any(err in test_response.text for err in sql_errors):
                    vuln_code, fix_code = get_fix("SQL Injection")
                    result.append({
                        'type': 'SQL Injection',
                        'description': 'Possible SQL injection point detected in URL parameters.',
                        'severity': 'Critical',
                        'vuln_code': vuln_code,
                        'fix_code': fix_code
                    })
            except:
                pass

        # 7. Check for CSRF (forms without tokens)
        for form in forms:
            inputs = form.find_all('input', {'type': 'hidden'})
            token_names = ['csrf', 'token', '_token', 'authenticity_token', 'csrfmiddlewaretoken']
            has_csrf = any(
                any(t in (inp.get('name', '').lower()) for t in token_names) for inp in inputs
            )
            if not has_csrf and form.get('method', '').lower() == 'post':
                vuln_code, fix_code = get_fix("CSRF Vulnerability")
                result.append({
                    'type': 'CSRF Vulnerability',
                    'description': 'POST form found without CSRF token protection.',
                    'severity': 'High',
                    'vuln_code': vuln_code,
                    'fix_code': fix_code
                })

        # 8. Check for insecure cookies
        cookies = response.cookies
        for cookie in cookies:
            issues = []
            if not cookie.secure:
                issues.append('Secure flag missing')
            if not cookie.has_nonstandard_attr('HttpOnly'):
                issues.append('HttpOnly flag missing')
            if issues:
                vuln_code, fix_code = get_fix("Insecure Cookies")
                result.append({
                    'type': 'Insecure Cookies',
                    'description': f'Cookie "{cookie.name}": {", ".join(issues)}.',
                    'severity': 'Medium',
                    'vuln_code': vuln_code,
                    'fix_code': fix_code
                })

        # 9. Check for server version disclosure
        server = resp_headers.get('Server', '')
        if server and re.search(r'\d+\.\d+', server):
            vuln_code, fix_code = get_fix("Server Version Exposed")
            result.append({
                'type': 'Server Version Exposed',
                'description': f'Server header exposes version: "{server}".',
                'severity': 'Low',
                'vuln_code': vuln_code,
                'fix_code': fix_code
            })

        # 10. Check for mixed content (HTTP resources on HTTPS page)
        if url.startswith('https'):
            http_resources = soup.find_all(src=re.compile(r'^http://'))
            http_links = soup.find_all(href=re.compile(r'^http://'))
            if http_resources or http_links:
                vuln_code, fix_code = get_fix("Mixed Content")
                result.append({
                    'type': 'Mixed Content',
                    'description': f'Found {len(http_resources) + len(http_links)} HTTP resource(s) loaded on HTTPS page.',
                    'severity': 'Low',
                    'vuln_code': vuln_code,
                    'fix_code': fix_code
                })

        # 11. Check for information disclosure in HTML comments
        comments = soup.find_all(string=lambda text: isinstance(text, type(soup.new_string(''))) and '<!--' in str(text) or (hasattr(text, 'string') and text.string and 'TODO' in text.string))
        html_comments = re.findall(r'<!--(.*?)-->', html, re.DOTALL)
        sensitive_patterns = ['password', 'api_key', 'secret', 'token', 'debug', 'TODO', 'FIXME', 'admin']
        for comment in html_comments:
            if any(p.lower() in comment.lower() for p in sensitive_patterns):
                vuln_code, fix_code = get_fix("Information Disclosure")
                result.append({
                    'type': 'Information Disclosure',
                    'description': 'Sensitive information found in HTML comments.',
                    'severity': 'Low',
                    'vuln_code': vuln_code,
                    'fix_code': fix_code
                })
                break

        if not result:
            result.append({
                'type': 'Secure',
                'description': 'No common vulnerabilities found. The site appears well-configured.',
                'severity': 'None',
                'vuln_code': '',
                'fix_code': ''
            })

    except requests.exceptions.Timeout:
        result.append({
            'type': 'Error',
            'description': 'Connection timed out. The website did not respond within 10 seconds.',
            'severity': 'N/A',
            'vuln_code': '',
            'fix_code': ''
        })
    except requests.exceptions.ConnectionError:
        result.append({
            'type': 'Error',
            'description': 'Could not connect to the website. Please check the URL.',
            'severity': 'N/A',
            'vuln_code': '',
            'fix_code': ''
        })
    except Exception as e:
        result.append({
            'type': 'Error',
            'description': str(e),
            'severity': 'N/A',
            'vuln_code': '',
            'fix_code': ''
        })

    return result


# Suppress InsecureRequestWarning for scanning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize database on startup
init_db()


# ---------- Auth Routes ----------

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
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('home'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---------- Main Routes ----------

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('home'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    vulnerabilities = []
    scanned_url = ''

    if request.method == 'POST':
        website = request.form.get('website', '').strip()
        if not website.startswith('http'):
            website = 'http://' + website
        scanned_url = website

        if is_valid_url(website):
            vulnerabilities = scan_website(website)
            # Save results to database
            conn = get_db()
            scan_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for v in vulnerabilities:
                if v['type'] != 'Error':
                    conn.execute(
                        "INSERT INTO scan_results (user_id, website, vulnerability, description, severity, scan_date) VALUES (?, ?, ?, ?, ?, ?)",
                        (session['user_id'], website, v['type'], v['description'], v['severity'], scan_date)
                    )
            conn.commit()
            conn.close()
        else:
            vulnerabilities = [{
                'type': 'Error',
                'description': 'Invalid URL provided. Please enter a valid URL.',
                'severity': 'N/A',
                'vuln_code': '',
                'fix_code': ''
            }]

    return render_template('home.html', vulnerabilities=vulnerabilities, scanned_url=scanned_url)


@app.route('/result')
def result():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    last_scan = conn.execute('''
        SELECT * FROM scan_results WHERE user_id = ? ORDER BY id DESC LIMIT 1
    ''', (session['user_id'],)).fetchone()
    # Get all results from the same scan (same scan_date)
    scan_results = []
    if last_scan:
        scan_results = conn.execute('''
            SELECT * FROM scan_results
            WHERE user_id = ? AND scan_date = ?
            ORDER BY id
        ''', (session['user_id'], last_scan['scan_date'])).fetchall()
    conn.close()
    return render_template('result.html', results=scan_results, fix_data=FIX_DATA)


@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    results = conn.execute('''
        SELECT * FROM scan_results WHERE user_id = ? ORDER BY id DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('history.html', results=results)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()

    # Current user stats
    user_results = conn.execute(
        "SELECT * FROM scan_results WHERE user_id = ?", (session['user_id'],)
    ).fetchall()

    # Vulnerability type distribution
    vuln_counts = {}
    for r in user_results:
        vtype = r['vulnerability']
        vuln_counts[vtype] = vuln_counts.get(vtype, 0) + 1

    # Severity distribution
    severity_counts = {}
    for r in user_results:
        sev = r['severity']
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    # Websites scanned
    site_counts = {}
    for r in user_results:
        site = r['website']
        site_counts[site] = site_counts.get(site, 0) + 1

    # Admin stats
    admin_stats = {}
    if session.get('role') == 'admin':
        admin_stats['total_users'] = conn.execute("SELECT COUNT(*) FROM users WHERE role='user'").fetchone()[0]
        admin_stats['total_scans'] = conn.execute("SELECT COUNT(*) FROM scan_results").fetchone()[0]
        admin_stats['unique_sites'] = conn.execute("SELECT COUNT(DISTINCT website) FROM scan_results").fetchone()[0]

    conn.close()

    return render_template('dashboard.html',
                           vuln_data=json.dumps(vuln_counts),
                           severity_data=json.dumps(severity_counts),
                           site_data=json.dumps(site_counts),
                           total_scans=len(user_results),
                           total_sites=len(site_counts),
                           admin_stats=admin_stats)


@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST' and session.get('user_id'):
        feedback_msg = request.form.get('feedback', '').strip()
        if feedback_msg:
            conn = get_db()
            conn.execute("INSERT INTO feedback (user_id, username, message) VALUES (?, ?, ?)",
                         (session['user_id'], session['username'], feedback_msg))
            conn.commit()
            conn.close()
            flash('Thank you for your feedback!', 'success')
        return redirect(url_for('about'))
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
