# Project Explanation: Spam Detection for Smart Home Devices Using Machine Learning

This document explains the entire project in simple terms — what it does, how it works, and what every part is for.

---

## What Is This Project About?

Imagine your house is a **smart home** — your lights turn on automatically, your thermostat adjusts itself, your door locks when you leave, and your fridge tells you when you're out of milk. All these devices are connected to the internet and talk to each other. This is called the **Internet of Things (IoT)**.

Now imagine a **hacker** tries to send fake messages to your smart devices — maybe to unlock your door, or to flood your system with thousands of fake commands so your real devices stop working. These fake messages are called **spam**.

This project builds a system that can **automatically detect whether a message from a smart home device is real (normal) or fake (spam)** using Machine Learning — and it exposes a full REST API so any system can send records and get predictions back.

---

## What Are Smart Home Devices?

Smart home devices are everyday objects connected to the internet:

| Device | What It Does | Example in This Project |
|--------|-------------|------------------------|
| Smart Lights | Turn on/off from your phone | `lightcontrol1`, `lightcontrol2` |
| Smart Thermostat | Adjusts temperature automatically | `thermostat1` |
| Smart Lock | Locks/unlocks doors remotely | Part of security system |
| Smart Sensors | Detects motion, temperature, etc. | Various sensor devices |

Each device sends **messages** through the network. For example, when you turn on a light, it sends a message like: "I am lightcontrol2, I'm in the Parents' Bedroom, and I want to register my service."

---

## What Is Spam in IoT?

In email, spam is unwanted junk mail. In IoT, **spam is fake or malicious messages** sent by attackers:

- **Flooding attacks** — Sending thousands of fake messages to overwhelm the system
- **Fake device registration** — Pretending to be a legitimate device
- **Unauthorized commands** — Sending commands to devices you don't own
- **Data theft** — Intercepting messages between devices

---

## How the Machine Learning Works

### The Dataset

The project uses data from real smart home device interactions (REFIT Smart Home dataset). Each record has:

- **Who sent the message?** (sourceID — e.g., "lightcontrol2")
- **Where did it come from?** (sourceAddress, sourceLocation — e.g., "BedroomParents")
- **Where is it going?** (destinationServiceAddress, destinationLocation)
- **What is it trying to do?** (operation — e.g., "registerService")
- **Is it real or fake?** (normality — "normal" or "spam")

There are **1,664 records** in total, and the system learns the difference between normal and spam messages.

### Step 1: Data Preprocessing (Cleaning the Data)

Computers only understand numbers, not words like "BedroomParents". So the first step converts everything:

1. **Label Encoding** — Convert text to numbers ("BedroomParents" → 0, "Kitchen" → 1)
2. **Handling Missing Values** — Fills gaps using constant or mean values
3. **Standard Scaling** — Makes all numbers the same size range so no feature dominates
4. **PCA (Principal Component Analysis)** — Compresses 11 features into **10 key components** that capture most of the information (like summarizing an essay into 10 bullet points)

### Step 2: Training the 5 ML Models (Admin → Compare Algorithms)

#### 1. Bagging Classifier (with SVC)
Instead of asking one expert, ask **10 different experts** and take the majority vote. Each expert sees a slightly different sample of data.

#### 2. Gaussian Naive Bayes
Uses **probability math** to ask: "Given these features, how likely is this message to be spam?" It's fast and works surprisingly well even with simple assumptions.

#### 3. AdaBoost (Adaptive Boosting)
Like a student who studies for a test, focuses extra hard on the questions they got wrong, and repeats **100 times**. Each round corrects the mistakes of the last round.

#### 4. Voting Classifier
Combines **3 different models** (Logistic Regression, Random Forest, Gaussian NB) and takes a vote. Majority wins.

#### 5. Decision Tree
Works like **20 Questions** — a flowchart of yes/no questions that leads to the final answer (spam or normal).

### Step 3: Deep Learning Neural Network (Admin → Create Model)

After comparing the 5 models, a **neural network** is trained — a computer system inspired by the human brain:

```
Input (10 PCA components)
       ↓
Hidden Layer 1 (4 neurons, ReLU)
       ↓
Hidden Layer 2 (4 neurons, ReLU)
       ↓
Output (1 neuron, Sigmoid → 0=Normal, 1=Spam)
```

- **200 epochs** — The model sees all data 200 times, improving each round
- **Adam optimizer** — Automatically adjusts the learning rate
- **Binary Cross-Entropy loss** — Measures how wrong the predictions are

### Step 4: Making Predictions

Users can submit device records in three ways:

1. **Manual form** — Enter 10 PCA values, get instant result
2. **Single API call** — POST one JSON record, get prediction back
3. **Bulk ingestion** — Upload a CSV or send a batch JSON array; get predictions for all rows at once, optionally as a downloadable CSV

---

## How to Measure If the Model Is Good?

| Metric | What It Means |
|--------|--------------|
| **Accuracy** | What percentage of all predictions were correct? |
| **Precision** | When the model says "spam," how often is it actually spam? |
| **Recall** | Of all actual spam messages, how many did the model catch? |
| **F1-Score** | A balanced score combining precision and recall |

---

## Application Architecture

### Backend (Flask REST API)

The backend is built using the **App Factory pattern** — a professional software design that makes the application configurable, testable, and scalable.

