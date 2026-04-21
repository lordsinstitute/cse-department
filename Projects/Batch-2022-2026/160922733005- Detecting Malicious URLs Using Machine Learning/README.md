# C12 — Detecting Malicious URLs Using Machine Learning

## Project Structure

```
code/
├── app.py                          # Main Flask application
├── generate_dataset.py             # Synthetic URL dataset generator
├── train_model.py                  # ML model training + EDA visualizations
├── url_model.pkl                   # Trained Gradient Boosting model
├── models_info.json                # Model performance metrics
├── malicious_urls.csv              # Dataset (10,000 URLs)
├── url_detect.db                   # SQLite database (auto-created)
├── Dockerfile                      # Docker container configuration
├── .dockerignore                   # Docker ignore file
├── static/
│   └── vis/                        # EDA visualization charts (12 charts)
│       ├── label_dist.png          # Legitimate vs Malicious Distribution
│       ├── url_length.png          # URL Length Distribution
│       ├── https_dist.png          # HTTP vs HTTPS by Label
│       ├── ip_dist.png             # IP Address Presence
│       ├── suspicious_words.png    # Suspicious Words Count
│       ├── domain_length.png       # Domain Length Distribution
│       ├── subdomains.png          # Number of Subdomains
│       ├── special_ratio.png       # Special Character Ratio
│       ├── url_depth.png           # URL Path Depth
│       ├── correlation.png         # Feature Correlation Heatmap
│       ├── feature_importance.png  # Random Forest Feature Importance
│       └── confusion_matrix.png    # Best Model Confusion Matrix
└── templates/
    ├── base.html                   # Base layout (navbar, Bootstrap 5, dark theme)
    ├── home.html                   # Home page with stats and quick actions
    ├── login.html                  # Login page
    ├── register.html               # Registration page
    ├── predict.html                # URL analysis form + result
    ├── history.html                # Scan history table
    ├── visualize.html              # EDA visualization gallery
    ├── dashboard.html              # Model comparison charts and analytics
    └── about.html                  # About page with feature details
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps (Windows)

**Step 1:** Open Command Prompt and navigate to project

```bash
cd code
```

**Step 2:** Install required packages

```bash
pip install flask scikit-learn pandas numpy matplotlib seaborn werkzeug
```

**Step 3:** Generate the dataset (first time only)

```bash
python generate_dataset.py
```

**Step 4:** Train the models and generate visualizations (first time only)

```bash
python train_model.py
```

**Step 5:** Run the application

```bash
python app.py
```

**Step 6:** Open in browser

```
http://127.0.0.1:5004
```

The SQLite database (`url_detect.db`) is auto-created on first run with an admin user.

---

## Docker Setup (Windows)

### Prerequisites

- Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
- Make sure Docker Desktop is running
- Run Steps 3 and 4 above first to generate `url_model.pkl` and visualizations

### Build and Run

**Step 1:** Open Command Prompt and navigate to project

```bash
cd code
```

**Step 2:** Build the Docker image

```bash
docker build -t url-detect .
```

**Step 3:** Run the container

```bash
docker run -d -p 5004:5004 --name url-detect-app url-detect
```

**Step 4:** Open in browser

```
http://localhost:5004
```

### Docker Management Commands

```bash
# Stop the container
docker stop url-detect-app

# Start the container again
docker start url-detect-app

# Remove the container
docker rm -f url-detect-app

# View logs
docker logs url-detect-app

