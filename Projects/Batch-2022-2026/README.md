# B10 — Machine Learning Based Detection of DDoS Attacks in SDN

## Project Structure

```
ddos/
├── app.py                          # Main Flask-SocketIO application (routes, DB, auth, WebSocket)
├── ddos.py                         # Streamlit application (alternative UI)
├── ddos.sav                        # Pre-trained Random Forest classifier (2.1 MB)
├── encoder.pkl                     # Label encoder
├── dataset_sdn.csv                 # SDN traffic dataset (12 MB, can be uploaded via dashboard)
├── requirements.txt                # Python dependencies
├── ddos-attack-detection-classification.ipynb  # Jupyter notebook (model training)
├── database.db                     # SQLite database (auto-created on first run)
├── uploads/                        # Temporary storage for uploaded CSV files (auto-created)
├── .gitignore                      # Git ignore rules
├── download.jpg                    # Project image
├── download 1.jpg                  # Project image
├── static/
│   └── images/
│       ├── background.jpeg         # Background image
│       ├── images (12).jpeg        # UI image
│       └── images (13).jpeg        # UI image
└── templates/
    ├── base.html                   # Base layout (navbar, Chart.js + Socket.IO CDN)
    ├── home.html                   # Landing page with feature cards
    ├── login.html                  # Login page (hashed password auth)
    ├── register.html               # Registration page (with full name field)
    ├── prediction.html             # Prediction form (13 SDN features)
    ├── suggestion.html             # Security suggestions (DB-backed)
    ├── dashboard.html              # Live dashboard (charts, 3 data inputs, WebSocket)
    └── model_info.html             # Model performance metrics and charts
```

## Features

- **ML-Powered DDoS Detection** — Random Forest classifier with 99.39% accuracy on 104K+ samples
- **SQLite Database** — Persistent storage for users and prediction history
- **Secure Authentication** — Password hashing with Werkzeug, session-based login, `login_required` decorator
- **Interactive Dashboard** — Real-time stat cards, pie chart (attack distribution), line chart (traffic over time), recent predictions table
- **3 Data Input Methods** (tabbed interface on dashboard):
  1. **CSV Upload** — Upload your own CSV file with SDN flow data; rows are processed one-by-one through the ML model with configurable speed (0.25s–2s/row) and live progress via WebSocket
  2. **API Push** — External systems POST JSON to `/api/predict` (single) or `/api/predict/batch` (up to 100 records); authenticated via `X-API-Key` header
  3. **Endpoint Poller** — System polls an external URL at configurable intervals (1s–30s), fetches JSON flow data, and classifies each record live
- **WebSocket Dashboard** — Instant live updates via Flask-SocketIO — stat cards, charts, and tables update in real-time as predictions arrive (no page reload, no polling delay)
- **Attack Simulation** — Generate 1-20 random network packets, auto-classify and store results
- **Model Performance Page** — Accuracy metrics, confusion matrix, model comparison chart, feature importance chart
- **Security Suggestions** — Actionable recommendations based on latest prediction from database

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps (Windows)

**Step 1:** Open Command Prompt and navigate to project

```bash
cd ddos
```

**Step 2:** Install required packages

```bash
pip install flask numpy scikit-learn flask-socketio requests
```

**Step 3:** Run the Flask application

```bash
python app.py
```

**Step 4:** Open in browser

```
http://127.0.0.1:5021
```

### Alternative: Run Streamlit version

```bash
pip install streamlit streamlit-option-menu
streamlit run ddos.py
```

Opens at `http://localhost:8501`

## First Time Usage

1. Open http://127.0.0.1:5021 — you'll see the **Home** page with feature cards
2. Click **Get Started** → create an account with full name, username, and password
3. Click **Login** → enter your credentials
4. You'll land on the **Prediction** page with 13 SDN traffic input fields
5. Fill in the values and click **Analyze Traffic**
6. View the result (DDoS Attack Detected / Normal Traffic) — saved to database
7. Visit **Dashboard** → see stats, charts, and recent prediction history
8. Use the **CSV Upload** tab to upload a CSV file with SDN data and watch live row-by-row analysis
9. Use the **API Push** tab to see how external systems can send data via REST API
10. Use the **Endpoint Poller** tab to pull data from an external URL at regular intervals
11. Use the **Quick Simulation** panel to generate random traffic packets (1-20)
12. Visit **Model Info** → see accuracy metrics, confusion matrix, model comparison
13. Click **Suggestions** → get security recommendations based on your latest prediction