```
app.py (create_app)
├── config.py          → Development / Production settings
├── extensions.py      → Database, JWT, CORS (created once, shared everywhere)
├── models/            → Database tables
│   ├── User           → Stores admin and user accounts with hashed passwords
│   ├── Prediction     → Every prediction stored with parameters and result
│   ├── Dataset        → Tracks uploaded CSV files
│   └── ModelVersion   → Tracks trained model versions with accuracy
├── services/
│   ├── MLService      → All ML logic: preprocess, train, predict, batch predict
│   └── AuthService    → Login against the database, updates last_login time
├── views/
│   ├── adminbp        → /api/admin/* REST endpoints
│   ├── userbp         → /api/user/* REST endpoints
│   ├── ingest_bp      → /api/ingest/* data ingestion endpoints
│   └── health_bp      → /health status check
└── utils/
    ├── responses      → Consistent JSON envelope for all API responses
    ├── logging_config → Structured logging (JSON in production, readable in dev)
    └── request_logger → Logs every request with method, path, status, latency
```

### Database (SQLite via SQLAlchemy)

Every important action is recorded in the database:

- **User logins** → User table (with last login timestamp)
- **Every prediction** → Prediction table (parameters, result, source: manual/api/csv)
- **Dataset uploads** → Dataset table (filename, row count, which one is active)
- **Model training** → ModelVersion table (version number, accuracy, which one is active)

### Authentication (JWT)

The API uses **JSON Web Tokens (JWT)**:

1. Login endpoint returns a token (valid 1 hour)
2. All protected endpoints require `Authorization: Bearer <token>` header
3. The Next.js frontend stores the token in sessionStorage and attaches it automatically via an Axios interceptor
4. On 401 (expired/invalid), the frontend clears the token and redirects to login

### Data Ingestion API

This is the most important new feature for real-world use:

```
POST /api/ingest          → Single record
POST /api/ingest/batch    → Up to 1,000 records in one call
POST /api/ingest/csv      → CSV file with up to 5,000 rows
                            ?format=csv → returns CSV with predictions column added
                            ?format=json (default) → returns JSON summary
```

All ingestion endpoints:
- Require JWT authentication
- Validate input carefully (correct number of columns, numeric values, size limits)
- Store every prediction in the database with `source = "api"` or `source = "csv"`
- Return spam count, valid count, and per-record results

### Frontend (Next.js)

The modern frontend is built with **React + TypeScript + Tailwind CSS**:

| Component | What It Does |
|-----------|-------------|
| `AuthContext` | Global JWT state — login/logout available everywhere |
| `ToastContext` | Toast notifications (green = success, red = error, blue = info) |
| `ErrorBoundary` | Catches React errors and shows a friendly "Try again" screen |
| `ProtectedRoute` | Guards pages — redirects to login if no valid token |
| `LoadingSpinner` | Reusable spinner for all loading states |
| `ToastContainer` | Fixed bottom-right stack of notification toasts |

**Login pages** now call the real Flask API (not hardcoded strings) and use toasts for feedback.

**Bulk Ingest page** (`/user/ingest`) supports three modes:
1. CSV file upload with optional CSV download of results
2. Single JSON record with a labeled 10-field form
3. Batch JSON with a text area and example template

**Compare Algorithms page** now calls the real API (removed mock data) and shows a "Run Comparison" button with a loading spinner.

---

## What Does the Health Check Tell You?

```bash
GET /health
```
```json
{
  "status": "healthy",
  "checks": {
    "db": "ok",
    "model": "loaded"
  },
  "timestamp": "2026-04-05T10:00:00",
  "version": "1.0.0"
}
```

- `db: ok` — The database is connected and responding
- `model: loaded` — The Keras `.h5` model is in memory, ready to predict
- `status: degraded` — Something is wrong (HTTP 503 instead of 200)

---

## Logging

In development: human-readable log lines in the terminal.
In production: **structured JSON logs** written to `logs/app.log` with rotation (10MB per file, 5 backups kept).

Every request is logged:
```json
{"method": "POST", "path": "/api/user/predict", "status": 200, "duration_ms": 45.2}
```

---

## Why Is This Project Important?

1. **IoT Security** — Over 75 billion IoT devices are expected worldwide by 2025. Detecting spam behavior is critical to keeping smart homes safe
2. **ML for Cybersecurity** — ML can detect subtle attack patterns that traditional rule-based systems miss
3. **REST API for automation** — Any external system, SIEM, or monitoring tool can send device records and get real-time spam detection via the ingestion API
4. **Production-grade design** — The App Factory, JWT auth, database persistence, structured logging, and error handling demonstrate real-world software engineering practices

---

## Technology Summary

| Technology | Purpose |
|-----------|---------|
| **Flask 3.0** | Web server + REST API framework |
| **Flask-SQLAlchemy** | Database ORM (SQLite in dev, PostgreSQL-ready) |
| **Flask-JWT-Extended** | JWT token authentication |
| **Flask-CORS** | Cross-Origin Resource Sharing for Next.js |
| **TensorFlow / Keras** | Deep Learning neural network |
| **scikit-learn** | 5 classical ML algorithms |
| **pandas / NumPy** | Data processing and PCA transformation |
| **Matplotlib** | Learning curves and accuracy/loss plots |
| **Next.js 14** | Modern React frontend |
| **TypeScript** | Type-safe frontend code |
| **Tailwind CSS** | Utility-first CSS styling |
| **Recharts** | Interactive algorithm comparison charts |
| **Axios** | HTTP client with JWT interceptors |
| **SQLite** | Lightweight embedded database |
