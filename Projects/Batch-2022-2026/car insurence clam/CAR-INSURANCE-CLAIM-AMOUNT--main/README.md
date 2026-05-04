# C11 — Car Insurance Claim Prediction Using Machine Learning

## Project Structure

```
code/
├── app.py                          # Main Flask application
├── generate_dataset.py             # Synthetic dataset generator
├── train_model.py                  # ML model training + EDA visualizations
├── claim_model.pkl                 # Trained Gradient Boosting model
├── encoders.pkl                    # Label encoders for categorical features
├── models_info.json                # Model performance metrics
├── Car_Insurance_Claim.csv         # Dataset (10,000 records)
├── insurance.db                    # SQLite database (auto-created)
├── Dockerfile                      # Docker container configuration
├── .dockerignore                   # Docker ignore file
├── static/
│   └── vis/                        # EDA visualization charts (10 charts)
│       ├── age.png                 # Age vs Outcome
│       ├── gender.png              # Gender vs Outcome
│       ├── drive.png               # Driving Experience vs Outcome
│       ├── vtype.png               # Vehicle Type vs Outcome
│       ├── edu.png                 # Education vs Outcome
│       ├── vyear.png               # Vehicle Year vs Outcome
│       ├── income.png              # Income vs Outcome
│       ├── correlation.png         # Feature Correlation Heatmap
│       ├── outcome_dist.png        # Outcome Distribution Pie Chart
│       └── feature_importance.png  # Random Forest Feature Importance
└── templates/
    ├── base.html                   # Base layout (navbar, Bootstrap 5, dark theme)
    ├── home.html                   # Home page with stats and quick actions
    ├── login.html                  # Login page
    ├── register.html               # Registration page
    ├── predict.html                # Prediction form (17 features)
    ├── history.html                # Prediction history table
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
http://127.0.0.1:5002
```

The SQLite database (`insurance.db`) is auto-created on first run with an admin user.

---

## Docker Setup (Windows)

### Prerequisites

- Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
- Make sure Docker Desktop is running
- Run Steps 3 and 4 above first to generate `claim_model.pkl` and visualizations

### Build and Run

**Step 1:** Open Command Prompt and navigate to project

```bash
cd code
```

**Step 2:** Build the Docker image

```bash
docker build -t insurance-claim .
```

**Step 3:** Run the container

```bash
docker run -d -p 5002:5002 --name insurance-app insurance-claim
```

**Step 4:** Open in browser

```
http://localhost:5002
```

### Docker Management Commands

```bash
# Stop the container
docker stop insurance-app

# Start the container again
docker start insurance-app

# Remove the container
docker rm -f insurance-app

# View logs
docker logs insurance-app

# Rebuild after code changes
docker rm -f insurance-app
docker build -t insurance-claim .
docker run -d -p 5002:5002 --name insurance-app insurance-claim
```

---

## Accounts

| Role | Username | Password | Access |
|---|---|---|---|
| Admin | `admin` | `admin123` | Home (global stats), Predict, History, Visualize, Dashboard, About |
| User | (register) | (register) | Home, Predict, History, Visualize, Dashboard, About |

## Pages Overview

| Page | URL | Description |
|---|---|---|
| Login | `/login` | Login with credentials |
| Register | `/register` | Create a new account |
| Home | `/home` | Stats, recent predictions, quick actions |
| Predict | `/predict` | Enter customer details for claim prediction |
| History | `/history` | View all past prediction results |
| Visualize | `/visualize` | EDA charts (Gender, Age, Vehicle, etc.) |
| Dashboard | `/dashboard` | Model comparison and analytics charts |
| About | `/about` | Feature details, tech stack, model info |

---

## Model Performance

| Model | Accuracy | Precision | Recall | F1 Score |
|---|---|---|---|---|
| **Gradient Boosting** | **91.95%** | 86.93% | 77.31% | 83.49% |
| SVM | 91.1% | 86.72% | 78.08% | 82.2% |
| Logistic Regression | 90.25% | 83.17% | 77.69% | 80.48% |
| Random Forest | 90.1% | 84.9% | 74.62% | 79.5% |