# Rebuild after code changes
docker rm -f url-detect-app
docker build -t url-detect .
docker run -d -p 5004:5004 --name url-detect-app url-detect
```

---

## Accounts

| Role | Username | Password | Access |
|---|---|---|---|
| Admin | `admin` | `admin123` | Home (global stats), Detect, History, Visualize, Dashboard, About |
| User | (register) | (register) | Home, Detect, History, Visualize, Dashboard, About |

## Pages Overview

| Page | URL | Description |
|---|---|---|
| Login | `/login` | Login with credentials |
| Register | `/register` | Create a new account |
| Home | `/home` | Stats, recent scans, quick actions |
| Detect | `/predict` | Enter a URL for malicious detection |
| History | `/history` | View all past scan results |
| Visualize | `/visualize` | EDA charts (12 visualizations) |
| Dashboard | `/dashboard` | Model comparison and analytics charts |
| About | `/about` | 28 features explained, tech stack, model info |

---

## Model Performance

| Model | Accuracy | Precision | Recall | F1 Score |
|---|---|---|---|---|
| **Gradient Boosting** | **92.35%** | 91.53% | 93.10% | 92.31% |
| SVM | 92.30% | 91.52% | 93.00% | 92.25% |
| MLP Neural Network | 92.30% | 91.43% | 93.10% | 92.26% |
| K-Nearest Neighbors | 91.95% | 91.46% | 92.29% | 91.87% |
| Logistic Regression | 91.45% | 92.05% | 90.47% | 91.25% |
| Random Forest | 90.65% | 90.56% | 90.47% | 90.51% |
| Decision Tree | 89.10% | 91.03% | 86.41% | 88.66% |
| Naive Bayes | 82.85% | 92.25% | 71.20% | 80.37% |

## Dataset Features (28)

| # | Feature | Description |
|---|---|---|
| 1 | url_length | Total length of the URL |
| 2 | n_dots | Number of dots in URL |
| 3 | n_hyphens | Number of hyphens |
| 4 | n_underscores | Number of underscores |
| 5 | n_slashes | Number of forward slashes |
| 6 | n_question_marks | Number of question marks |
| 7 | n_equal | Number of equal signs |
| 8 | n_at | Number of @ symbols |
| 9 | n_ampersand | Number of & characters |
| 10 | n_percent | Number of % (encoding) characters |
| 11 | n_digits | Count of digit characters |
| 12 | n_letters | Count of letter characters |
| 13 | n_special | Count of non-alphanumeric characters |
| 14 | has_https | Uses HTTPS protocol (1/0) |
| 15 | has_ip | Contains IP address (1/0) |
| 16 | domain_length | Length of domain part |
| 17 | n_subdomains | Number of subdomain levels |
| 18 | path_length | Length of URL path |
| 19 | url_depth | Number of path segments |
| 20 | has_at_symbol | @ symbol present (1/0) |
| 21 | double_slash_redirect | Multiple // found (1/0) |
| 22 | prefix_suffix | Hyphen in domain (1/0) |
| 23 | n_suspicious_words | Count of phishing keywords |
| 24 | is_shortened | URL shortener used (1/0) |
| 25 | suspicious_tld | Suspicious TLD like .tk, .xyz (1/0) |
| 26 | digit_ratio | Ratio of digits to URL length |
| 27 | letter_ratio | Ratio of letters to URL length |
| 28 | special_ratio | Ratio of special chars to URL length |

---

## Test Cases

### Test Case 1: Legitimate URL — Google Search

1. Login as `admin` / `admin123`
2. Click **Detect** in navbar
3. Enter: `https://www.google.com/search?q=python`
4. Click **Analyze URL**

**Expected Result:** Legitimate (high confidence)

**Why:** Short URL, HTTPS, well-known domain, no suspicious words, no IP address, simple path.

---

### Test Case 2: Legitimate URL — GitHub

1. Enter: `https://github.com/trending`
2. Click **Analyze URL**

**Expected Result:** Legitimate (high confidence)

**Why:** Short URL, HTTPS, well-known domain (github.com), single path segment, no suspicious indicators.

---

### Test Case 3: Malicious URL — IP Address with Phishing Keywords

1. Enter: `http://192.168.1.1/login/verify/account`
2. Click **Analyze URL**

**Expected Result:** Malicious (high confidence)

**Why:** Uses IP address instead of domain name, HTTP (not HTTPS), contains suspicious words ("login", "verify", "account"), deep path.

---

### Test Case 4: Malicious URL — Suspicious TLD with Keywords

1. Enter: `http://secure-login-verify.tk/account/password`
2. Click **Analyze URL**

**Expected Result:** Malicious (high confidence)

**Why:** Suspicious TLD (.tk), multiple suspicious words ("secure", "login", "verify", "account", "password"), HTTP, hyphens in domain.

---

### Test Case 5: Malicious URL — Misspelled Domain

1. Enter: `http://g00gle.tk/login`
2. Click **Analyze URL**

**Expected Result:** Malicious (high confidence)

**Why:** Fake/misspelled domain (g00gle instead of google), suspicious TLD (.tk), suspicious word ("login"), HTTP.

---

