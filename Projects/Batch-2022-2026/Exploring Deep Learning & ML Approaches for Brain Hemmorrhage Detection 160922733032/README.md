# C16 — Exploring Deep Learning & ML Approaches for Brain Hemorrhage Detection

## Project Structure

```
code/
├── app.py                          # Main Flask application
├── generate_dataset.py             # Synthetic brain CT dataset generator
├── train_model.py                  # CNN + ML model training script
├── brain_cnn_model.pth             # Trained CNN model weights (PyTorch)
├── ml_model.pkl                    # Trained ML model (Random Forest)
├── models_info.json                # Model performance metrics
├── vulnerability_fix_dataset.csv   # (if present)
├── hemorrhage.db                   # SQLite database (auto-created)
├── Dockerfile                      # Docker container configuration
├── .dockerignore                   # Docker ignore file
├── dataset/                        # Generated training/test images
│   ├── train/
│   │   ├── hemorrhage/             # 400 hemorrhage CT images
│   │   └── normal/                 # 400 normal CT images
│   └── test/
│       ├── hemorrhage/             # 100 hemorrhage CT images
│       └── normal/                 # 100 normal CT images
├── static/
│   ├── uploads/                    # User-uploaded images
│   └── test_samples/               # 6 sample test images
└── templates/
    ├── base.html                   # Base layout (navbar, Bootstrap 5, dark theme)
    ├── home.html                   # Home page with stats and sample images
    ├── login.html                  # Login page
    ├── register.html               # Registration page
    ├── predict.html                # Upload CT image and get prediction
    ├── history.html                # Scan history table
    ├── dashboard.html              # Model comparison charts and analytics
    └── about.html                  # About page with architecture details
```

## Features

- **CNN Deep Learning Model:** 4-layer Convolutional Neural Network (PyTorch) achieving 99.5% accuracy
- **ML Model Comparison:** Random Forest (92%), SVM (86.5%), Logistic Regression (76.5%)
- **Image Upload & Analysis:** Upload brain CT scan and get instant hemorrhage prediction
- **Confidence Score:** Each prediction includes a percentage confidence level
- **Hemorrhage Types:** Detects subdural, intracerebral, and subarachnoid hemorrhages
- **Scan History:** All past analyses stored in SQLite database
- **Dashboard:** Model comparison charts, prediction distribution, confidence analytics
- **Sample Test Images:** 6 pre-generated test images (3 hemorrhage + 3 normal) for easy testing
- **User Authentication:** Secure login with password hashing (Werkzeug)
- **Admin Panel:** Admin user sees global stats (total users, total scans, hemorrhages found)

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
pip install flask torch torchvision pillow werkzeug scikit-learn
```

**Step 3:** Generate the dataset (first time only)

```bash
python generate_dataset.py
```

**Step 4:** Train the models (first time only)

```bash
python train_model.py
```

**Step 5:** Run the application

```bash
python app.py
```

**Step 6:** Open in browser

```
http://127.0.0.1:5001
```

The SQLite database (`hemorrhage.db`) is auto-created on first run with an admin user.

---

## Docker Setup (Windows)

### Prerequisites

- Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
- Make sure Docker Desktop is running
- Run Steps 3 and 4 above first to generate `brain_cnn_model.pth` and `models_info.json`

### Build and Run

**Step 1:** Open Command Prompt and navigate to project

```bash
cd code
```

**Step 2:** Build the Docker image

```bash
docker build -t brain-scan .
```

**Step 3:** Run the container

```bash
docker run -d -p 5001:5001 --name brain-app brain-scan
```

**Step 4:** Open in browser

```
http://localhost:5001
```

### Docker Management Commands

```bash
# Stop the container
docker stop brain-app

# Start the container again
docker start brain-app

# Remove the container
docker rm -f brain-app

# View logs
docker logs brain-app

# Rebuild after code changes
docker rm -f brain-app
docker build -t brain-scan .
docker run -d -p 5001:5001 --name brain-app brain-scan
```

---

## Accounts

| Role | Username | Password | Access |
|---|---|---|---|
| Admin | `admin` | `admin123` | Home (global stats), Analyze, History, Dashboard, About |
| User | (register) | (register) | Home, Analyze, History, Dashboard, About |

## Pages Overview

| Page | URL | Access | Description |
|---|---|---|---|
| Login | `/login` | Guest | Login with credentials |
| Register | `/register` | Guest | Create a new account |
| Home | `/home` | User | Stats, recent analyses, sample test images |
| Analyze Scan | `/predict` | User | Upload CT image for hemorrhage detection |
| History | `/history` | User | View all past scan results |
| Dashboard | `/dashboard` | User | Model comparison and analytics charts |
| About | `/about` | All | Architecture details, tech stack |

---

## Quick Start

1. Open browser: `http://127.0.0.1:5001`
2. Click "Register" → Name: `John`, Username: `john`, Password: `pass123`
3. Login with same credentials
4. On Home page, download a sample test image (hemorrhage or normal)
5. Click **Analyze Scan** → Upload the image → Click **Analyze Image**
6. View prediction result with confidence score

