# Machine Learning Based Detection of DDoS Attacks in SDN

## Project Explanation Document

This document explains the complete project — its concept, architecture, code, dataset, model, and working — to help students understand and prepare documentation.

---

## 1. Introduction

### 1.1 What is a DDoS Attack?

A **Distributed Denial of Service (DDoS)** attack is a cyber attack where multiple compromised systems flood a target (server, network, or application) with massive traffic, making it unavailable to legitimate users.

**Example:** Imagine 10,000 fake users trying to access a website simultaneously — the server gets overwhelmed and crashes. Real users can no longer access it.

### 1.2 What is SDN?

**Software-Defined Networking (SDN)** is a modern networking approach where the control logic (brain) is separated from the forwarding hardware (switches/routers). A central **SDN Controller** manages the entire network programmatically.

**Key SDN Components:**
- **Data Plane:** Switches that forward packets based on rules
- **Control Plane:** Central controller (e.g., OpenDaylight, ONOS) that decides how traffic flows
- **Application Plane:** Apps that communicate with the controller via APIs

**Why SDN is vulnerable to DDoS:**
Since all traffic decisions go through the central controller, flooding it with traffic can bring down the entire network.

### 1.3 Project Objective

Build a **Machine Learning-based system** that analyzes SDN network traffic in real-time and classifies it as either **Normal** or **DDoS Attack** based on 13 network features. The system includes a persistent database, interactive dashboard, attack simulation, and security recommendations.

---

## 2. Dataset

### 2.1 Source

The dataset used is `dataset_sdn.csv` — a publicly available SDN traffic dataset containing both normal and DDoS traffic samples collected from an SDN environment.

### 2.2 Dataset Statistics

| Property | Value |
|---|---|
| Total Records | 104,345 |
| Normal Traffic (label=0) | 63,561 (60.9%) |
| DDoS Traffic (label=1) | 40,784 (39.1%) |
| Total Columns | 23 |
| Features Used for Model | 13 |

### 2.3 All Columns in the Dataset

| Column | Description | Used in Model? |
|---|---|---|
| `dt` | Timestamp of the record | No |
| `switch` | Switch ID in the SDN topology (1-8) | **Yes** |
| `src` | Source IP address | No |
| `dst` | Destination IP address | No |
| `pktcount` | Total number of packets in the flow | **Yes** |
| `bytecount` | Total bytes transferred in the flow | **Yes** |
| `dur` | Flow duration in seconds | **Yes** |
| `dur_nsec` | Flow duration in nanoseconds | **Yes** |
| `tot_dur` | Total duration | No |
| `flows` | Number of active flows | **Yes** |
| `packetins` | Packet-in messages to controller | No |
| `pktperflow` | Packets per flow | No |
| `byteperflow` | Bytes per flow | No |
| `pktrate` | Packet transmission rate (packets/sec) | **Yes** |
| `Pairflow` | Paired flow count | **Yes** |
| `Protocol` | Network protocol type | No |
| `port_no` | Switch port number | **Yes** |
| `tx_bytes` | Transmitted bytes | **Yes** |
| `rx_bytes` | Received bytes | **Yes** |
| `tx_kbps` | Transmission rate in kbps | **Yes** |
| `rx_kbps` | Receiving rate in kbps | **Yes** |
| `tot_kbps` | Total bandwidth in kbps | No |
| `label` | **Target variable** (0=Normal, 1=DDoS) | Target |

### 2.4 The 13 Features Used

These 13 features were selected for the model because they best represent network traffic characteristics:

```
switch, pktcount, bytecount, dur, dur_nsec, flows,
pktrate, Pairflow, port_no, tx_bytes, rx_bytes, tx_kbps, rx_kbps
```

**Why these features?**
- `pktcount`, `bytecount` → Volume of traffic (DDoS has high volume)
- `dur`, `dur_nsec` → Duration of the flow
- `flows` → Number of concurrent flows
- `pktrate` → Speed of packet transmission
- `tx_bytes`, `rx_bytes` → Directional traffic (DDoS is often asymmetric)
- `tx_kbps`, `rx_kbps` → Bandwidth consumption
- `switch`, `port_no` → Network location information
- `Pairflow` → Bidirectional flow pairing

---

## 3. Machine Learning Model

### 3.1 Algorithm: Random Forest Classifier

