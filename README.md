# B6 — Medical Report Management & Distribution System Using Blockchain

## Project Structure

```
code/
├── app.py                    # Main Flask application
├── blockchain.py             # Blockchain simulation (SHA-256)
├── medical_blockchain.db     # SQLite database (auto-created)
├── Dockerfile                # Docker container configuration
├── .dockerignore             # Docker ignore file
├── static/
│   └── uploads/              # Uploaded medical report files
└── templates/
    ├── base.html             # Base layout (navbar, Bootstrap 5, dark theme)
    ├── login.html            # Login page
    ├── register.html         # Registration with role selection
    ├── home.html             # Role-based dashboard (Patient/Doctor/Admin)
    ├── upload_report.html    # Doctor: upload medical report
    ├── my_reports.html       # Patient: view own reports
    ├── patient_reports.html  # Doctor: uploaded + shared reports
    ├── view_report.html      # View single report with blockchain info
    ├── share_report.html     # Patient: grant/revoke doctor access
    ├── blockchain.html       # Blockchain explorer with chain view
    ├── audit.html            # Admin: audit trail log
    ├── dashboard.html        # Analytics charts (Chart.js)
    └── about.html            # Project info, tech stack, how blockchain works
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
pip install flask werkzeug
```

**Step 3:** Run the application

```bash
python app.py
```

**Step 4:** Open in browser

```
http://127.0.0.1:5005
```

The SQLite database (`medical_blockchain.db`) is auto-created on first run with sample data.

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
docker build -t medchain .
```

**Step 3:** Run the container

```bash
docker run -d -p 5005:5005 --name medchain-app medchain
```

**Step 4:** Open in browser

```
http://localhost:5005
```

### Docker Management Commands

```bash
# Stop the container
docker stop medchain-app

# Start the container again
docker start medchain-app

# Remove the container
docker rm -f medchain-app

# View logs
docker logs medchain-app