**Default Admin Account:** Username: `admin`, Password: `admin123` (auto-created on first run)

## Application Routes

| Route | Method | Auth | Purpose |
|---|---|---|---|
| `/` | GET | No | Landing page with feature cards |
| `/register` | GET/POST | No | User registration (hashed passwords, SQLite) |
| `/login` | GET/POST | No | User login (password verification) |
| `/logout` | GET | No | Clear session and redirect |
| `/predict` | GET/POST | Yes | 13-field prediction form, saves to DB |
| `/suggestion` | GET | Yes | Security tips based on latest DB prediction |
| `/dashboard` | GET | Yes | Stats, charts, 3 data input tabs, simulation, history |
| `/model-info` | GET | Yes | Model accuracy, confusion matrix, comparisons |
| `/simulate` | POST | Yes | Random traffic generation (1-20 samples) |
| `/upload-csv` | POST | Yes | Upload CSV file for row-by-row analysis (AJAX) |
| `/stop-csv` | POST | Yes | Stop an active CSV processing task |
| `/start-poller` | POST | Yes | Start polling an external URL for flow data (AJAX) |
| `/stop-poller` | POST | Yes | Stop an active endpoint poller |
| `/api/predict` | POST | API Key | Single prediction from external system (JSON) |
| `/api/predict/batch` | POST | API Key | Batch prediction — up to 100 records (JSON) |
| `/api/dashboard-data` | GET | Yes | JSON endpoint for manual refresh fallback |

## Database Schema

```sql
users (id, username UNIQUE, password [hashed], name, created_at)
predictions (id, user_id FK, switch, pktcount, bytecount, dur, dur_nsec, flows,
             pktrate, pairflow, port_no, tx_bytes, rx_bytes, tx_kbps, rx_kbps,
             result, source ['manual'|'simulation'|'csv'|'api'|'poller'], created_at)
```

## Notes

- User accounts and predictions are stored in SQLite (`database.db`) — persistent across restarts
- The database is auto-created on first run with an admin user seeded
- The model was trained using Random Forest on the `dataset_sdn.csv` dataset
- The model classifies SDN traffic into **DDoS** or **Normal** based on 13 network features
- Dashboard updates in real-time via WebSocket (Flask-SocketIO) — no page reload needed
- CSV Upload, API Push, and Endpoint Poller all use AJAX — the page stays live during processing
- Uploaded CSV files are auto-deleted after processing completes
- API endpoints use `X-API-Key: sdn_monitor_2024` for authentication
- A sklearn version warning may appear — this is harmless and does not affect results

## SDN Feature Descriptions

| Field | Description |
|---|---|
| switch | Switch ID in the SDN topology |
| pktcount | Total packet count observed |
| bytecount | Total byte count of traffic |
| dur | Duration of the flow (seconds) |
| dur_nsec | Duration in nanoseconds |
| flows | Number of active flows |
| pktrate | Packet rate (packets/second) |
| Pairflow | Pair flow count |
| port_no | Port number of the switch |
| tx_bytes | Transmitted bytes |
| rx_bytes | Received bytes |
| tx_kbps | Transmission rate (kbps) |
| rx_kbps | Receiving rate (kbps) |

---

## Test Cases

### Test Case 1: DDoS Attack Detection

| Field | Value |
|---|---|
| switch | 1 |
| pktcount | 4777 |
| bytecount | 5092282 |
| dur | 10 |
| dur_nsec | 711000000 |
| flows | 3 |
| pktrate | 0 |
| Pairflow | 0 |
| port_no | 2 |
| tx_bytes | 3753 |
| rx_bytes | 1332 |
| tx_kbps | 0 |
| rx_kbps | 0 |

**Expected Result:** DDoS Attack Detected

**Why:** High byte count (~5M) relative to short duration (10 sec) with only 3 flows and zero packet rate/bandwidth metrics — characteristic of a volumetric DDoS flood in SDN.

---

### Test Case 2: Normal Traffic

| Field | Value |
|---|---|
| switch | 1 |
| pktcount | 45304 |
| bytecount | 48294064 |
| dur | 100 |
| dur_nsec | 716000000 |
| flows | 3 |
| pktrate | 451 |
| Pairflow | 0 |
| port_no | 3 |
| tx_bytes | 143928631 |
| rx_bytes | 3917 |
| tx_kbps | 0 |
| rx_kbps | 0 |