### Test Case 6: Malicious URL — URL Shortener

1. Enter: `https://bit.ly/abc123xy`
2. Click **Analyze URL**

**Expected Result:** Malicious (high confidence)

**Why:** URL shortener (bit.ly) which hides the real destination, common phishing technique.

---

### Test Case 7: Legitimate URL — Amazon

1. Enter: `https://www.amazon.com/products`
2. Click **Analyze URL**

**Expected Result:** Legitimate (high confidence)

**Why:** Well-known domain, HTTPS, simple path, no suspicious indicators.

---

### Test Case 8: Malicious URL — Long Subdomain Chain

1. Enter: `http://login.verify.account.security.update.xyz/credential`
2. Click **Analyze URL**

**Expected Result:** Malicious (high confidence)

**Why:** Multiple suspicious subdomains, suspicious TLD (.xyz), many suspicious words, HTTP, deep nesting.

---

### Test Case 9: Legitimate URL — Wikipedia

1. Enter: `https://en.wikipedia.org/wiki/Machine_learning`
2. Click **Analyze URL**

**Expected Result:** Legitimate (high confidence)

**Why:** Well-known domain (wikipedia.org), HTTPS, clean path, no suspicious elements.

---

### Test Case 10: Malicious URL — At Symbol Redirect

1. Enter: `http://admin@secure-banking.tk/wallet/payment`
2. Click **Analyze URL**

**Expected Result:** Malicious (high confidence)

**Why:** @ symbol (used for redirect attacks), suspicious TLD (.tk), suspicious words ("secure", "banking", "wallet", "payment"), hyphens in domain.

---

### Test Case 11: View Scan History

1. After running Test Cases 1-10, click **History** in navbar
2. View the table with all past scans

**Expected:** Table shows URL, result badge (Legitimate/Malicious), confidence %, URL length, HTTPS status, IP presence, suspicious words count, and date for each scan.

---

### Test Case 12: Data Visualizations

1. Click **Visualize** in navbar
2. View 12 EDA charts:
   - URL Distribution (pie chart)
   - URL Length Distribution
   - Protocol (HTTP vs HTTPS)
   - IP Address Presence
   - Suspicious Words Count
   - Domain Length Distribution
   - Number of Subdomains
   - Special Character Ratio
   - URL Path Depth
   - Feature Correlation Heatmap
   - Feature Importance (Random Forest)
   - Confusion Matrix (Best Model)

**Expected:** All 12 charts display correctly.

---

### Test Case 13: Dashboard Analytics

1. Click **Dashboard** in navbar
2. View Model Performance table (8 models)
3. View charts: Accuracy Comparison, F1 Score, Precision vs Recall, Radar Chart
4. View training/test size stats

**Expected:** Gradient Boosting highlighted as best model (92.35%). Charts show clear model comparison.

---

### Test Case 14: Feature Extraction Display

1. Click **Detect** → Enter any URL → Click **Analyze URL**
2. Below the prediction result, view the "Extracted Features" table

**Expected:** Shows 18 key features extracted from the URL (URL Length, Domain Length, Path Length, HTTPS, IP, Subdomains, etc.).

---

### Test Case 15: Admin Dashboard

1. Logout → Login as `admin` / `admin123`
2. Home page shows additional admin stats: Registered Users, Total Scans (All Users), Total Malicious Detected
3. All other pages work the same

**Expected:** Admin sees global statistics across all users.

---

### Test Case 16: User Registration and Isolation

1. Click **Logout** → Click **Register**
2. Register as: Name: `Alice`, Username: `alice`, Password: `pass123`
3. Login as `alice` / `pass123`
4. Scan a URL
5. Check History — should only show Alice's scans (not admin's)

**Expected:** New user can register and login. History is isolated per user.

---

## Notes

- SQLite database (`url_detect.db`) is auto-created on first run — no setup needed
- Admin account (`admin`/`admin123`) is seeded automatically
- Passwords are hashed using Werkzeug (not stored in plain text)
- Model files must exist before running the app — run `train_model.py` first
- 12 EDA visualizations are generated during training
- The dataset is synthetic (generated by `generate_dataset.py`) for demonstration
- URLs without `http://` or `https://` prefix get `http://` added automatically
- 28 features are extracted from each URL for classification
- To reset data, delete `url_detect.db` and restart the app
