# Network Intrusion Detection System (NIDS)

Full-stack **flow-level** NIDS: FastAPI backend + Next.js SOC dashboard. Live/PCAP ingestion, multi-dataset SVM training (NSL-KDD, UNSW-NB15, CIC-IDS2017/2018, BoT-IoT), drift monitoring, explainability, analyst feedback, Splunk HEC.

---

## Overview

- **Backend**: Class-weighted SVM (F1/minority recall), rule fallback; **MITRE ATT&CK** mapping; multi-dataset loaders; PCAP upload and batch flow ingest; adaptive drift; confidence/uncertainty; explainability API; analyst feedback; Splunk HEC; JWT auth.
- **Frontend**: SOC dark UI; real-time alert stream (WebSocket); severity/attack charts; explainability and feedback pages; drift and training run views.
- **API**: Flow ingestion, alerts, stats, WebSocket; training runs; explain; drift; feedback; auth.
- **Frontend (Next.js)**: SOC dark UI; real-time alerts (WebSocket); severity/attack viz; explainability; analyst feedback; drift; training runs.

It is suitable as a **demo/reference** and for extension; it is not a drop-in replacement for production tools like Suricata or Zeek.

---

## Architecture

```
                    +------------------+
                    |  Frontend (HTML/JS)
                    |  Dashboard + filters, stats
                    +--------+---------+
                             | HTTP / WebSocket
                             v
+----------+   POST /ingest/flow   +------------------+   broadcast   +----------+
| Simulator| ------------------> |  FastAPI Backend | ------------> | WebSocket|
| or PCAP  |                      |  - Validation    |               | clients  |
| or CSV   |                      |  - ML / rules    |               +----------+
+----------+                      |  - DB (SQLite/PG) |
                                  +--------+---------+
                                           |
                                  +--------v---------+
                                  |  Alerts DB      |
                                  |  (indexed)      |
                                  +-----------------+
```

### Data flow

1. **Ingestion**: Flows arrive via `POST /ingest/flow` (simulator, PCAP script, or external collector). Input is validated (IPs, ports, protocol).
2. **Detection**: Each flow is converted to a feature vector; the trained model (or rule fallback) returns attack type, severity, confidence, and MITRE techniques.
3. **Storage**: Alerts are written to the database (SQLite or PostgreSQL) with source/dest IP, ports, attack type, severity, score, confidence, summary, MITRE.
4. **Alerting**: New alerts are broadcast over WebSocket and returned in the HTTP response.
5. **Dashboard**: The UI fetches alerts with optional filters (attack type, severity, time range, IP search), sort, and deduplication; it also fetches `/api/stats` for trends and top IPs.

---

## Project structure

```
nids-app/
├── backend/
│   ├── app/
│   │   ├── config.py          # Settings (DB, API, ML paths, logging)
│   │   ├── core/               # Logging, validation
│   │   ├── data/               # Features, CICIDS/UNSW loaders, PCAP ingest
│   │   ├── ml/                 # Attack categories, training, inference
│   │   ├── services/           # Alert deduplication, correlation
│   │   ├── database.py         # SQLite / PostgreSQL
│   │   ├── main.py             # FastAPI app, routes
│   │   └── models.py           # Pydantic + SQLAlchemy models
│   ├── scripts/
│   │   ├── train_model.py      # Train on CICIDS/UNSW CSV
│   │   ├── evaluate_model.py   # Confusion matrix, F1, FPR
│   │   └── ingest_pcap.py      # Offline PCAP → POST flows
│   └── requirements.txt
├── frontend/                 # Next.js SOC dashboard
│   ├── app/                  # App Router pages (dashboard, explain, feedback, drift, training)
│   ├── lib/api.ts
│   └── package.json
├── .gitignore                  # Excludes .venv, data, models
└── README.md
```

---

## Prerequisites

- **Python 3.10+**
- Optional: **PostgreSQL** (for production; default is SQLite)
- Optional: **scapy** or **dpkt** for PCAP ingestion (`pip install scapy` or `dpkt`)

---

## Getting started

### 1. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

Run the API (default port 9000):

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 9000
```

### 2. Frontend

Serve the dashboard (e.g. on port 8080):

```bash
cd frontend
python -m http.server 8080
```

Open `http://127.0.0.1:8080`. Point the dashboard to the backend (default `http://127.0.0.1:9000` in `app.js`).

### 3. Simulate traffic

From the `backend` directory:

```bash
python -m app.simulator
```

This sends synthetic flows to `POST /ingest/flow`; alerts appear in the dashboard (and in the DB).

---

## Real data and ML

### Train on CICIDS 2017 or UNSW-NB15