# Rebuild after code changes
docker rm -f medchain-app
docker build -t medchain .
docker run -d -p 5005:5005 --name medchain-app medchain
```

---

## Accounts

| Role | Username | Password | Access |
|---|---|---|---|
| Admin | `admin` | `admin123` | Home (global stats), Blockchain, Audit Trail, Dashboard, About |
| Doctor | `dr_ahmed` | `doctor123` | Home, Upload Report, Patient Reports, Blockchain, Dashboard, About |
| Patient | `patient1` | `patient123` | Home, My Reports, Share Reports, Blockchain, Dashboard, About |
| New User | (register) | (register) | Register as Patient or Doctor |

## Pages Overview

| Page | URL | Access | Description |
|---|---|---|---|
| Login | `/login` | Guest | Login with credentials |
| Register | `/register` | Guest | Create account (Patient or Doctor) |
| Home | `/home` | All | Role-based dashboard with stats |
| Upload Report | `/upload` | Doctor | Upload medical report for a patient |
| My Reports | `/my-reports` | Patient | View own medical reports |
| Patient Reports | `/patient-reports` | Doctor | View uploaded and shared reports |
| View Report | `/report/<id>` | Auth | View single report with blockchain info |
| Share Report | `/share/<id>` | Patient | Grant/revoke doctor access |
| Blockchain | `/blockchain` | All | View blockchain chain with hashes |
| Verify Chain | `/verify` | All | Verify blockchain integrity |
| Audit Trail | `/audit` | Admin | View all system actions |
| Dashboard | `/dashboard` | All | Analytics with 4 charts |
| About | `/about` | All | Project info, tech stack, features |

---

## Blockchain Features

The system uses a simulated blockchain built with Python and SHA-256 hashing:

- **Genesis Block** — Created automatically on first run
- **Block Structure** — Each block contains: index, timestamp, data, data hash, previous hash, block hash
- **Chain Linking** — Each block's hash includes the previous block's hash, creating a tamper-proof chain
- **Integrity Verification** — One-click verification checks all block hashes and chain links
- **Recorded Actions** — Report uploads, access grants, access revocations, report views, integrity checks

---

## Test Cases

### Test Case 1: Patient Registration

1. Go to `/register`
2. Fill: Name=Alice, Username=alice, Password=pass123, Role=Patient
3. Click Register

**Expected Result:** Redirect to login page with success message.

---

### Test Case 2: Doctor Registration

1. Go to `/register`
2. Fill: Name=Dr. Sarah, Username=dr_sarah, Password=doc123, Role=Doctor, Specialization=Cardiology
3. Click Register

**Expected Result:** Redirect to login page with success message. Specialization field appears only when Doctor role is selected.

---

### Test Case 3: Login & Role-Based Dashboard

1. Login as `admin` / `admin123` — Home shows: Total Users, Doctors, Patients, Reports, Blocks, Active Shares
2. Logout → Login as `dr_ahmed` / `doctor123` — Home shows: Reports Uploaded, Patients Served, Shared With Me
3. Logout → Login as `patient1` / `patient123` — Home shows: My Reports, Active Shares, Doctors

**Expected Result:** Each role sees its own dashboard with relevant statistics and quick actions.

---

### Test Case 4: Doctor Uploads Report

1. Login as `dr_ahmed` / `doctor123`
2. Click **Upload Report** in navbar
3. Select patient: Asiya Ali
4. Type: Blood Test, Title: "Liver Function Test", Description: "All values normal"
5. Upload a PDF file
6. Click **Upload & Record on Blockchain**

**Expected Result:** Report saved, success message shown, new block added to blockchain.

---

### Test Case 5: Patient Views Reports

1. Login as `patient1` / `patient123`
2. Click **My Reports** in navbar
3. View list of reports (3 seeded + any new uploads)
4. Click **View** on any report

**Expected Result:** Report details shown with doctor's notes, file hash (SHA-256), and blockchain activity.

---

### Test Case 6: Patient Shares Report with Doctor

1. Login as `patient1` / `patient123`
2. Click **My Reports** → Click **Share** on any report
3. Select a doctor from the dropdown → Click **Grant Access**

**Expected Result:** Access granted, success message. Doctor now appears in the "Current Access" table. New blockchain block created.

---

### Test Case 7: Patient Revokes Access

1. On the Share page, click **Revoke** next to the doctor's name

**Expected Result:** Access revoked, success message. Doctor removed from access list. Revocation recorded on blockchain.

---

### Test Case 8: Doctor Views Shared Reports

1. Login as the doctor who was granted access
2. Click **Patient Reports** in navbar
3. "Reports Shared With You" section shows the shared report

**Expected Result:** Shared reports appear under the "Shared With You" section. After revocation, they disappear.

---

### Test Case 9: Blockchain Explorer

1. Login as any user
2. Click **Blockchain** in navbar
3. View the chain of blocks with hashes, timestamps, and actions

**Expected Result:** Chain displayed with connected blocks, genesis block at top. Each block shows block hash, previous hash, and data hash.

---

### Test Case 10: Blockchain Integrity Verification

1. On the Blockchain page, click **Verify Chain Integrity**

**Expected Result:** Success message: "Blockchain is VALID. All X blocks verified successfully."

---

### Test Case 11: Audit Trail (Admin Only)

1. Login as `admin` / `admin123`
2. Click **Audit Trail** in navbar
3. View table of all system actions

**Expected Result:** Table shows all actions (uploads, grants, revocations, views) with user name, role, action type, details, and timestamp.

---

### Test Case 12: Dashboard Analytics

1. Click **Dashboard** in navbar
2. View 4 charts:
   - Reports by Type (pie chart)
   - Reports Over Time (line chart)
   - User Distribution (doughnut chart)
   - Access Grants (bar chart)

**Expected Result:** All 4 charts render with correct data from the database.

---

### Test Case 13: About Page

1. Click **About** in navbar
2. View: Project overview, how blockchain works (4-step visual), key features, blockchain actions table, tech stack, user roles, security features

**Expected Result:** Complete project information displayed.

---

### Test Case 14: Report Integrity Check

1. View any report (click **View** from reports list)
2. Check the right sidebar for SHA-256 file hash
3. Check the blockchain activity section

**Expected Result:** File hash displayed. Blockchain records show upload and view actions for this report.

---

### Test Case 15: Access Isolation

1. Register a new doctor (e.g., `dr_new` / `pass123`)
2. Login as `dr_new` → Click Patient Reports
3. Both sections (Uploaded and Shared) should be empty
4. Login as `patient1` → Share a report with `dr_new`
5. Login as `dr_new` → Patient Reports now shows the shared report
6. Login as `patient1` → Revoke access from `dr_new`
7. Login as `dr_new` → Shared report is gone

**Expected Result:** Strict access control enforced. Doctors only see reports they uploaded or that were explicitly shared with them.

---

### Test Case 16: Admin Global Statistics

1. Login as `admin` / `admin123`
2. Home page shows global counts across all users
3. Perform actions (upload reports, register users) with other accounts
4. Login as admin again — counts should be updated

**Expected Result:** Admin sees accurate system-wide statistics.

---

## Notes

- SQLite database (`medical_blockchain.db`) is auto-created on first run — no setup needed
- Admin account (`admin`/`admin123`) is seeded automatically
- Sample doctor (`dr_ahmed`/`doctor123`) and patient (`patient1`/`patient123`) are seeded
- 3 sample medical reports are seeded with blockchain entries
- Passwords are hashed using Werkzeug (not stored in plain text)
- Blockchain genesis block is created automatically on first run
- Uploaded files are stored in `static/uploads/` with timestamp prefix
- File integrity is verified using SHA-256 hashing stored on blockchain
- To reset all data, delete `medical_blockchain.db` and `static/uploads/` contents, then restart
