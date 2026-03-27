# House Price Prediction Using Machine Learning

A machine learning-powered web application that predicts California housing prices using Gradient Boosting regression trained on geographic, demographic, and economic features.

## Features

- **Price Prediction** — Enter 9 housing features to get an instant price estimate
- **Multiple ML Models** — 5 models trained and compared (Linear Regression, Ridge, Decision Tree, Random Forest, Gradient Boosting)
- **EDA Visualizations** — 7 data analysis charts (price distribution, correlation heatmap, feature importance, geographic price map, model comparison)
- **Prediction History** — Per-user history of all predictions with input details
- **Model Dashboard** — Side-by-side comparison of all models with R², MAE, MSE, RMSE metrics
- **User Authentication** — Login/register with password hashing
- **Dark Theme UI** — Bootstrap 5 dark gradient design

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python + Flask |
| Frontend | Jinja2 Templates + Bootstrap 5 |
| Database | SQLite |
| ML Library | scikit-learn |
| Data Analysis | pandas + NumPy |
| Visualization | matplotlib + seaborn |
| Authentication | Werkzeug (PBKDF2-SHA256) |
| Container | Docker |

## Project Structure

```
code/
├── app.py                    # Flask application
├── generate_dataset.py       # Synthetic dataset generator
├── train_model.py            # Model training + EDA visualization
├── housing_model.pkl         # Trained Gradient Boosting model
├── models_info.json          # Model metrics and feature config
├── housing.csv               # Training dataset (10,000 rows)
├── templates/
│   ├── base.html             # Dark theme layout + navbar
│   ├── login.html            # Login page
│   ├── register.html         # Registration page
│   ├── home.html             # Dashboard
│   ├── predict.html          # Prediction form + results
│   ├── history.html          # Prediction history
│   ├── visualize.html        # EDA visualizations
│   ├── dashboard.html        # Model comparison
│   └── about.html            # Project info
├── static/vis/               # EDA chart images
├── Dockerfile
├── README.md
└── PROJECT_EXPLANATION.md
```

## Installation (Windows)

### Prerequisites

- **Python 3.8 or higher** — Download from [https://python.org](https://python.org)
- **Git** — Download from [https://git-scm.com](https://git-scm.com)

### Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd code
   ```

2. **Install dependencies:**
   ```bash
   pip install flask scikit-learn pandas numpy matplotlib seaborn joblib werkzeug
   ```

3. **Generate dataset and train model:**
   ```bash
   python generate_dataset.py
   python train_model.py
   ```

4. **Start the application:**
   ```bash
   python app.py
   ```

5. **Open in browser:**
   ```
   http://127.0.0.1:5005
   ```

### Demo Login

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |

## Docker Setup

```bash
docker build -t house-price .
docker run -p 5005:5005 house-price
```

Open `http://127.0.0.1:5005` in your browser.

## Input Features

| Feature | Description | Range |
|---------|-------------|-------|
| Longitude | Geographic longitude | -124.35 to -114.31 |
| Latitude | Geographic latitude | 32.54 to 41.95 |
| Housing Median Age | Median age of houses | 1 to 52 years |
| Total Rooms | Total rooms in census block | 1 to 40,000 |
| Total Bedrooms | Total bedrooms in census block | 1 to 7,000 |
| Population | Block population | 1 to 35,000 |
| Households | Number of households | 1 to 6,100 |
| Median Income | Median income (tens of thousands $) | 0.5 to 15.0 |
| Ocean Proximity | Location relative to ocean | 5 categories |

## Model Performance

| Model | R² Score | MAE ($) | RMSE ($) |
|-------|----------|---------|----------|
| Linear Regression | 0.8456 | 24,237 | 30,278 |
| Ridge Regression | 0.8456 | 24,237 | 30,278 |
| Decision Tree | 0.8457 | 23,857 | 30,263 |
| Random Forest | 0.8826 | 21,193 | 26,398 |
| **Gradient Boosting** | **0.8924** | **20,267** | **25,273** |

## Test Cases

### Test Case 1: User Registration
1. Go to `/register`, fill Name=Alice, Username=alice, Password=pass123
2. Click Register
- **Expected:** Redirect to login with success message

### Test Case 2: Login
1. Go to `/login`, enter admin / admin123
- **Expected:** Redirect to dashboard

### Test Case 3: Dashboard
1. Login → see dashboard with prediction count and recent predictions
- **Expected:** Stats cards and recent predictions table displayed

### Test Case 4: Predict House Price
1. Go to `/predict`
2. Fill: Longitude=-122.23, Latitude=37.88, Age=41, Rooms=880, Bedrooms=129, Population=322, Households=126, Income=8.33, Ocean=NEAR BAY
3. Click Predict
- **Expected:** Predicted price displayed (approximately $296,000)

### Test Case 5: Predict with Different Locations
1. Predict with INLAND, Income=2.5 → lower price (~$85,000)
2. Predict with NEAR BAY, Income=8.33 → higher price (~$296,000)
- **Expected:** Prices reflect location and income differences

### Test Case 6: Prediction History
1. After making several predictions, go to `/history`
- **Expected:** Table showing all past predictions with inputs and prices

### Test Case 7: EDA Visualizations
1. Go to `/visualize`
- **Expected:** 7 charts: price distribution, correlation heatmap, feature importance, ocean proximity, geographic map, model comparison, income vs price

### Test Case 8: Model Dashboard
1. Go to `/dashboard`
- **Expected:** Cards and table showing all 5 models with R², MAE, MSE, RMSE. Gradient Boosting marked as best.

### Test Case 9: About Page
1. Go to `/about`
- **Expected:** Project info, tech stack, features list, ML explanation

### Test Case 10: Invalid Login
1. Try logging in with wrong credentials
- **Expected:** Error message "Invalid username or password"

### Test Case 11: Duplicate Registration
1. Try registering with existing username "admin"
- **Expected:** Error message "Username already exists"

### Test Case 12: Access Control
1. Logout → try accessing `/predict` directly
- **Expected:** Redirect to login page

### Test Case 13: Admin Stats
1. Login as admin → dashboard shows total users and total predictions
- **Expected:** Admin section visible with system-wide statistics

### Test Case 14: Form Validation
1. Submit prediction form with empty fields
- **Expected:** Browser validation prevents submission

### Test Case 15: Multiple Users
1. Register as new user → make predictions → check history
- **Expected:** Only that user's predictions shown

### Test Case 16: Docker Deployment
1. `docker build -t house-price .`
2. `docker run -p 5005:5005 house-price`
- **Expected:** App accessible at http://127.0.0.1:5005

## Notes

- The SQLite database (`housing.db`) is auto-created on first run with an admin account
- Delete `housing.db` and restart to reset all data
- The model is pre-trained and saved as `housing_model.pkl` — no training needed at runtime
- Run `generate_dataset.py` and `train_model.py` to regenerate the dataset and retrain models
