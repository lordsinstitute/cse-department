# Carbon Emission Prediction

A Flask web application that predicts vehicle CO2 emissions (g/km) using machine learning. Compares 6 regression algorithms and uses the best-performing model for real-time predictions based on vehicle specifications. Supports gasoline, diesel, hybrid, and electric vehicles with confidence intervals, carbon footprint calculator, multiple prediction modes, and a REST API.

## Features

- Predict CO2 emissions by entering vehicle specifications (make, class, engine size, weight, model year, fuel type, etc.)
- **Hybrid & Electric vehicle support** — EVs return zero tailpipe emissions; hybrids show reduced consumption
- **Confidence intervals** — 90% prediction range from model tree variance
- **Smart input validation** — Warns about impossible combinations (e.g., 12-cylinder compact, electric with engine)
- **Carbon Footprint Calculator** — Annual emissions in tonnes, monthly breakdown, trees needed to offset, comparison chart
- **Eco-friendly recommendations** — Actionable tips per prediction (switch to hybrid, smaller engine, etc.)
- **REST API** — `POST /api/predict`, `POST /api/validate`, and `POST /api/predict-live` for external integration
- **Quick Presets** — One-click predictions for 12 popular real-world vehicles (Toyota Camry, Honda Civic, Ford F-150, Tesla, BMW, etc.)
- **Vehicle Comparison** — Side-by-side comparison of up to 3 vehicles with visual bar charts and "Greenest" badge
- **Batch Prediction** — Upload CSV with multiple vehicles, get predictions for all, download results as CSV
- **Interactive Sliders** — Real-time prediction updates as you drag sliders (no submit button, 200ms debounce)
- CO2 rating system (1-10 scale) with color-coded environmental impact labels
- Model comparison dashboard with R², MAE, and RMSE metrics across 6 algorithms
- Prediction history with color-coded results
- Auto-fill vehicle specs when changing vehicle class
- Electric mode auto-zeros and locks engine/fuel fields
- User authentication (login/register)
- Chart.js interactive visualizations
- Dark theme UI with glassmorphic cards

## Algorithms Compared

| Algorithm | R² Score | MAE (g/km) | RMSE (g/km) |
|-----------|----------|------------|-------------|
| Linear Regression | 95.30% | 14.97 | 20.80 |
| Random Forest | 99.69% | 3.43 | 5.31 |
| Decision Tree | 99.27% | 4.80 | 8.22 |
| **XGBoost** | **99.72%** | **3.69** | **5.08** |
| AdaBoost | 96.83% | 14.18 | 17.08 |
| Lasso | 95.23% | 15.39 | 20.96 |

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

### macOS / Linux

```bash
git clone <repository-url>
cd code

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python3 generate_dataset.py    # Creates 7,000 vehicle records
python3 train_model.py         # Trains 6 models, saves best
python3 app.py                 # Starts on http://localhost:5012
```

### Windows

```bash
git clone <repository-url>
cd code

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python generate_dataset.py
python train_model.py
python app.py
```

Open http://localhost:5012 in your browser.

**Login:** Username: `admin`, Password: `admin123`

## Docker Deployment

```bash
docker build -t carbon-emission .
docker run -p 5012:5012 carbon-emission
```

## Input Features (11)

| Feature | Type | Range / Options |
|---------|------|-----------------|
| Make | Categorical | Toyota, Honda, Ford, BMW, Hyundai, Chevrolet, Nissan, Mercedes-Benz, Kia, Volkswagen |
| Model Year | Numeric | 2015 - 2025 |
| Vehicle Class | Categorical | Compact, Mid-size, SUV, Full-size, Pickup, Subcompact, Minicompact, Station wagon |
| Transmission | Categorical | Automatic, Manual, CVT |
| Fuel Type | Categorical | Regular Gasoline, Premium Gasoline, Diesel, Ethanol (E85), Hybrid, Electric |
| Engine Size | Numeric | 0.0 - 6.5 L (0 for Electric) |
| Cylinders | Numeric | 0 - 12 (0 for Electric) |
| Vehicle Weight | Numeric | 800 - 3000 kg |
| Fuel Consumption (City) | Numeric | 0.0 - 22.0 L/100km |
| Fuel Consumption (Highway) | Numeric | 0.0 - 16.0 L/100km |
| Fuel Consumption (Combined) | Numeric | 0.0 - 20.0 L/100km |

## CO2 Rating System

| Rating | CO2 Range | Label | Color |
|--------|-----------|-------|-------|
| 10 | 0 g/km (Electric) or < 120 g/km | Excellent | Green |
| 8-9 | 120 - 180 g/km | Excellent | Green |
| 6-7 | 180 - 250 g/km | Good | Lime |
| 4-5 | 250 - 350 g/km | Moderate | Yellow |
| 1-3 | > 350 g/km | High / Very High | Red |

## REST API

### POST /api/predict

Predict CO2 emissions from vehicle specifications.