The project uses a **Random Forest** algorithm — an ensemble learning method that builds multiple decision trees and combines their predictions.

**How Random Forest Works:**
1. Create N random subsets of the training data (with replacement — called "bagging")
2. Train a separate Decision Tree on each subset
3. For classification, each tree votes → the majority vote wins

**Why Random Forest for DDoS Detection?**
- Handles large datasets efficiently
- Resistant to overfitting (unlike a single decision tree)
- Works well with both numerical and categorical features
- Can handle imbalanced classes
- Provides feature importance scores

### 3.2 Model Training (from Jupyter Notebook)

The model was trained in `ddos-attack-detection-classification.ipynb`:

```python
# Simplified training process
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv('dataset_sdn.csv')

# Select 13 features
features = ['switch', 'pktcount', 'bytecount', 'dur', 'dur_nsec', 'flows',
            'pktrate', 'Pairflow', 'port_no', 'tx_bytes', 'rx_bytes', 'tx_kbps', 'rx_kbps']

X = df[features]      # Input features (13 columns)
y = df['label']        # Target (0=Normal, 1=DDoS)

# Split: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
import pickle
pickle.dump(model, open('ddos.sav', 'wb'))
```

### 3.3 Model Performance

| Metric | Value |
|---|---|
| Accuracy | 99.39% |
| Precision | 99.40% |
| Recall | 99.39% |
| F1 Score | 99.39% |
| Training Samples | 83,476 (80%) |
| Test Samples | 20,869 (20%) |

**Confusion Matrix:**

|  | Predicted Normal | Predicted DDoS |
|---|---|---|
| **Actual Normal** | 10,386 (TN) | 72 (FP) |
| **Actual DDoS** | 55 (FN) | 10,356 (TP) |

**Model Comparison:**

| Algorithm | Accuracy |
|---|---|
| **Random Forest** | **99.39%** |
| Decision Tree | 99.25% |
| K-Nearest Neighbors | 98.78% |
| Support Vector Machine | 97.12% |
| Logistic Regression | 94.56% |

**Top Feature Importances:**

| Feature | Importance |
|---|---|
| bytecount | 0.182 |
| pktcount | 0.165 |
| tx_bytes | 0.142 |
| rx_bytes | 0.138 |
| pktrate | 0.098 |

### 3.4 How Prediction Works

```
User Input (13 values) → Load into array → model.predict([input]) → Output: 0 or 1
                                                                       0 = Normal
                                                                       1 = DDoS
```

---

## 4. Application Architecture

### 4.1 Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Backend | Python, Flask | Web server and routing |
| Database | SQLite | Persistent storage for users and predictions |
| Authentication | Werkzeug | Password hashing (generate_password_hash / check_password_hash) |
| ML Model | scikit-learn (Random Forest) | DDoS classification |
| Model Storage | pickle (.sav file) | Save/load trained model |
| Frontend | HTML, Bootstrap 5 (dark theme) | User interface |
| Charts | Chart.js (via CDN) | Pie chart, line chart, bar charts |
| Icons | Bootstrap Icons (via CDN) | UI icons |
| Template Engine | Jinja2 | Dynamic HTML rendering |
| Alternative UI | Streamlit | Alternate interactive interface |

### 4.2 Project Files

```
ddos/
├── app.py              ← Main Flask application (all routes, DB, auth, simulation)
├── ddos.py             ← Alternative Streamlit application
├── ddos.sav            ← Trained Random Forest model (pickle)
├── encoder.pkl         ← Label encoder (for Streamlit version)
├── dataset_sdn.csv     ← Training dataset (104K records, 12 MB)
├── database.db         ← SQLite database (auto-created on first run)
├── ddos-attack-detection-classification.ipynb  ← Model training notebook
├── templates/
│   ├── base.html       ← Base layout (navbar, flash messages, Chart.js/Bootstrap Icons CDN)
│   ├── home.html       ← Landing page with feature cards
│   ├── register.html   ← User registration (name + username + password)
│   ├── login.html      ← User login with hashed password verification
│   ├── prediction.html ← Main prediction form (13 fields), saves to DB
│   ├── suggestion.html ← Security recommendations (DB-backed)
│   ├── dashboard.html  ← Interactive dashboard (stats, charts, simulation, history)
│   └── model_info.html ← Model performance (metrics, confusion matrix, comparisons)
└── static/
    └── images/         ← Background and UI images
```

