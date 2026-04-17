# PROJECT EXPLANATION — Medical Report Management & Distribution System Using Blockchain

This document explains the entire project in simple terms so that even a 7th-grader can understand how it works.

---

## What Does This Project Do?

Imagine you go to the hospital and the doctor runs some tests on you — like a blood test or an X-ray. The results come as a **medical report**. Right now, these reports are usually stored on paper or on a hospital's computer. But what if:

- The hospital's computer gets hacked and someone changes your report?
- You need to show your report to a different doctor at another hospital?
- Someone sees your private health information without your permission?

This project solves all these problems using a technology called **blockchain**.

**MedChain** is a website where:
1. **Doctors** can upload medical reports for their patients
2. **Patients** can view their own reports and choose which doctors can see them
3. **Every action** is recorded on a blockchain — a digital record book that nobody can change or delete

---

## What is Blockchain? (Simple Explanation)

Think of blockchain as a **chain of locked boxes**.

- Each box is called a **block**
- Each block contains some information (like "Dr. Ahmed uploaded a blood test for patient Asiya")
- Each block also has a **unique code** (called a hash) — like a fingerprint
- Each block remembers the fingerprint of the **previous box**
- This creates a **chain** — if anyone tries to change one box, the fingerprint changes, and the whole chain breaks!

This is why blockchain is called **tamper-proof** — you can't change old records without everyone knowing.

### Real-World Example

Imagine a notebook where:
1. On Page 1, you write: "Started the record book" (this is the Genesis Block)
2. On Page 2, you write: "Dr. Ahmed uploaded a blood test for Asiya" and you also write down a code from Page 1
3. On Page 3, you write: "Asiya shared her blood test with Dr. Sarah" and you write down a code from Page 2

If someone tears out Page 2 and replaces it, the code on Page 3 won't match anymore — so you'll know something was changed!

That's exactly how blockchain works in this project.

---

## Who Uses This System?

There are **3 types of users** (called roles):

### 1. Patient
- Can **view** their own medical reports
- Can **share** reports with specific doctors (grant access)
- Can **revoke** access from doctors anytime
- Can see the **blockchain** to verify nothing was tampered with
- **Cannot** upload reports or see other patients' data

### 2. Doctor
- Can **upload** medical reports for patients (blood tests, X-rays, prescriptions, etc.)
- Can **view** reports they uploaded
- Can **view** reports that patients shared with them
- **Cannot** see reports they weren't given permission to view

### 3. Admin (Hospital Administrator)
- Can see **statistics** about the whole system (total users, reports, etc.)
- Can view the **audit trail** (a log of every action taken in the system)
- Can check if the **blockchain** is still valid
- **Cannot** upload or modify medical reports

---

## How Does Each Feature Work?

### Registration and Login

When someone wants to use the system, they first **register** by entering their:
- Full name
- Username (must be unique)
- Password (stored securely — not as plain text!)
- Role (Patient or Doctor)
- If Doctor: their specialization (Cardiology, Neurology, etc.)

After registering, they can **login** with their username and password. The system checks the password using a special security method called **hashing** — the actual password is never stored in the database, only a scrambled version of it.

### Uploading a Report (Doctor)

When a doctor uploads a report:
1. The doctor selects the patient, enters the report title and type, and uploads the file (PDF or image)
2. The system calculates a **SHA-256 hash** of the file — this is a unique 64-character code that represents the file's exact contents
3. The report is saved in the database
4. A new **block** is added to the blockchain recording: who uploaded it, for which patient, and the file hash
5. An entry is added to the **audit log**

### Viewing Reports (Patient)

When a patient clicks "My Reports":
1. The system fetches all reports where this patient is the owner
2. Shows a table with: report title, type, doctor name, date
3. Patient can click "View" to see full details including the file hash and blockchain activity
4. Every view action is also recorded on the blockchain!

### Sharing Reports (Patient)

This is one of the most important features — **the patient controls who sees their data**.

When a patient wants to share a report with a different doctor:
1. Patient clicks "Share" on a report
2. A list of all registered doctors appears
3. Patient selects a doctor and clicks "Grant Access"
4. The system creates an **access grant** in the database
5. A new block is added to the blockchain: "Patient X shared Report Y with Doctor Z"
6. Now that doctor can see this report in their "Patient Reports" page

If the patient changes their mind:
1. They click "Revoke" next to the doctor's name
2. The access grant is deactivated
3. A block is added to the blockchain: "Patient X revoked Doctor Z's access to Report Y"
4. The doctor can no longer see this report

### Blockchain Explorer

