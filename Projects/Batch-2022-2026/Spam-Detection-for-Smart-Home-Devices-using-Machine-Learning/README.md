# Spam Detection for Smart Home Devices Using Machine Learning

A production-grade machine learning system that detects spam and malicious behavior in IoT smart home devices. The application uses a Flask REST API backend with JWT authentication, SQLite database, structured logging, and 5 ML classification algorithms with a Deep Learning Neural Network. A modern Next.js frontend provides a full-featured dashboard with real-time predictions.

---

## Features

### Admin Panel
- **Dataset Upload** — Upload IoT device CSV datasets; tracked in database with row count and version history
- **Compare Algorithms** — Evaluate 5 ML models with accuracy, precision, recall, and F1-score metrics + learning curve charts
- **Create Model** — Train a Deep Learning Neural Network (Keras) with accuracy and loss visualization; model versions saved to DB
- **Dashboard** — View total predictions, active model version and accuracy, active dataset info

### User Panel
- **Spam Prediction** — Input 10 PCA-transformed parameters to detect spam/valid device behavior
- **Prediction History** — Paginated log of all previous predictions stored in database
- **Bulk Ingest** — Submit multiple records for batch prediction via:
  - CSV file upload (up to 5,000 rows) — returns JSON or downloadable CSV with predictions appended
  - Single JSON record
  - Batch JSON array (up to 1,000 records)

### REST API (Data Ingestion)
All endpoints return a consistent `{"status": "success"|"error", "data": {...}}` envelope.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `POST /api/admin/login` | POST | Admin login, returns JWT |
| `POST /api/user/login` | POST | User login, returns JWT |
| `POST /api/admin/upload` | POST | Upload dataset CSV |
| `GET /api/admin/compare-algorithms` | GET | Train + compare 5 ML models |
| `POST /api/admin/create-model` | POST | Train deep learning model |
| `GET /api/admin/dashboard` | GET | Summary stats |
| `POST /api/user/predict` | POST | Single record prediction |
| `GET /api/user/predictions` | GET | Prediction history (paginated) |
| `POST /api/ingest` | POST | Single JSON record ingestion |
| `POST /api/ingest/batch` | POST | Batch JSON records (up to 1,000) |
| `POST /api/ingest/csv` | POST | CSV file ingestion (up to 5,000 rows) |
| `GET /health` | GET | Health check (DB + model status) |

### ML Algorithms Compared
| # | Algorithm | Description |
|---|-----------|-------------|
| 1 | Bagging Classifier | Ensemble with SVC base estimator (10 estimators) |
| 2 | Gaussian Naive Bayes | Probabilistic classifier using Bayes theorem |
| 3 | AdaBoost | Boosting ensemble (100 estimators) |
| 4 | Voting Classifier | Combines Logistic Regression, Random Forest, Gaussian NB |
| 5 | Decision Tree | Gini criterion-based tree classifier |

### Deep Learning Model
- **Architecture:** Input(10) → Dense(4, ReLU) → Dense(4, ReLU) → Dense(1, Sigmoid)
- **Optimizer:** Adam | **Loss:** Binary Cross-Entropy | **Training:** 200 epochs, 80/20 split

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.11, Flask 3.0 (App Factory pattern) |
| REST API | Flask-JWT-Extended (JWT auth), Flask-CORS |
| Database | SQLite via Flask-SQLAlchemy + Flask-Migrate |
| ML/DL | TensorFlow 2.13, Keras, scikit-learn 1.3 |
| Data Processing | pandas, NumPy, PCA (10 components) |
| Visualization | Matplotlib (learning curves, accuracy/loss plots) |
| Logging | Python `logging` + rotating file handler (JSON in prod) |
| Frontend (Classic) | Flask Templates (HTML/CSS) |
| Frontend (Modern) | Next.js 14, TypeScript, Tailwind CSS, Recharts |
| Auth (Frontend) | JWT stored in sessionStorage, Axios interceptors |

---

## Dataset

The application uses an **IoT Smart Home REFIT dataset**:
- **1,664 records** of smart home device interactions
- **13 features:** sourceID, sourceAddress, sourceType, sourceLocation, destinationServiceAddress, destinationServiceType, destinationLocation, accessedNodeAddress, accessedNodeType, operation, value, timestamp, normality
- **Labels:** `normal` or `spam`
- **Preprocessing pipeline:** Label encoding → missing value imputation → standard scaling → PCA (10 components)

---

## Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- Git

### Backend Setup

```bash
# 1. Clone the repository
git clone https://github.com/Eng-Proj-Col/Spam-Detecction-for-Smart-Home-Devices-for-Home-Devices.git
cd Spam-Detecction-for-Smart-Home-Devices-for-Home-Devices

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Seed the database (creates default admin/user accounts)
python3 seed.py

# 5. Run the Flask application
python3 app.py
# → http://localhost:5020
```

### Next.js Frontend Setup

```bash
cd spam-detection-nextjs
npm install
npm run dev
# → http://localhost:3000
```

> The Flask backend must be running before using the Next.js frontend.

### Docker

```bash
docker build -t spam-detection-iot .
docker run -p 5020:5020 spam-detection-iot
```

---

## Configuration

All configuration is via environment variables (`.env` file in project root):

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `dev-secret-change-in-prod` | Flask session secret |
| `JWT_SECRET_KEY` | `jwt-secret-change-in-prod` | JWT signing key |
| `ADMIN_USER` | `admin` | Admin username |
| `ADMIN_PASS` | `admin` | Admin password |
| `USER_USER` | `user` | User username |
| `USER_PASS` | `user` | User password |
| `FLASK_PORT` | `5020` | Port to run on |
| `FLASK_ENV` | `development` | `development` or `production` |
| `SENTRY_DSN` | _(empty)_ | Optional Sentry error tracking DSN |