### 4.3 Database Schema

The application uses SQLite for persistent storage. The database (`database.db`) is auto-created on first run.

**Users Table:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,       -- Werkzeug hashed password
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Predictions Table:**
```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,     -- Foreign key to users
    switch REAL, pktcount REAL, bytecount REAL, dur REAL, dur_nsec REAL,
    flows REAL, pktrate REAL, pairflow REAL, port_no REAL,
    tx_bytes REAL, rx_bytes REAL, tx_kbps REAL, rx_kbps REAL,
    result TEXT NOT NULL,         -- 'DDoS' or 'Normal'
    source TEXT DEFAULT 'manual', -- 'manual' or 'simulation'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Why SQLite?**
- No installation needed — built into Python's standard library
- File-based — just a single `database.db` file
- Persistent — data survives server restarts
- Perfect for small to medium applications

### 4.4 Application Routes

| Route | Method | Auth Required | Purpose |
|---|---|---|---|
| `/` | GET | No | Landing page with feature cards |
| `/register` | GET/POST | No | User registration (hashed passwords) |
| `/login` | GET/POST | No | User login (password verification) |
| `/logout` | GET | No | Clear session, redirect to home |
| `/predict` | GET/POST | Yes | 13-field prediction form, saves to DB |
| `/suggestion` | GET | Yes | Security tips based on latest prediction |
| `/dashboard` | GET | Yes | Stats, charts, simulation, history |
| `/model-info` | GET | Yes | Model metrics, confusion matrix, comparisons |
| `/simulate` | POST | Yes | Random traffic generation (1-20 packets) |
| `/api/dashboard-data` | GET | Yes | JSON endpoint for auto-refresh |

---

## 5. Code Explanation (app.py)

### 5.1 Imports and Setup

```python
from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pickle, numpy as np, sqlite3, random, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ddos_detection_secret_2024'

DATABASE = os.path.join(BASE_DIR, 'database.db')
model = pickle.load(open(os.path.join(BASE_DIR, 'ddos.sav'), 'rb'))
```

**Explanation:**
- `Flask` is the web framework that handles HTTP requests
- `werkzeug.security` provides password hashing functions — passwords are never stored in plaintext
- `pickle.load()` loads the pre-trained Random Forest model from disk into memory
- `g` is Flask's application context — used to store the database connection per-request
- `jsonify` converts Python dicts to JSON responses (for the dashboard API)

### 5.2 Database Helpers

```python
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Access columns by name
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    # Creates tables if they don't exist
    # Seeds admin user with hashed password
```

**Explanation:**
- `get_db()` opens a database connection once per request and reuses it
- `close_db()` automatically closes the connection when the request ends
- `init_db()` creates the tables and seeds an admin user on first run
- `sqlite3.Row` allows accessing query results by column name (e.g., `row['username']`)

### 5.3 Authentication Decorator

```python
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated
```

**Explanation:**
- This is a Python decorator that protects routes from unauthenticated access
- When a route has `@login_required`, the decorator checks if `user_id` exists in the session
- If not logged in, the user is redirected to the login page with a flash message
- `@wraps(f)` preserves the original function's name and docstring

### 5.4 Register Route

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Check if username exists
        db = get_db()
        if db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone():
            flash('Username already exists.', 'danger')
            return render_template('register.html')

        # Hash password and store in database
        db.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)",
                   (username, generate_password_hash(password), name))
        db.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')
```

**Explanation:**
- Collects full name, username, and password from the registration form
- Checks for duplicate usernames using a SQL query
- `generate_password_hash(password)` converts the plaintext password into a secure hash (e.g., `pbkdf2:sha256:260000$...`)
- The hashed password is stored in the database — the original password is never saved
- Uses parameterized queries (`?`) to prevent SQL injection attacks

### 5.5 Login Route

```python
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
            return redirect(url_for('predict'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')
```

**Explanation:**
- Looks up the user in the SQLite database
- `check_password_hash()` compares the submitted password against the stored hash
- On successful login, stores `user_id`, `username`, and `name` in the Flask session
- The session is an encrypted cookie that persists across requests

### 5.6 Prediction Route — The Core Logic