## Dataset Features (17)

| Feature | Type | Description |
|---|---|---|
| AGE | Categorical | Age group (16-25, 26-39, 40-64, 65+) |
| GENDER | Categorical | Male / Female |
| RACE | Categorical | Majority / Minority |
| DRIVING_EXPERIENCE | Categorical | Years of driving (0-9y, 10-19y, 20-29y, 30y+) |
| EDUCATION | Categorical | None / High School / University |
| INCOME | Categorical | Poverty / Working Class / Middle Class / Upper Class |
| CREDIT_SCORE | Numeric | Credit score (0.0 to 1.0) |
| VEHICLE_OWNERSHIP | Binary | 0 = No, 1 = Yes |
| VEHICLE_YEAR | Categorical | Before 2015 / After 2015 |
| MARRIED | Binary | 0 = No, 1 = Yes |
| CHILDREN | Binary | 0 = No, 1 = Yes |
| POSTAL_CODE | Numeric | Area postal code |
| ANNUAL_MILEAGE | Numeric | Annual kilometers driven |
| VEHICLE_TYPE | Categorical | Sedan / Sports Car |
| SPEEDING_VIOLATIONS | Numeric | Number of speeding violations (0-5) |
| DUIS | Numeric | Number of DUI incidents (0-3) |
| PAST_ACCIDENTS | Numeric | Number of past accidents (0-5) |

---

## Quick Start

1. Open browser: `http://127.0.0.1:5002`
2. Click "Register" → Name: `John`, Username: `john`, Password: `pass123`
3. Login with same credentials
4. Click **Predict** → Fill in customer details → Click **Predict Claim**
5. View prediction result with confidence score

---

## Test Cases

### Test Case 1: High-Risk Young Driver (Claim Likely)

| Field | Value |
|---|---|
| Age | 16-25 |
| Gender | male |
| Race | majority |
| Driving Experience | 0-9y |
| Education | high school |
| Income | working class |
| Credit Score | 0.3 |
| Vehicle Ownership | Yes |
| Vehicle Year | after 2015 |
| Married | No |
| Children | No |
| Postal Code | 10238 |
| Annual Mileage | 18000 |
| Vehicle Type | sports car |
| Speeding Violations | 4 |
| DUIs | 2 |
| Past Accidents | 3 |

**Expected Result:** Claim Likely (~99% confidence)

**Why:** Young driver (16-25), minimal experience (0-9y), sports car, 4 speeding violations, 2 DUIs, 3 past accidents, and low credit score (0.3) — all high-risk indicators.

---

### Test Case 2: Low-Risk Experienced Driver (No Claim)

| Field | Value |
|---|---|
| Age | 40-64 |
| Gender | female |
| Race | majority |
| Driving Experience | 20-29y |
| Education | university |
| Income | middle class |
| Credit Score | 0.85 |
| Vehicle Ownership | Yes |
| Vehicle Year | after 2015 |
| Married | Yes |
| Children | Yes |
| Postal Code | 10065 |
| Annual Mileage | 10000 |
| Vehicle Type | sedan |
| Speeding Violations | 0 |
| DUIs | 0 |
| Past Accidents | 0 |

**Expected Result:** No Claim Expected (~99% confidence)

**Why:** Experienced driver (20-29y), mature age (40-64), sedan, zero violations, zero DUIs, zero accidents, high credit score (0.85) — all low-risk indicators.

---

### Test Case 3: Senior Driver with DUI History (Claim Likely)

| Field | Value |
|---|---|
| Age | 65+ |
| Gender | male |
| Race | minority |
| Driving Experience | 30y+ |
| Education | high school |
| Income | working class |
| Credit Score | 0.45 |
| Vehicle Ownership | Yes |
| Vehicle Year | before 2015 |
| Married | Yes |
| Children | No |
| Postal Code | 10007 |
| Annual Mileage | 8000 |
| Vehicle Type | sedan |
| Speeding Violations | 2 |
| DUIs | 2 |
| Past Accidents | 3 |

**Expected Result:** Claim Likely (~93% confidence)