**Expected Result:** Normal Traffic

**Why:** Sustained packet rate (451) over a longer duration (100 sec) with high tx_bytes — indicates legitimate bulk data transfer, not an attack pattern.

---

### Test Case 3: DDoS Attack (Multiple Switches)

| Field | Value |
|---|---|
| switch | 7 |
| pktcount | 12146 |
| bytecount | 12947636 |
| dur | 27 |
| dur_nsec | 249000000 |
| flows | 2 |
| pktrate | 0 |
| Pairflow | 0 |
| port_no | 3 |
| tx_bytes | 3185 |
| rx_bytes | 3059 |
| tx_kbps | 0 |
| rx_kbps | 0 |

**Expected Result:** DDoS Attack Detected

**Why:** High byte count (~13M) with only 2 flows, zero pktrate and zero bandwidth on switch 7 — pattern consistent with DDoS traffic in the SDN topology.

---

### Test Case 4: Normal Traffic (Different Switch)

| Field | Value |
|---|---|
| switch | 4 |
| pktcount | 19138 |
| bytecount | 20401108 |
| dur | 41 |
| dur_nsec | 852000000 |
| flows | 2 |
| pktrate | 446 |
| Pairflow | 0 |
| port_no | 4 |
| tx_bytes | 2882 |
| rx_bytes | 2924 |
| tx_kbps | 0 |
| rx_kbps | 0 |

**Expected Result:** Normal Traffic

**Why:** Active packet rate (446) with balanced tx/rx bytes and moderate duration (41 sec) — matches normal SDN traffic pattern.

---

### Test Case 5: DDoS Attack (High Volume)

| Field | Value |
|---|---|
| switch | 1 |
| pktcount | 130634 |
| bytecount | 135522132 |
| dur | 650 |
| dur_nsec | 95000000 |
| flows | 3 |
| pktrate | 0 |
| Pairflow | 1 |
| port_no | 1 |
| tx_bytes | 135529018 |
| rx_bytes | 65390 |
| tx_kbps | 0 |
| rx_kbps | 0 |

**Expected Result:** DDoS Attack Detected

**Why:** Extremely high packet count (130K+) and byte count (135M) with heavily asymmetric traffic (tx >> rx) — classic DDoS pattern with massive one-way data flow.

---

### Test Case 6: Dashboard, Data Input Methods & Simulation

1. After making predictions (Test Cases 1-5), visit **Dashboard** (`/dashboard`)
2. You should see:
   - **Stat cards** showing total predictions, DDoS count, Normal count, user count
   - **Pie chart** showing attack distribution (DDoS vs Normal)
   - **Line chart** showing rx_kbps traffic over time with color-coded points
   - **Recent predictions table** with user, result, source, timestamps
3. **CSV Upload tab** — upload `dataset_sdn.csv`, set 20 rows at 1s speed, click "Upload & Analyze"
   - Watch row-by-row progress bar, live stat/chart updates via WebSocket
   - Click "Stop" mid-way to test graceful stop
4. **API Push tab** — shows curl and Python examples for external integration
   - Test with: `curl -X POST http://127.0.0.1:5021/api/predict -H "Content-Type: application/json" -H "X-API-Key: sdn_monitor_2024" -d '{"switch":1,"pktcount":4777,"bytecount":5092282,"dur":10,"dur_nsec":711000000,"flows":3,"pktrate":0,"Pairflow":0,"port_no":2,"tx_bytes":3753,"rx_bytes":1332,"tx_kbps":0,"rx_kbps":0}'`
   - Dashboard updates instantly after each API call
5. **Endpoint Poller tab** — enter an external URL, set interval and max polls
6. Use the **Quick Simulation** panel — enter 5 and click "Run Simulation"
7. All updates happen live via WebSocket — no page reload needed

### Test Case 7: Model Info Page

1. Visit **Model Info** (`/model-info`)
2. You should see:
   - Accuracy: 99.39%, Precision: 99.40%, Recall: 99.39%, F1: 99.39%
   - Confusion matrix: TP=10356, TN=10386, FP=72, FN=55
   - Model comparison bar chart (Random Forest vs 4 other models)
   - Feature importance chart (bytecount, pktcount, tx_bytes as top features)

### Test Case 8: Suggestions Based on DB

1. After running DDoS test cases (1, 3, 5), visit **Suggestions**
2. You should see DDoS mitigation recommendations (red alerts)
3. After running Normal test cases (2, 4), visit **Suggestions** again
4. The suggestions now reflect the most recent prediction from the database