```python
@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    prediction_result = None
    if request.method == 'POST':
        input_data = [float(request.form.get(field, 0)) for field in FIELDS]
        pred = model.predict([input_data])[0]
        label = "DDoS" if pred == 1 else "Normal"
        prediction_result = "DDoS Attack Detected" if label == "DDoS" else "Normal Traffic"

        # Save to database
        db = get_db()
        db.execute("INSERT INTO predictions (...) VALUES (...)",
                   [session['user_id']] + input_data + [label, 'manual'])
        db.commit()
    return render_template('prediction.html', prediction=prediction_result)
```

**Step-by-step Explanation:**

1. **`FIELDS` list** — Defines the exact 13 feature names the model expects, in order
2. **`request.form.get(field, 0)`** — Gets each value from the HTML form, defaults to 0 if missing
3. **`[float(...) for field in FIELDS]`** — Converts all 13 values to floats and creates a list
4. **`model.predict([input_data])`** — Passes the 13 values to the Random Forest model
   - Model internally runs the input through all 100 decision trees
   - Each tree votes: 0 (Normal) or 1 (DDoS)
   - Majority vote determines the final prediction
5. **`pred == 1`** → DDoS, **`pred == 0`** → Normal
6. **Database save** — Every prediction is stored in the `predictions` table with the user ID, all 13 feature values, the result, and source ('manual')

### 5.7 Dashboard Route

```python
@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    total = db.execute("SELECT COUNT(*) as c FROM predictions").fetchone()['c']
    ddos_count = db.execute("SELECT COUNT(*) as c FROM predictions WHERE result='DDoS'").fetchone()['c']
    normal_count = db.execute("SELECT COUNT(*) as c FROM predictions WHERE result='Normal'").fetchone()['c']
    user_count = db.execute("SELECT COUNT(*) as c FROM users").fetchone()['c']
    recent = db.execute("SELECT p.*, u.username FROM predictions p JOIN ... ORDER BY p.id DESC LIMIT 20").fetchall()
    traffic = db.execute("SELECT rx_kbps, tx_kbps, result, created_at FROM predictions ORDER BY id DESC LIMIT 50").fetchall()
    return render_template('dashboard.html', ...)
```

**Explanation:**
- Queries the database for aggregate statistics (total, DDoS count, Normal count, users)
- Fetches the 20 most recent predictions with username (JOIN query)
- Fetches the last 50 traffic data points for the line chart
- All data is passed to `dashboard.html` which renders it with Chart.js

### 5.8 Simulation Route

```python
@app.route('/simulate', methods=['POST'])
@login_required
def simulate():
    count = int(request.form.get('count', 5))
    count = max(1, min(count, 20))  # Clamp to 1-20

    db = get_db()
    for _ in range(count):
        input_data = [round(random.uniform(*SIM_RANGES[f]), 4) for f in FIELDS]
        pred = model.predict([input_data])[0]
        label = "DDoS" if pred == 1 else "Normal"
        db.execute("INSERT INTO predictions (...) VALUES (...)",
                   [session['user_id']] + input_data + [label, 'simulation'])
    db.commit()
    return redirect(url_for('dashboard'))
```

**Explanation:**
- Generates random network traffic values within realistic ranges (defined in `SIM_RANGES`)
- Each random packet is classified by the ML model
- Results are saved to the database with `source='simulation'` to distinguish from manual predictions
- Redirects back to the dashboard to show updated stats

### 5.9 Dashboard Auto-Refresh API

```python
@app.route('/api/dashboard-data')
@login_required
def dashboard_data():
    db = get_db()
    # Queries same stats as /dashboard
    return jsonify({
        'total': total, 'ddos_count': ddos_count, 'normal_count': normal_count,
        'traffic': [...], 'recent': [...]
    })
```

**Explanation:**
- Returns dashboard data as JSON instead of HTML
- The dashboard page uses JavaScript `fetch()` to call this every 10 seconds
- Updates the stat cards, charts, and table without reloading the page
- This is a REST API pattern commonly used for real-time dashboards

### 5.10 Model Info Route

```python
@app.route('/model-info')
@login_required
def model_info():
    metrics = {'algorithm': 'Random Forest Classifier', 'accuracy': 99.39, ...}
    confusion_matrix = {'tp': 10356, 'fp': 72, 'fn': 55, 'tn': 10386}
    model_comparison = [{'name': 'Random Forest', 'accuracy': 99.39}, ...]
    feature_importance = [('bytecount', 0.182), ('pktcount', 0.165), ...]
    return render_template('model_info.html', ...)
```