---

## Usage

### Admin Workflow
1. Go to `http://localhost:3000/admin` (or `http://localhost:5020/admin`)
2. Login with `admin` / `admin`
3. **Upload Dataset** → upload `Dataset.csv`
4. **Compare Algorithms** → click "Run Comparison" — trains 5 models and shows metrics
5. **Create Model** → trains the neural network — view accuracy/loss charts

### User Workflow
1. Go to `http://localhost:3000/user`
2. Login with `user` / `user`
3. **Predict** → enter 10 PCA component values → get spam/valid result
4. **Bulk Ingest** → upload a CSV or paste JSON for batch predictions

### Data Ingestion API (cURL examples)

**Login:**
```bash
curl -X POST http://localhost:5020/api/user/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "user"}'
```

**Single prediction:**
```bash
curl -X POST http://localhost:5020/api/ingest \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"parameters": [-2.28, -0.60, -0.35, -0.18, 0.13, 0.08, -0.03, -0.03, -0.02, 0.004]}'
```

**Batch prediction:**
```bash
curl -X POST http://localhost:5020/api/ingest/batch \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"records": [[-2.28,-0.60,-0.35,-0.18,0.13,0.08,-0.03,-0.03,-0.02,0.004], [3.90,-0.54,-1.33,-0.60,-0.34,-0.28,-0.47,-0.03,0.005,-0.03]]}'
```

**CSV upload (returns JSON):**
```bash
curl -X POST http://localhost:5020/api/ingest/csv \
  -H "Authorization: Bearer <token>" \
  -F "file=@your_data.csv"
```

**CSV upload (returns downloadable CSV with predictions):**
```bash
curl -X POST "http://localhost:5020/api/ingest/csv?format=csv" \
  -H "Authorization: Bearer <token>" \
  -F "file=@your_data.csv" -o predictions.csv
```

**CSV format:** Columns named `p0` through `p9`, or any CSV with at least 10 numeric columns (first 10 used as PCA components). Max 5,000 rows.

---

## Project Structure

```
code/
├── app.py                      # App factory (create_app), entry point
├── config.py                   # DevelopmentConfig / ProductionConfig
├── extensions.py               # SQLAlchemy, Migrate, JWT, CORS instances
├── seed.py                     # DB seeding script (creates default users)
├── requirements.txt            # Production Python dependencies
├── requirements-dev.txt        # Dev tools (black, flake8, mypy, pytest)
├── pyproject.toml              # black + isort + mypy config
├── .flake8                     # flake8 config
├── Dockerfile                  # Docker containerization
├── Dataset.csv                 # IoT smart home dataset (1,664 rows)
├── iot_spam_model.h5           # Pre-trained Keras deep learning model
│
├── models/                     # SQLAlchemy ORM models
│   ├── user.py                 # User (username, password_hash, role)
│   ├── prediction.py           # Prediction (parameters, result, source)
│   ├── dataset.py              # Dataset (filename, row_count, is_active)
│   └── model_version.py        # ModelVersion (version, accuracy, is_active)
│
├── services/                   # Business logic layer
│   ├── ml_service.py           # MLService: preprocess, train, predict, batch
│   └── auth_service.py         # AuthService: DB-backed login + last_login
│
├── views/                      # Flask blueprints (REST JSON API)
│   ├── adminbp.py              # /api/admin/* routes (login, upload, train)
│   ├── userbp.py               # /api/user/* routes (login, predict, history)
│   ├── ingest_bp.py            # /api/ingest/* routes (single, batch, CSV)
│   └── health_bp.py            # GET /health (DB + model status check)
│
├── utils/
│   ├── responses.py            # success_response() / error_response()
│   ├── logging_config.py       # Structured JSON logging setup
│   └── request_logger.py       # Per-request latency logging
│
├── data/                       # Legacy ML modules (kept for reference)
│   ├── compAlg.py              # Original 5-algorithm comparison
│   ├── FinalClassifier.py      # Original deep learning training
│   └── TestModel.py            # Original model inference
│
├── templates/                  # Classic Flask HTML templates
├── static/                     # CSS, images, generated ML plots
├── uploads/                    # Uploaded datasets
├── logs/                       # Application log files (production)
│
└── spam-detection-nextjs/      # Modern Next.js frontend
    ├── app/                    # Pages (admin/, user/, user/ingest/)
    ├── components/             # ErrorBoundary, LoadingSpinner, Toast, ProtectedRoute
    ├── context/                # AuthContext, ToastContext
    ├── lib/                    # api.ts (Axios+JWT), auth.ts (sessionStorage)
    ├── types/                  # api.ts (TypeScript response types)
    ├── .env.local              # NEXT_PUBLIC_API_URL
    ├── .eslintrc.json          # ESLint config
    └── .prettierrc             # Prettier config
```

---

## Health Check

```bash
curl http://localhost:5020/health
```
```json
{
  "status": "healthy",
  "checks": { "db": "ok", "model": "loaded" },
  "timestamp": "2026-04-05T10:00:00",
  "version": "1.0.0"
}
```

---

## Default Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin` |
| User | `user` | `user` |

> Change these via environment variables (`ADMIN_PASS`, `USER_PASS`) or update directly in the database using `seed.py`.