---

## Test Cases

### Test Case 1: User Registration and Login

1. Open http://127.0.0.1:5001
2. Click **Register**
3. Fill: Name: `Mohammed`, Username: `mohammed`, Password: `test123`
4. Click **Register** → redirects to Login
5. Enter `mohammed` / `test123` → Click **Login**

**Expected:** Redirects to Home page. Welcome message with stats shown.

---

### Test Case 2: Upload Hemorrhage CT Scan

1. Login as `mohammed` / `test123`
2. On Home page, download `sample_hemorrhage_1.png` from test samples
3. Click **Analyze Scan** in navbar
4. Upload `sample_hemorrhage_1.png`
5. Click **Analyze Image**

**Expected:** Result shows **"Hemorrhage Detected"** with a red badge and confidence near 100%. Warning message advises consulting a medical professional.

---

### Test Case 3: Upload Normal CT Scan

1. Login as any user
2. Download `sample_normal_1.png` from Home page test samples
3. Click **Analyze Scan** → Upload the image → Click **Analyze Image**

**Expected:** Result shows **"Normal (No Hemorrhage)"** with a green badge and confidence near 99%. Message confirms no hemorrhage patterns found.

---

### Test Case 4: Test All Sample Images

1. Login as any user
2. Upload each of the 6 sample images one by one:
   - `sample_hemorrhage_1.png` → Hemorrhage Detected
   - `sample_hemorrhage_2.png` → Hemorrhage Detected
   - `sample_hemorrhage_3.png` → Hemorrhage Detected
   - `sample_normal_1.png` → Normal (No Hemorrhage)
   - `sample_normal_2.png` → Normal (No Hemorrhage)
   - `sample_normal_3.png` → Normal (No Hemorrhage)

**Expected:** All 6 images classified correctly with high confidence scores.

---

### Test Case 5: View Scan History

1. After analyzing multiple images, click **History** in navbar
2. View the table with all past results

**Expected:** Table shows image thumbnail, prediction (Hemorrhage/Normal badge), confidence percentage, and scan date for each analysis.

---

### Test Case 6: Dashboard Analytics

1. After performing several scans, click **Dashboard**
2. View Model Performance Comparison table (CNN, Random Forest, SVM, Logistic Regression)
3. View charts: Model Accuracy, F1 Score, Prediction Distribution, Confidence Distribution

**Expected:** CNN shows highest accuracy (99.5%). Charts reflect actual scan data. Model comparison table shows all 4 models.

---

### Test Case 7: Admin Dashboard

1. Logout → Login as `admin` / `admin123`
2. Home page shows additional admin stats: Registered Users, Total Scans (All Users), Total Hemorrhages Found
3. Click **Dashboard** → same model comparison + analytics

**Expected:** Admin sees global statistics. Total scans and hemorrhage counts reflect all users' data.

---

### Test Case 8: Invalid File Upload

1. Login as any user
2. Click **Analyze Scan**
3. Try uploading a non-image file (e.g., `.txt` or `.pdf`)

**Expected:** Error message: "Invalid file type. Please upload PNG, JPG, JPEG, BMP, or TIF."

---

### Test Case 9: About Page

1. Click **About** in navbar
2. View hemorrhage types (Subdural, Intracerebral, Subarachnoid)
3. View CNN architecture details
4. View model accuracy progress bars

**Expected:** All sections display correctly. Model accuracies match dashboard values.

---

## Model Performance

| Model | Accuracy | Precision | Recall | F1 Score |
|---|---|---|---|---|
| CNN (Deep Learning) | 99.5% | 99.5% | 99.5% | 99.5% |
| Random Forest | 92.0% | 90.91% | 93.0% | 92.45% |
| SVM | 86.5% | 83.5% | 88.0% | 88.0% |
| Logistic Regression | 76.5% | 74.76% | 78.92% | 78.92% |

## CNN Architecture

```
Input (1x128x128 grayscale)
  → Conv2d(1, 32) + ReLU + MaxPool2d
  → Conv2d(32, 64) + ReLU + MaxPool2d
  → Conv2d(64, 128) + ReLU + MaxPool2d
  → Conv2d(128, 256) + ReLU + MaxPool2d
  → Flatten → Linear(256*8*8, 256) + ReLU + Dropout(0.5)
  → Linear(256, 1) + Sigmoid
  → Output (0=Hemorrhage, 1=Normal)
```

## Notes

- SQLite database (`hemorrhage.db`) is auto-created on first run — no setup needed
- Admin account (`admin`/`admin123`) is seeded automatically
- Passwords are hashed using Werkzeug (not stored in plain text)
- Model files (`brain_cnn_model.pth`, `ml_model.pkl`, `models_info.json`) must exist before running the app — run `train_model.py` first
- 6 sample test images are provided in `static/test_samples/` for easy testing
- The dataset is synthetic (generated by `generate_dataset.py`) for demonstration
- To reset data, delete `hemorrhage.db` and restart the app
- This tool is for educational purposes only — not for clinical diagnosis