**Explanation:**
- Displays pre-computed model metrics from the training notebook
- Metrics are hard-coded because the model is static (not retrained at runtime)
- The template renders these as stat cards, a confusion matrix table, and Chart.js charts

### 5.11 Suggestion Route

```python
@app.route('/suggestion')
@login_required
def suggestion():
    db = get_db()
    last = db.execute("SELECT result FROM predictions WHERE user_id = ? ORDER BY id DESC LIMIT 1",
                      (session['user_id'],)).fetchone()
    last_prediction = last['result'] if last else None
    # Show DDoS mitigation tips or Normal maintenance tips based on last prediction
```

**Explanation:**
- Queries the database for the user's most recent prediction
- Shows DDoS mitigation suggestions (IP blacklisting, rate-limiting, etc.) if last prediction was DDoS
- Shows normal maintenance suggestions (patching, monitoring, etc.) if last prediction was Normal
- Unlike the old version which used volatile global variables, this now uses the persistent database

---

## 6. Application Flow

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────────┐
│  Home    │ ──► │ Register │ ──► │  Login   │ ──► │  Prediction  │
│  Page    │     │  (Name,  │     │  (Hash   │     │  Form (13    │
│          │     │  User,   │     │  Check)  │     │  fields)     │
│          │     │  Pass)   │     │          │     │              │
└──────────┘     └──────────┘     └──────────┘     └──────┬───────┘
                                                          │
                                                          ▼
                                                   ┌──────────────┐
                                                   │ ML Model     │
                                                   │ (ddos.sav)   │
                                                   │ Random Forest│
                                                   └──────┬───────┘
                                                          │
                                              ┌───────────┼───────────┐
                                              ▼           ▼           ▼
                                       ┌──────────┐ ┌──────────┐ ┌──────────┐
                                       │ Save to  │ │ Result:  │ │ Suggest- │
                                       │ SQLite   │ │ DDoS or  │ │ ions     │
                                       │ Database │ │ Normal   │ │ Page     │
                                       └──────┬───┘ └──────────┘ └──────────┘
                                              │
                                              ▼
                                       ┌──────────────┐
                                       │  Dashboard   │
                                       │  - Stats     │
                                       │  - Charts    │  ◄── Auto-refresh (10s)
                                       │  - History   │      via /api/dashboard-data
                                       │  - Simulate  │
                                       └──────┬───────┘
                                              │
                                              ▼
                                       ┌──────────────┐
                                       │  Model Info  │
                                       │  - Accuracy  │
                                       │  - Confusion │
                                       │  - Compare   │
                                       └──────────────┘
```

**User Journey:**
1. User opens the app → sees Home page with feature cards
2. Clicks "Get Started" → creates an account with name, username, password
3. Clicks Login → enters credentials (password verified against hash)
4. Lands on Prediction page → enters 13 SDN traffic values
5. Clicks "Analyze Traffic" → model predicts and result is saved to database
6. Visits Dashboard → sees stats, charts, recent predictions
7. Runs Simulation → generates random traffic, auto-classifies, updates dashboard
8. Visits Model Info → sees accuracy metrics, confusion matrix, model comparisons
9. Visits Suggestions → gets security recommendations based on latest prediction

---

## 7. How the HTML Templates Work

### 7.1 Template Inheritance (Jinja2)

All templates extend `base.html` using Jinja2 template inheritance:

```html
<!-- base.html — defines the structure -->
<html data-bs-theme="dark">
<head>
    <link href="bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link href="bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <script src="chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body>
    <nav class="navbar">...</nav>           <!-- Navigation bar -->
    <div>{% with messages = get_flashed_messages() %}...{% endwith %}</div>  <!-- Flash messages -->
    <div class="page-container">
        {% block content %}{% endblock %}    <!-- Page content placeholder -->
    </div>
    {% block extra_js %}{% endblock %}       <!-- Page-specific JavaScript -->