**Request:**
```json
{
  "Make": "Toyota",
  "Vehicle_Class": "Compact",
  "Transmission": "CVT",
  "Fuel_Type": "Hybrid",
  "Engine_Size": 1.8,
  "Cylinders": 4,
  "Vehicle_Weight": 1400,
  "Model_Year": 2024,
  "Fuel_Consumption_City": 4.5,
  "Fuel_Consumption_Hwy": 4.0,
  "Fuel_Consumption_Comb": 4.3,
  "annual_km": 15000
}
```

**Response:**
```json
{
  "predicted_co2": 99.8,
  "unit": "g/km",
  "confidence_interval": { "low": 99.5, "high": 100.1 },
  "rating": 10,
  "rating_label": "Excellent",
  "warnings": [],
  "recommendations": [
    "Excellent! This is among the cleanest vehicles on the road.",
    "Great choice! Hybrid technology provides significant emission reductions."
  ],
  "carbon_footprint": {
    "annual_kg": 1497.0,
    "annual_tonnes": 1.5,
    "monthly_kg": 124.8,
    "trees_needed": 69
  }
}
```

### POST /api/predict-live

Lightweight real-time prediction for interactive sliders (no database save).

**Request:** Same as `/api/predict`

**Response:**
```json
{
  "co2": 163.1,
  "conf_low": 162.2,
  "conf_high": 164.0,
  "rating": 7,
  "label": "Good",
  "color": "#84cc16",
  "footprint": { "annual_kg": 2446.5, "annual_tonnes": 2.45, "monthly_kg": 203.9, "trees_needed": 112 },
  "warnings": [],
  "recommendations": []
}
```

### POST /api/validate

Validate input combinations without making a prediction.

**Request:**
```json
{
  "Vehicle_Class": "Compact",
  "Engine_Size": 5.0,
  "Cylinders": 8,
  "Vehicle_Weight": 2500,
  "Fuel_Type": "Regular Gasoline"
}
```

**Response:**
```json
{
  "valid": false,
  "warnings": [
    "Compact vehicles typically have 1.4-2.5L engines.",
    "Compact vehicles typically have 3-4 cylinders.",
    "Compact vehicles typically weigh 1000-1550 kg."
  ]
}
```

## Prediction Modes

| Mode | URL | Description |
|------|-----|-------------|
| Form Entry | `/predict` | Full form with all 11 vehicle specifications |
| Quick Presets | `/presets` | One-click predictions for 12 popular real-world vehicles |
| Compare Vehicles | `/compare` | Side-by-side comparison of up to 3 vehicles with preset auto-fill |
| Batch Upload | `/batch` | Upload CSV, get predictions for all rows, download results |
| Interactive Sliders | `/interactive` | Real-time prediction via range sliders with live updates |

## Pages

| Page | URL | Description |
|------|-----|-------------|
| Login | `/login` | User authentication |
| Register | `/register` | New user registration |
| Home | `/home` | Dashboard with stats, recent predictions, quick actions |
| Predict | `/predict` | Vehicle specs form with prediction results, confidence interval, recommendations, footprint |
| Quick Presets | `/presets` | 12 pre-defined vehicle cards with instant CO2, rating, and footprint |
| Compare | `/compare` | Side-by-side comparison of up to 3 vehicles with visual bar chart |
| Batch | `/batch` | CSV upload for bulk predictions with downloadable results |
| Interactive | `/interactive` | Slider-based real-time prediction with no submit button |
| Calculator | `/calculator` | Standalone carbon footprint calculator with comparison chart |
| History | `/history` | All past predictions with color-coded ratings |
| Dashboard | `/dashboard` | Model comparison charts (R², MAE, RMSE, rating distribution) |
| About | `/about` | Project info, v2 features, API docs, tech stack |

## Smart Validation Rules

| Scenario | Warning |
|----------|---------|
| Electric vehicle with engine > 0 | "Electric vehicles have no combustion engine" |
| Electric vehicle with cylinders > 0 | "Electric vehicles have no cylinders" |
| Electric vehicle with fuel > 0 | "Electric vehicles have zero fuel consumption" |
| Engine size outside class range | "Compact vehicles typically have 1.4-2.5L engines" |
| Cylinders outside class range | "SUV vehicles typically have 4-8 cylinders" |
| Weight outside class range | "Pickup vehicles typically weigh 1700-3000 kg" |

## Project Structure

```
code/
├── app.py                  # Flask web application (routes, prediction, API, 5 prediction modes)
├── train_model.py          # Model training (6 regressors, saves best)
├── generate_dataset.py     # Synthetic dataset generator (7,000 records, 12 columns)
├── templates/
│   ├── base.html           # Dark theme layout with navbar (Predict dropdown with 5 modes)
│   ├── login.html          # Login / Register
│   ├── home.html           # Dashboard overview
│   ├── predict.html        # CO2 prediction form + results + confidence + footprint
│   ├── presets.html        # Quick preset cards for 12 popular vehicles
│   ├── compare.html        # Side-by-side vehicle comparison (up to 3)
│   ├── batch.html          # CSV upload for bulk predictions
│   ├── interactive.html    # Real-time slider-based prediction
│   ├── calculator.html     # Standalone carbon footprint calculator
│   ├── history.html        # Prediction history table
│   ├── dashboard.html      # Model comparison charts
│   └── about.html          # Project info, v2 features, API reference
├── final_co2.csv           # Dataset (7,000 records, 12 columns)
├── best_model.pkl          # Trained best model (XGBoost)
├── encoders.pkl            # LabelEncoders for categorical features
├── scaler.pkl              # StandardScaler for numeric features
├── models_info.json        # Performance metrics for all 6 models
├── carbon_emissions.db     # SQLite database (users + predictions)
├── Dockerfile              # Docker container setup
├── requirements.txt        # Python dependencies
└── .gitignore
```