**Why:** Despite extensive experience (30y+), the combination of 2 DUIs, 3 past accidents, 2 speeding violations, older vehicle, and low credit score pushes the risk prediction toward claim.

---

### Test Case 4: Responsible Middle-Aged Driver (No Claim)

| Field | Value |
|---|---|
| Age | 26-39 |
| Gender | female |
| Race | majority |
| Driving Experience | 10-19y |
| Education | university |
| Income | upper class |
| Credit Score | 0.92 |
| Vehicle Ownership | Yes |
| Vehicle Year | after 2015 |
| Married | Yes |
| Children | Yes |
| Postal Code | 10022 |
| Annual Mileage | 12000 |
| Vehicle Type | sedan |
| Speeding Violations | 0 |
| DUIs | 0 |
| Past Accidents | 1 |

**Expected Result:** No Claim Expected (~99% confidence)

**Why:** University-educated, high income, excellent credit score (0.92), sedan, zero violations/DUIs, and only 1 minor past accident — very low-risk profile.

---

### Test Case 5: High-Risk Profile (Claim Likely)

| Field | Value |
|---|---|
| Age | 16-25 |
| Gender | male |
| Race | minority |
| Driving Experience | 0-9y |
| Education | none |
| Income | poverty |
| Credit Score | 0.2 |
| Vehicle Ownership | No |
| Vehicle Year | before 2015 |
| Married | No |
| Children | No |
| Postal Code | 10032 |
| Annual Mileage | 20000 |
| Vehicle Type | sports car |
| Speeding Violations | 3 |
| DUIs | 1 |
| Past Accidents | 2 |

**Expected Result:** Claim Likely (~99% confidence)

**Why:** Youngest age group, no experience, sports car, multiple violations, DUI, past accidents, very low credit score, high annual mileage — maximum risk profile.

---

### Test Case 6: View Prediction History

1. After running Test Cases 1-5, click **History** in navbar
2. View the table with all past predictions

**Expected:** Table shows customer details (Age, Gender, Experience, Vehicle, Violations), prediction badge (Claim Likely / No Claim), confidence percentage, and date for each prediction.

---

### Test Case 7: Data Visualizations

1. Click **Visualize** in navbar
2. View 10 EDA charts:
   - Gender vs Outcome
   - Driving Experience vs Outcome
   - Vehicle Type vs Outcome
   - Education vs Outcome
   - Vehicle Year vs Outcome
   - Age Group vs Outcome
   - Income vs Outcome
   - Correlation Heatmap
   - Outcome Distribution
   - Feature Importance

**Expected:** All 10 charts display correctly showing the relationship between features and claim outcomes.

---

### Test Case 8: Dashboard Analytics

1. Click **Dashboard** in navbar
2. View Model Performance Comparison table (Gradient Boosting, Random Forest, SVM, Logistic Regression)
3. View charts: Accuracy Comparison, F1 Score, Prediction Distribution, Confidence Distribution
4. View Feature Importance chart

**Expected:** Gradient Boosting highlighted as best model (91.95%). Charts reflect actual prediction data from your session.

---

### Test Case 9: Admin Dashboard

1. Logout → Login as `admin` / `admin123`
2. Home page shows additional admin stats: Registered Users, Total Predictions (All Users), Total Claims Predicted
3. All other pages work the same

**Expected:** Admin sees global statistics across all users.

---

## Notes

- SQLite database (`insurance.db`) is auto-created on first run — no setup needed
- Admin account (`admin`/`admin123`) is seeded automatically
- Passwords are hashed using Werkzeug (not stored in plain text)
- Model files must exist before running the app — run `train_model.py` first
- 10 EDA visualizations are generated during training
- The dataset is synthetic (generated by `generate_dataset.py`) for demonstration
- To reset data, delete `insurance.db` and restart the app

## Team

| Roll Number | Name |
|-------------|------|
| 160922733142 | Shadman Ahmad |
| 160922733143 | Shaik Sufyaan Ahmed |
| 160922733147 | Syed Affan Hussain Syed Barey |
| 160922733151 | Syed Jawad |