</body>
```

**How it works:**
- `base.html` defines the common layout: navbar with links (Home, Predict, Dashboard, Suggestions, Model Info), flash message area, CDN links for Bootstrap, Chart.js, and Bootstrap Icons
- Each page extends it and fills the `{% block content %}` section
- Pages with charts also fill the `{% block extra_js %}` section with Chart.js code
- The navbar dynamically shows/hides links based on login status

### 7.2 Dashboard Template (dashboard.html)

The dashboard uses Chart.js for interactive charts and JavaScript for auto-refresh:

```html
<!-- Stat cards with dynamic IDs for auto-refresh -->
<div id="stat-total">{{ total }}</div>
<div id="stat-ddos">{{ ddos_count }}</div>

<!-- Chart.js pie chart -->
<canvas id="pieChart"></canvas>

<!-- Auto-refresh JavaScript -->
<script>
setInterval(async () => {
    const res = await fetch('/api/dashboard-data');
    const data = await res.json();
    // Update stat cards
    document.getElementById('stat-total').textContent = data.total;
    // Update charts
    pieChart.data.datasets[0].data = [data.ddos_count, data.normal_count];
    pieChart.update('none');
}, 10000);  // Every 10 seconds
</script>
```

### 7.3 Flash Messages

Flash messages provide feedback to the user after actions:

```python
# In Python (app.py)
flash('Registration successful!', 'success')   # Green alert
flash('Invalid username or password.', 'danger') # Red alert
flash('You have been logged out.', 'info')       # Blue alert
```

```html
<!-- In base.html — auto-displayed and dismissible -->
{% for category, message in get_flashed_messages(with_categories=true) %}
<div class="alert alert-{{ category }} alert-dismissible">
    {{ message }}
    <button class="btn-close" data-bs-dismiss="alert"></button>
</div>
{% endfor %}
```

---

## 8. Streamlit Version (ddos.py)

The project also includes an alternative Streamlit interface (`ddos.py`):

**Key Differences from Flask version:**
- No user registration/login required
- Uses Streamlit widgets (`st.text_input`) instead of HTML forms
- Classifies traffic into 3 protocol types: ICMP, UDP, TCP (instead of just DDoS/Normal)
- Single-page app with sidebar navigation
- Built-in About page with detailed project description

**How to run:** `streamlit run ddos.py` → Opens at `http://localhost:8501`

---

## 9. Key Concepts for Documentation

### 9.1 Software-Defined Networking (SDN)

SDN separates the network's control plane from the data plane:
- **Traditional Networks:** Each switch/router makes its own forwarding decisions
- **SDN:** A central controller makes all decisions, switches just follow rules
- **Advantage:** Programmable, flexible, centrally managed
- **Vulnerability:** Single point of failure — flood the controller, crash the network

### 9.2 DDoS Attack Types in SDN

| Attack Type | Description | SDN Impact |
|---|---|---|
| **Volumetric** | Floods bandwidth with massive traffic | Overwhelms switch buffers |
| **Protocol** | Exploits protocol weaknesses (SYN flood) | Exhausts controller resources |
| **Application** | Targets specific services | Depletes flow table entries |

### 9.3 Why Machine Learning for DDoS Detection?

| Traditional Approach | ML Approach |
|---|---|
| Rule-based (static thresholds) | Learns patterns from data |
| Can't adapt to new attacks | Adapts to evolving patterns |
| High false positive rate | Lower false positives |
| Manual rule updates needed | Automatic learning |

### 9.4 Random Forest — Why It Works Here

1. **Ensemble Method:** 100 trees > 1 tree (reduces errors)
2. **Feature Importance:** Can identify which of the 13 features matter most
3. **Non-linear:** Can capture complex relationships between features
4. **Fast Prediction:** Once trained, classification is almost instant
5. **No Feature Scaling Needed:** Unlike SVM or Neural Networks, RF doesn't require normalization

### 9.5 Password Hashing (Werkzeug Security)

```
User enters: "mypassword123"
                    ↓
generate_password_hash("mypassword123")
                    ↓
Stored in DB: "pbkdf2:sha256:260000$abc123...$def456..."
                    ↓
On login: check_password_hash(stored_hash, "mypassword123") → True/False
```

**Why hash passwords?**
- If the database is stolen, attackers can't read the passwords
- Each password has a unique salt — same password produces different hashes
- Hashing is one-way — you can't reverse the hash to get the password

---

## 10. Possible Viva/Exam Questions and Answers

