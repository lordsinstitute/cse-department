# — A Simple Scanner for Identifying Web Application Vulnerabilities

## Project Structure

```
code/
├── app.py                          # Main Flask application
├── vulnerability_fix_dataset.csv   # Vulnerability fix suggestions dataset
├── scanner.db                      # SQLite database (auto-created on first run)
├── Dockerfile                      # Docker container configuration
├── .dockerignore                   # Docker ignore file
├── static/                         # Static assets
└── templates/
    ├── base.html                   # Base layout (navbar, Bootstrap 5, dark theme)
    ├── home.html                   # Main scanner page with URL input
    ├── login.html                  # Login page
    ├── register.html               # Registration page
    ├── result.html                 # Last scan result with fix suggestions
    ├── history.html                # Full scan history table
    ├── dashboard.html              # Analytics with charts (Chart.js)
    └── about.html                  # About page with feedback form
```

## Features

- **11 Vulnerability Checks:** XSS, SQL Injection, CSRF, Clickjacking, Missing CSP, Missing Security Headers, Directory Listing, Insecure Cookies, Information Disclosure, Server Version Exposed, Mixed Content
- **Fix Suggestions:** Shows vulnerable code vs fixed code for each finding
- **Severity Levels:** Critical, High, Medium, Low with color coding
- **Scan History:** All past scan results stored in SQLite database
- **Dashboard:** Charts showing vulnerability distribution, severity breakdown, and findings per website
- **User Authentication:** Secure registration and login with password hashing (Werkzeug)
- **Admin Support:** Admin user sees additional stats on dashboard
- **Feedback System:** Users can submit feedback from the About page

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
pip install flask requests beautifulsoup4 werkzeug
```

**Step 3:** Run the application

```bash
python app.py
```

**Step 4:** Open in browser

```
http://127.0.0.1:5001
```

The SQLite database (`scanner.db`) is auto-created on first run with an admin user.

---

## Docker Setup (Windows)

### Prerequisites

- Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
- Make sure Docker Desktop is running

### Build and Run

**Step 1:** Open Command Prompt and navigate to project

```bash
cd code
```

**Step 2:** Build the Docker image

```bash
docker build -t vuln-scanner .
```

**Step 3:** Run the container

```bash
docker run -d -p 5001:5001 --name scanner-app vuln-scanner
```

**Step 4:** Open in browser

```
http://localhost:5001
```

### Docker Management Commands

```bash
# Stop the container
docker stop scanner-app

# Start the container again
docker start scanner-app

# Remove the container
docker rm -f scanner-app

# View logs
docker logs scanner-app

# Rebuild after code changes
docker rm -f scanner-app
docker build -t vuln-scanner .
docker run -d -p 5001:5001 --name scanner-app vuln-scanner
```

---

## Accounts

| Role | Username | Password | Access |
|---|---|---|---|
| Admin | `admin` | `admin123` | Scanner, Dashboard (with global stats), History, About |
| User | (register) | (register) | Scanner, Dashboard, History, About |

## Pages Overview

| Page | URL | Access | Description |
|---|---|---|---|
| Login | `/login` | Guest | Login with credentials |
| Register | `/register` | Guest | Create a new account |
| Scanner | `/home` | User | Enter URL and scan for vulnerabilities |
| Last Result | `/result` | User | View most recent scan with fix suggestions |
| History | `/history` | User | View all past scan results |
| Dashboard | `/dashboard` | User | Charts and analytics |
| About | `/about` | All | About page with feedback form |

---

## Quick Start

1. Open browser: `http://127.0.0.1:5001`
2. Click "Register" → Name: `John`, Username: `john`, Password: `pass123`
3. Login with same credentials
4. Enter a URL (e.g., `https://example.com`) and click **Scan Now**
5. View results with vulnerability details and fix suggestions

---

## Test Cases

### Test Case 1: User Registration and Login