Anyone logged in can visit the Blockchain Explorer page to see the full chain:
- Every block is displayed as a card
- Shows: block number, timestamp, action type, block hash, previous hash
- Blocks are connected visually with arrows showing the chain
- The Genesis Block (Block #0) is shown in green — it's the first block created when the system started

### Blockchain Verification

Users can click "Verify Chain Integrity" to check if the blockchain is still valid:
1. The system goes through every block one by one
2. It recalculates each block's hash and compares it with the stored hash
3. It checks that each block's "previous hash" matches the actual hash of the previous block
4. If everything matches → "Blockchain is VALID"
5. If anything is wrong → "Blockchain is INVALID" with details of what broke

### Audit Trail (Admin Only)

The admin can see a complete log of everything that happened in the system:
- Who registered
- Who uploaded which report
- Who shared reports with whom
- Who revoked access
- Who viewed which reports
- Who verified the blockchain

Each entry shows: timestamp, user name, user role, action type, and details.

### Dashboard

The Dashboard page shows 4 charts:
1. **Reports by Type** (pie chart) — how many blood tests, X-rays, MRI scans, etc.
2. **Reports Over Time** (line chart) — how many reports were uploaded each day
3. **User Distribution** (doughnut chart) — how many patients, doctors, and admins
4. **Access Grants** (bar chart) — how many active vs. revoked access grants

---

## How is Data Stored?

The system uses a **SQLite database** — a simple file-based database that doesn't need any special software to install.

There are 5 tables:

| Table | What It Stores |
|-------|---------------|
| `users` | All registered users (name, username, hashed password, role) |
| `medical_reports` | All medical reports (title, type, file path, file hash, patient, doctor) |
| `access_grants` | Who has permission to see which reports |
| `blockchain` | The blockchain — every block with its hashes and data |
| `audit_log` | A log of every action taken in the system |

---

## What is SHA-256 Hashing?

SHA-256 is a mathematical function that takes any input (like a file) and produces a fixed-length 64-character code called a **hash**.

**Important properties:**
- The same input always gives the same hash
- Even a tiny change in the input gives a completely different hash
- You cannot reverse a hash back to the original input
- Two different inputs will (practically) never give the same hash

**Example:**
- Input: "Hello World" → Hash: `a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e`
- Input: "Hello World!" (added one `!`) → Hash: `7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069`

See how completely different they are? That's why it's perfect for detecting if a file was changed.

In our system, when a doctor uploads a blood test report, the system calculates the SHA-256 hash of that file and stores it on the blockchain. Later, if anyone wants to verify that the report hasn't been changed, they can recalculate the hash and compare it with the one on the blockchain.

---

## What Technologies Are Used?

| Technology | What It Does |
|-----------|-------------|
| **Python** | The programming language used to write the backend |
| **Flask** | A web framework that handles web pages, forms, and routes |
| **SQLite** | A lightweight database to store all data |
| **SHA-256** | A hashing algorithm for file integrity and blockchain |
| **Werkzeug** | A library for securely hashing passwords |
| **Bootstrap 5** | A CSS framework for making the website look professional |
| **Chart.js** | A JavaScript library for creating charts on the dashboard |
| **Docker** | A tool to package the entire app into a container for easy deployment |
| **HTML/CSS/JS** | Standard web technologies for the user interface |

---

## Security Measures

1. **Password Hashing** — Passwords are never stored as plain text. They are hashed using Werkzeug's `generate_password_hash()` function.

2. **Session-Based Authentication** — When you login, a session is created. Every page checks if you have a valid session before showing data.

3. **Role-Based Access Control** — Patients can only see their own reports. Doctors can only see reports they uploaded or were granted access to. Admin sees system-wide data.

4. **Parameterized SQL Queries** — All database queries use parameters (? placeholders) instead of string concatenation, which prevents SQL injection attacks.

5. **File Type Validation** — Only PDF, PNG, JPG, and JPEG files can be uploaded. Other file types are rejected.

6. **Blockchain Integrity** — Every action is recorded on an immutable blockchain. If someone directly modifies the database, the blockchain verification will detect it.

7. **Audit Trail** — Every action is logged, providing full accountability.

---

## Step-by-Step: How to Use the System

### As a Doctor:
1. Login with `dr_ahmed` / `doctor123`
2. Click "Upload Report" in the navigation bar
3. Select the patient, choose report type, enter title and notes
4. Upload the report file (PDF or image)
5. Click "Upload & Record on Blockchain"
6. The report is now saved and secured on the blockchain!

### As a Patient:
1. Login with `patient1` / `patient123`
2. Click "My Reports" to see all your medical reports
3. Click "View" on any report to see full details and blockchain verification
4. Click "Share" to give another doctor access to your report
5. You can "Revoke" access anytime — the doctor will no longer see that report

### As an Admin:
1. Login with `admin` / `admin123`
2. Home page shows system-wide statistics
3. Click "Blockchain" to see the full chain of recorded actions
4. Click "Audit Trail" to see a log of everything that happened
5. Click "Dashboard" for analytics and charts

---

## What Makes This Project Special?

1. **Patient-Centric** — The patient controls who sees their medical data, not the hospital
2. **Tamper-Proof** — The blockchain ensures no one can silently change medical records
3. **Transparent** — Every action is logged and verifiable
4. **Decentralized Concept** — Even though this demo uses a single database, the blockchain design demonstrates how data integrity works in real-world decentralized systems
5. **Complete Audit Trail** — Full accountability for all users
6. **Simple Yet Powerful** — Built with standard web technologies but demonstrates advanced security concepts

---

## Frequently Asked Questions

**Q: Is this a real blockchain like Bitcoin or Ethereum?**
A: No. This is a **simulated blockchain** that demonstrates the core concepts (hashing, block linking, chain verification) using Python and SQLite. Real blockchains are distributed across many computers (nodes), but the security principles are the same.

**Q: Can patients upload reports?**
A: No. Only doctors can upload reports. This ensures that medical reports come from verified medical professionals.

**Q: What happens if I delete the database file?**
A: The system will create a new database with the default admin, doctor, and patient accounts plus sample reports. All previous data will be lost.

**Q: What file types can be uploaded?**
A: PDF, PNG, JPG, and JPEG files only.

**Q: How is this different from just storing reports in a regular database?**
A: A regular database can be changed by anyone with access. With blockchain, every change is recorded and linked to previous records. If anyone tries to modify a report, the blockchain verification will detect the tampering.