1. Download a CSV from [CICIDS 2017](https://www.unb.ca/cic/datasets/ids-2017.html) or [UNSW-NB15](https://research.unsw.edu.au/projects/unsw-nb15-dataset) and place it under `backend/data/raw/` (or set `CICIDS_CSV` / `UNSW_CSV`).
2. Train and save the model:

```bash
cd backend
python -m scripts.train_model --dataset cicids --path data/raw/YourFile.csv
# or
python -m scripts.train_model --dataset unsw --path data/raw/UNSW_NB15_traintest.csv --max-rows 100000
```

3. The pipeline splits data into train/val/test, trains a Random Forest, and writes:
   - `models/detector.joblib` (model + label encoder)
   - `models/feature_order.json`
4. Set `MODEL_PATH` and `MODEL_FEATURE_ORDER_PATH` if you use another directory. The API will load the model at startup and use it for scoring; otherwise it falls back to rule-based logic.

### Evaluate on test data

```bash
python -m scripts.evaluate_model --dataset cicids --path data/raw/Test.csv --model-path models/detector.joblib
```

This prints accuracy, precision, recall, F1, **false positive rate**, and confusion matrix.

### PCAP offline analysis

With `scapy` or `dpkt` installed:

```bash
python -m scripts.ingest_pcap --pcap capture.pcap --api http://127.0.0.1:9000
```

Flows are aggregated from the PCAP and posted to `/ingest/flow`; the same ML/rules and dashboard apply.

---

## API summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Liveness |
| `/ingest/flow` | POST | Ingest one flow (validated); returns created alert |
| `/api/alerts` | GET | List alerts (optional: `attack_type`, `severity`, `time_from`, `time_to`, `search`, `sort`, `dedupe`) |
| `/api/alerts/{id}` | GET | Get one alert |
| `/api/stats` | GET | Counts by severity, by attack type, top source IPs (optional `time_from`, `time_to`) |
| `/ws/alerts` | WebSocket | Real-time alert stream |

---

## Configuration (environment)

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./alerts.db` | Use `postgresql://user:pass@host:5432/nids` for PostgreSQL |
| `API_HOST` / `API_PORT` | `0.0.0.0` / `9000` | Bind address and port |
| `MODEL_PATH` | `models/detector.joblib` | Trained model file |
| `MODEL_FEATURE_ORDER_PATH` | `models/feature_order.json` | Feature order for the model |
| `USE_RULE_FALLBACK` | `true` | Use rule-based scoring when no model is loaded |
| `LOG_LEVEL` | `INFO` | Logging level |

---

## Attack coverage and MITRE ATT&CK

Detection supports multiple categories, including:

- **DoS / DDoS** – high/critical severity; MITRE T1498, T1499
- **Port scanning** – T1046
- **Brute force** – T1110
- **Botnet** – T1583, T1584, T1585
- **Web attacks** – T1190
- **Exploit / infiltration / data exfiltration** – mapped in `app/ml/attack_categories.py`

Alerts include `attack_type`, `severity`, `confidence`, and `mitre_techniques` for SOC use.

---

## Limitations

- **Flow-level only**: No deep packet inspection; detection is based on flow/connection features (bytes, packets, ports, protocol, duration).
- **Single process**: No built-in horizontal scaling or message queue (Kafka/RabbitMQ); can be added in front of ingestion/detection.
- **Auth**: No authentication on the API or dashboard by default; protect the service in production (e.g. reverse proxy + auth, API keys).
- **Rate limiting**: Ingest endpoint does not enforce rate limits; use a reverse proxy or middleware if you need strict limits.
- **Dataset compatibility**: CICIDS/UNSW CSV parsers assume common column names; your file may need small adjustments in `app/data/datasets.py`.

---

## Future scope

- **Live packet capture**: Integrate with libpcap/Npcap or a sensor that exports flows (e.g. Zeek/Suricata logs) for real-time ingestion.
- **Message queue**: Kafka or RabbitMQ between ingestion, detection, and alerting for scalability.
- **Authentication**: JWT or API keys for dashboard and API; role-based access.
- **Elasticsearch**: Optional secondary store for alerts and full-text search.
- **More models**: Experiment with XGBoost, neural networks, or ensemble methods; A/B test vs rule-based.

---

## Code quality

- **.gitignore**: Excludes `.venv`, `__pycache__`, large data/models, logs.
- **Logging**: Use `app.core.logging.get_logger(__name__)` instead of `print`.
- **Validation**: All flow input validated (IPs, ports, protocol) in `app/core/validation.py`.
- **PEP-8**: Structure and style follow standard Python conventions; docstrings on public modules and key functions.

---

## License and references- CICIDS2017: [Canadian Institute for Cybersecurity](https://www.unb.ca/cic/datasets/ids-2017.html)
- UNSW-NB15: [UNSW](https://research.unsw.edu.au/projects/unsw-nb15-dataset)
- MITRE ATT&CK: [attack.mitre.org](https://attack.mitre.org/)