1. Open http://127.0.0.1:5001
2. Click **Register**
3. Fill: Name: `Mohammed`, Username: `mohammed`, Password: `test123`
4. Click **Register** → redirects to Login
5. Enter `mohammed` / `test123` → Click **Login**

**Expected:** Redirects to Scanner page. Welcome message shown.

---

### Test Case 2: Scan a Website (example.com)

1. Login as `mohammed` / `test123`
2. On Scanner page, enter `https://example.com`
3. Click **Scan Now**

**Expected:** Results appear showing findings like "Missing CSP", "Missing Security Header", "Clickjacking" with severity badges and vulnerable/fixed code examples.

---

### Test Case 3: Scan a Website with Forms (httpbin.org)

1. Login as any user
2. Enter `https://httpbin.org/forms/post`
3. Click **Scan Now**

**Expected:** Additional findings related to forms (XSS, CSRF) along with header-based vulnerabilities.

---

### Test Case 4: View Last Scan Result

1. After scanning, click **Last Result** in navbar
2. View the detailed table of findings from the most recent scan
3. Scroll down to see fix suggestions with vulnerable vs fixed code

**Expected:** Table shows all vulnerabilities from the last scan with severity levels. Fix cards show code comparisons.

---

### Test Case 5: View Scan History

1. Scan multiple websites (e.g., `example.com`, `httpbin.org`)
2. Click **History** in navbar

**Expected:** Full table showing all past scan results with website, vulnerability type, description, severity, and date.

---

### Test Case 6: Dashboard Analytics

1. After performing several scans, click **Dashboard**
2. View stats cards (Total Findings, Websites Scanned)
3. View charts: Vulnerability Distribution (doughnut), Severity Breakdown (pie), Findings per Website (bar)

**Expected:** Charts reflect actual scan data. Stats are accurate.

---

### Test Case 7: Admin Dashboard

1. Login as `admin` / `admin123`
2. Click **Dashboard**
3. View additional admin stats: Registered Users, Total Scans (All Users), Unique Sites Scanned

**Expected:** Admin sees global statistics in addition to personal stats.

---

### Test Case 8: Invalid URL Handling

1. Login as any user
2. Enter `not-a-valid-url` in the scanner
3. Click **Scan Now**

**Expected:** Error message: "Invalid URL provided. Please enter a valid URL."

---

### Test Case 9: Submit Feedback

1. Login as any user
2. Click **About** in navbar
3. Scroll to "Send Feedback" form
4. Enter feedback message and click **Submit Feedback**

**Expected:** "Thank you for your feedback!" success message appears.

---

## Vulnerability Checks

| # | Vulnerability | Severity | Detection Method |
|---|---|---|---|
| 1 | SQL Injection | Critical | Appends `'` to URL params, checks for SQL error strings |
| 2 | Cross-Site Scripting (XSS) | High | Checks forms for missing input validation |
| 3 | CSRF Vulnerability | High | Checks POST forms for missing CSRF tokens |
| 4 | Directory Listing | High | Searches for "Index of /" in page content |
| 5 | Missing Security Header | Medium | Checks for X-Content-Type-Options header |
| 6 | Missing CSP | Medium | Checks for Content-Security-Policy header |
| 7 | Clickjacking | Medium | Checks for X-Frame-Options header |
| 8 | Insecure Cookies | Medium | Checks cookies for Secure and HttpOnly flags |
| 9 | Information Disclosure | Low | Scans HTML comments for sensitive keywords |
| 10 | Server Version Exposed | Low | Checks Server header for version numbers |
| 11 | Mixed Content | Low | Finds HTTP resources loaded on HTTPS pages |

## Notes

- SQLite database (`scanner.db`) is auto-created on first run — no setup needed
- Admin account (`admin`/`admin123`) is seeded automatically
- Passwords are hashed using Werkzeug (not stored in plain text)
- Scan results persist across server restarts (stored in `.db` file)
- To reset data, simply delete `scanner.db` and restart the app
- The scanner sends requests with a standard User-Agent header
- SSL verification is disabled for scanning to support self-signed certificates