## Test Cases

### Authentication
1. Register new user → redirect to login page with success message
2. Register duplicate username → error "Username already taken"
3. Login as admin/admin123 → redirect to home
4. Invalid login → error "Invalid username or password"
5. Access /predict without login → redirect to login

### Prediction — Gasoline Vehicles
6. Compact car (1.5L, 4 cyl, 1200 kg) → low CO2 (~130-180 g/km), rating 7-9
7. SUV (3.5L, 6 cyl, 2000 kg) → moderate CO2 (~220-280 g/km), rating 4-5
8. Pickup (5.0L, 8 cyl, 2500 kg) → high CO2 (~300+ g/km), rating 1-3
9. Diesel vehicle → higher CO2 per litre factor applied
10. Prediction shows CO2 value, 90% confidence interval, rating, and color-coded label

### Prediction — Hybrid & Electric
11. Hybrid Compact (1.8L, 4 cyl, CVT) → ~40% lower CO2 than gasoline equivalent, rating 9-10
12. Electric vehicle → CO2 = 0.0 g/km, rating 10, "Zero tailpipe emissions"
13. Selecting Electric → engine/fuel fields auto-zero and lock
14. Switching back from Electric → fields unlock and restore defaults

### Smart Validation
15. Compact with 5.0L engine, 8 cyl → warning about engine/cylinder range
16. Electric with Engine_Size > 0 → warning "no combustion engine"
17. Electric with Cylinders > 0 → warning "no cylinders"
18. SUV with 800 kg weight → warning about weight range

### Carbon Footprint
19. Prediction result shows annual footprint (tonnes, monthly, trees to offset)
20. Calculator page: enter CO2 g/km + annual km → shows footprint + comparison chart
21. Electric vehicle → 0 tonnes, 0 trees
22. High-emission vehicle → large tree count, comparison bar shows red

### Recommendations
23. Gasoline SUV > 200 g/km → suggests Hybrid variant
24. Any vehicle > 250 g/km → suggests Electric alternative
25. Engine > 3.0L with high CO2 → suggests smaller engine
26. Electric vehicle → "Zero tailpipe emissions" + renewable charging tip
27. Hybrid < 150 g/km → "Great choice!" confirmation

### REST API
28. `POST /api/predict` with valid JSON → 200 with prediction, CI, rating, recommendations, footprint
29. `POST /api/predict` with missing fields → 400 with error listing missing fields
30. `POST /api/predict` with Electric → CO2 = 0.0, CI = 0.0-0.0
31. `POST /api/validate` with impossible combo → `valid: false` with warnings
32. `POST /api/validate` with valid combo → `valid: true`, empty warnings

### Quick Presets
33. Presets page shows 12 vehicle cards with CO2, rating, confidence interval, and footprint
34. Each card shows vehicle specs (engine, fuel, class, weight, transmission)
35. Cards link to form entry and comparison pages

### Vehicle Comparison
36. Compare up to 3 vehicles side-by-side
37. Load preset vehicles with one click or enter custom specs
38. Visual bar chart shows relative CO2 emissions
39. "Greenest" badge highlights the lowest-emission vehicle
40. Each vehicle shows CO2, rating, footprint, warnings, and recommendations

### Batch Prediction
41. Upload CSV file with multiple vehicle rows
42. Download sample CSV template with correct column headers
43. Results table shows CO2, confidence interval, and rating for each row
44. Download results as CSV
45. Summary stats show average, lowest, and highest CO2
46. Skipped rows (missing fields) shown as warnings

### Interactive Sliders
47. All 11 parameters adjustable via range sliders and dropdowns
48. Prediction updates in real-time (200ms debounce, no submit button)
49. Selecting Electric auto-disables and zeros engine/fuel sliders
50. Live display shows CO2, confidence interval, rating, footprint, warnings, and recommendations

### UI Features
51. Predict navbar item is a dropdown with 5 modes (Form, Presets, Compare, Batch, Interactive)
52. Selecting Vehicle Class auto-fills suggested engine/weight/cylinder midpoints
53. History page shows all predictions with color-coded ratings
54. Dashboard shows R², MAE, RMSE bar charts and rating distribution doughnut
55. Model year 2025 produces slightly lower CO2 than 2015 (same specs)

## Technology Stack

- **Backend:** Python, Flask
- **ML:** scikit-learn, XGBoost
- **Data:** Pandas, NumPy
- **Frontend:** Bootstrap 5 (dark theme), Chart.js
- **Database:** SQLite
- **Deployment:** Docker

## Default Credentials

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | Admin |