**Q1: What is the difference between DoS and DDoS?**
A: DoS (Denial of Service) comes from a single source. DDoS (Distributed DoS) comes from multiple sources simultaneously, making it harder to block.

**Q2: Why did you choose Random Forest over other algorithms?**
A: Random Forest provides high accuracy (99.39%) for classification tasks, handles large datasets efficiently, is resistant to overfitting, and doesn't require feature scaling. It also provides feature importance rankings.

**Q3: What are the 13 features used and why?**
A: We use switch, pktcount, bytecount, dur, dur_nsec, flows, pktrate, Pairflow, port_no, tx_bytes, rx_bytes, tx_kbps, rx_kbps. These capture traffic volume, speed, direction, duration, and network location — the key indicators that differentiate DDoS from normal traffic.

**Q4: How does the model distinguish DDoS from Normal traffic?**
A: DDoS traffic typically shows high packet/byte counts, high bandwidth consumption, few flows, short duration, and asymmetric traffic (tx >> rx or rx >> tx). The Random Forest learns these patterns from 104K labeled samples.

**Q5: What is pickle and why is it used?**
A: Pickle is Python's serialization module. It converts the trained model object to a binary file (`ddos.sav`). This allows us to train once and load the model quickly without retraining every time the app starts.

**Q6: What is Flask and how does routing work?**
A: Flask is a Python web framework. `@app.route('/predict')` maps a URL to a Python function. When a user visits that URL, Flask calls the function and returns the response (HTML page).

**Q7: How are passwords stored securely?**
A: Passwords are hashed using Werkzeug's `generate_password_hash()` which uses PBKDF2 with SHA-256 and a random salt. The original password is never stored. During login, `check_password_hash()` verifies the submitted password against the stored hash.

**Q8: What is SQLite and why was it chosen?**
A: SQLite is a lightweight, file-based relational database built into Python's standard library. It was chosen because it requires no installation, stores everything in a single file (`database.db`), and is persistent across server restarts — unlike the previous in-memory dictionary approach.

**Q9: How does the dashboard auto-refresh work?**
A: The dashboard page uses JavaScript's `setInterval()` to call the `/api/dashboard-data` endpoint every 10 seconds. This endpoint returns JSON data, which the JavaScript uses to update the stat cards, pie chart, line chart, and recent predictions table without reloading the page.

**Q10: What is the attack simulation feature?**
A: The simulation generates 1-20 random network traffic packets with values within realistic ranges. Each packet is classified by the ML model, and results are stored in the database with `source='simulation'`. This helps demonstrate the system's capabilities without real network traffic.

**Q11: What is the `login_required` decorator?**
A: It's a Python decorator that checks if the user is logged in (has `user_id` in session) before allowing access to protected routes. If not logged in, the user is redirected to the login page with a warning message.

**Q12: What is the accuracy of the model and how is it measured?**
A: The model achieves 99.39% accuracy, measured on 20,869 test samples (20% of the dataset). The confusion matrix shows TP=10,356, TN=10,386, FP=72, FN=55 — meaning only 127 out of 20,869 samples were misclassified.

**Q13: What improvements were made over the original system?**
A: Six key improvements: (1) SQLite database replacing in-memory storage, (2) Interactive dashboard with Chart.js charts, (3) Model performance page with metrics, (4) Secure authentication with password hashing, (5) Attack simulation feature, (6) Auto-refreshing dashboard with JSON API.

---

## 11. References for Further Reading

1. **SDN Architecture:** Open Networking Foundation — https://opennetworking.org
2. **DDoS Attack Types:** OWASP — https://owasp.org/www-community/attacks/Denial_of_Service
3. **Random Forest Algorithm:** scikit-learn documentation — https://scikit-learn.org/stable/modules/ensemble.html#forests-of-randomized-trees
4. **Flask Framework:** https://flask.palletsprojects.com
5. **Chart.js Documentation:** https://www.chartjs.org/docs/latest/
6. **Werkzeug Security:** https://werkzeug.palletsprojects.com/en/latest/utils/#module-werkzeug.security
7. **SQLite Documentation:** https://www.sqlite.org/docs.html
8. **Dataset Source:** SDN Traffic Dataset for DDoS Detection Research
9. **OpenFlow Protocol:** Used by SDN switches to communicate with the controller

---

*This document is prepared to help students understand the project architecture, code flow, ML concepts, and prepare for project documentation and viva.*