---

### Test Case 9: API Push — Single Prediction (DDoS)

Run from terminal while the app is running:

```bash
curl -X POST http://127.0.0.1:5021/api/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sdn_monitor_2024" \
  -d '{
    "switch": 1, "pktcount": 4777, "bytecount": 5092282,
    "dur": 10, "dur_nsec": 711000000, "flows": 3,
    "pktrate": 0, "Pairflow": 0, "port_no": 2,
    "tx_bytes": 3753, "rx_bytes": 1332,
    "tx_kbps": 0, "rx_kbps": 0
  }'
```

**Expected Response:**
```json
{"result": "DDoS", "description": "DDoS Attack Detected", "features": {...}}
```

**Why DDoS:** High bytecount (5M) in short duration (10s) with zero pktrate — classic volumetric flood.

---

### Test Case 10: API Push — Single Prediction (Normal)

```bash
curl -X POST http://127.0.0.1:5021/api/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sdn_monitor_2024" \
  -d '{
    "switch": 1, "pktcount": 45304, "bytecount": 48294064,
    "dur": 100, "dur_nsec": 716000000, "flows": 3,
    "pktrate": 451, "Pairflow": 0, "port_no": 3,
    "tx_bytes": 143928631, "rx_bytes": 3917,
    "tx_kbps": 0, "rx_kbps": 0
  }'
```

**Expected Response:**
```json
{"result": "Normal", "description": "Normal Traffic", "features": {...}}
```

**Why Normal:** Active pktrate (451 packets/sec) over longer duration (100s) — steady legitimate traffic.

---

### Test Case 11: API Push — Batch Prediction

```bash
curl -X POST http://127.0.0.1:5021/api/predict/batch \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sdn_monitor_2024" \
  -d '{
    "records": [
      {"switch":1,"pktcount":4777,"bytecount":5092282,"dur":10,"dur_nsec":711000000,"flows":3,"pktrate":0,"Pairflow":0,"port_no":2,"tx_bytes":3753,"rx_bytes":1332,"tx_kbps":0,"rx_kbps":0},
      {"switch":1,"pktcount":45304,"bytecount":48294064,"dur":100,"dur_nsec":716000000,"flows":3,"pktrate":451,"Pairflow":0,"port_no":3,"tx_bytes":143928631,"rx_bytes":3917,"tx_kbps":0,"rx_kbps":0},
      {"switch":7,"pktcount":12146,"bytecount":12947636,"dur":27,"dur_nsec":249000000,"flows":2,"pktrate":0,"Pairflow":0,"port_no":3,"tx_bytes":3185,"rx_bytes":3059,"tx_kbps":0,"rx_kbps":0}
    ]
  }'
```

**Expected Response:**
```json
{"total": 3, "ddos_count": 2, "normal_count": 1, "results": [
  {"index": 0, "result": "DDoS"},
  {"index": 1, "result": "Normal"},
  {"index": 2, "result": "DDoS"}
]}
```

**Verify:** Dashboard stat cards, pie chart, and recent table all update instantly after the batch call.

---

### Test Case 12: API Push — Invalid API Key

```bash
curl -X POST http://127.0.0.1:5021/api/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: wrong_key" \
  -d '{"switch":1,"pktcount":100,"bytecount":1000,"dur":5,"dur_nsec":500000,"flows":1,"pktrate":20,"Pairflow":0,"port_no":1,"tx_bytes":500,"rx_bytes":500,"tx_kbps":1,"rx_kbps":1}'
```

**Expected Response:**
```json
{"error": "Invalid or missing API key. Pass X-API-Key header."}
```
**HTTP Status:** 401

---

### Test Case 13: API Push — Missing Fields

```bash
curl -X POST http://127.0.0.1:5021/api/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sdn_monitor_2024" \
  -d '{"switch": 1, "pktcount": 100}'
```

**Expected Response:**
```json
{"error": "Missing fields: bytecount, dur, dur_nsec, flows, pktrate, Pairflow, port_no, tx_bytes, rx_bytes, tx_kbps, rx_kbps", "required_fields": [...]}
```
**HTTP Status:** 400

---

## Key Indicators

The model was trained on real SDN traffic data (`dataset_sdn.csv`) with 13 network features. The Random Forest classifier learns complex feature interactions — predictions depend on the combination of all 13 values, not individual thresholds. Use the test case values above for reliable results.
