# Carbon Emission Prediction — Project Explanation

## What Does This Project Do?

Imagine you're buying a new car and want to know how much pollution it creates. This project is like a smart calculator — you tell it about a car (how big the engine is, what fuel it uses, how heavy it is, what year it was made) and it tells you exactly how much CO2 (carbon dioxide) that car will release into the air for every kilometer it drives.

CO2 is a gas that comes out of car exhaust pipes. Too much CO2 in the atmosphere causes climate change and global warming. So knowing how much CO2 a car produces helps people choose more environmentally friendly vehicles.

The project also supports **hybrid** and **electric** vehicles. An electric car produces zero CO2 from its exhaust (because it has no exhaust!), and a hybrid car produces about 40% less than a regular gasoline car.

## How Does It Work? (Step by Step)

### Step 1: Creating Practice Data

Since we don't have real data from car companies, we create realistic fake data. Think of it like making a practice test before the real exam.

We create 7,000 fake car records. Each record has 12 pieces of information:
- **Make** — The car brand (Toyota, Honda, Ford, BMW, etc.)
- **Model Year** — When the car was made (2015-2025). Newer cars are more efficient.
- **Vehicle Class** — The type of car (Compact, SUV, Pickup, etc.)
- **Engine Size** — How big the engine is (measured in litres, like 1.5L or 3.0L). Electric cars have 0.
- **Cylinders** — How many cylinders the engine has (4, 6, 8, etc.). Electric cars have 0.
- **Vehicle Weight** — How heavy the car is in kilograms. Heavier cars need more energy to move.
- **Transmission** — How gears are changed (Automatic, Manual, or CVT)
- **Fuel Type** — What powers the car: Regular Gasoline, Premium Gasoline, Diesel, Ethanol, **Hybrid**, or **Electric**
- **Fuel Consumption (City)** — How much fuel the car drinks per 100 km in city driving
- **Fuel Consumption (Highway)** — How much fuel on highways (less than city because no stop-and-go)
- **Fuel Consumption (Combined)** — Average of city and highway (55% city + 45% highway)
- **CO2 Emissions** — How much carbon dioxide comes out (in grams per kilometer)

The data follows real-world patterns. For example:
- Bigger engines burn more fuel and produce more CO2
- Heavier vehicles need more energy, so they produce more CO2
- Diesel cars produce more CO2 per litre of fuel than gasoline cars
- Hybrid cars use about 40% less fuel than regular gasoline cars
- Electric cars produce zero tailpipe CO2
- Newer cars (2025) are slightly more efficient than older ones (2015)
- SUVs and pickups generally produce more CO2 than compact cars
- CVT transmissions are slightly more fuel-efficient
- A compact car can't have a 6.5L engine with 12 cylinders — the data respects these real-world limits

### Step 2: Teaching the Computer (Training)

We take those 7,000 records and split them: 70% for teaching (4,900 records) and 30% for testing (2,100 records).

Before teaching, we prepare the data:
- **Text → Numbers:** The computer can't understand words like "Toyota" or "Diesel", so we convert them to numbers (e.g., Toyota = 8, Diesel = 1). This is called "Label Encoding."
- **Number Scaling:** Engine Size ranges from 0-6.5 but Weight ranges from 800-3000. We scale all numbers to a similar range so no feature dominates. This is called "Standard Scaling."

Then we teach 6 different "algorithms" (methods of learning) to predict CO2 from the car details:

1. **Linear Regression** — Draws a straight line through the data. Simple but not always accurate. Like estimating distance with a ruler. R² = 95.30%

2. **Random Forest** — Creates 100 different decision trees (like a flowchart: "Is engine > 3L? Yes → go left. No → go right.") and averages their answers. Very accurate! Like asking 100 experts and taking the average. R² = 99.69%

3. **Decision Tree** — Creates one flowchart of yes/no questions. Quick but can be a bit rough. R² = 99.27%

4. **XGBoost** — Builds trees one at a time, where each new tree fixes the mistakes of the previous ones. Like a student who reviews wrong answers and improves. R² = 99.72% — **THE WINNER!**

5. **AdaBoost** — Similar to XGBoost but focuses extra attention on the hardest cases. Like a teacher who gives more homework on topics students struggle with. R² = 96.83%

6. **Lasso Regression** — Like Linear Regression but ignores less important features. Like a student who focuses only on the main topics. R² = 95.23%

### Step 3: Picking the Best Teacher

We test all 6 methods on the 2,100 test records and measure how well they predict CO2 emissions:

- **R² Score** — How much of the pattern the model captures (100% = perfect). XGBoost got 99.72%!
- **MAE** — Average prediction error in g/km. XGBoost: only 3.69 g/km off on average!
- **RMSE** — Similar to MAE but penalizes big mistakes more. XGBoost: 5.08 g/km.

**XGBoost** won! It can predict CO2 emissions with incredible accuracy — off by less than 4 grams per kilometer on average.

### Step 4: The Web Application

We built a website where you can:

1. **Login** — Create an account or use admin/admin123
2. **Predict (5 different ways!)** — The app offers 5 ways to get CO2 predictions:
   - **Form Entry** — Fill in a form with car details → get predicted CO2, confidence interval, rating, footprint, recommendations, and warnings
   - **Quick Presets** — Click on any of 12 popular real-world vehicles (like Toyota Camry, Honda Civic, Ford F-150, Tesla Model 3) and instantly see their CO2 prediction. No typing needed!
   - **Vehicle Comparison** — Compare up to 3 vehicles side-by-side. See which one is the "Greenest" with a visual bar chart. You can load preset vehicles or enter custom specs.
   - **Batch Upload** — Have a fleet of vehicles? Upload a CSV file with all of them and get predictions for every vehicle at once. Download the results as a CSV too.
   - **Interactive Sliders** — Drag sliders to adjust engine size, weight, fuel consumption, etc. and watch the CO2 prediction update instantly — no submit button needed!
3. **Calculator** — A standalone carbon footprint calculator where you enter any CO2 value and your annual driving distance to see your full impact, with a comparison chart showing how you compare to EVs, hybrids, average cars, and SUVs
4. **View History** — See all your past predictions with ratings
5. **Dashboard** — Compare how well the 6 algorithms performed with interactive charts
6. **About** — Learn about CO2 emissions, the v2 improvements, the REST API, and the technology used

### Step 5: The REST API

Other applications can also use our prediction engine! By sending a JSON request to `/api/predict`, any program (a mobile app, another website, a spreadsheet) can get CO2 predictions without using the web interface.

There's also `/api/validate` to check if a set of inputs makes sense before predicting.

## What Are the Key Technologies?

| Technology | What It Does |
|-----------|-------------|
| **Python** | The programming language everything is written in |
| **Flask** | A web framework that turns Python code into a website |
| **scikit-learn** | A library with ML algorithms (Random Forest, Decision Tree, etc.) |
| **XGBoost** | A powerful ML library for gradient boosting (our best model!) |
| **Pandas** | Handles data tables (like Excel but in Python) |
| **NumPy** | Does math with arrays of numbers |
| **Chart.js** | Creates beautiful interactive charts in the browser |
| **Bootstrap 5** | Makes the website look modern and professional (dark theme) |
| **SQLite** | A simple database that stores user accounts and predictions |
| **Docker** | Packages the entire app so it runs the same everywhere |

## What Is Machine Learning Regression?

In "classification" (like our other projects), the computer picks a category (like "spam" or "not spam"). In "regression," the computer predicts a number (like "237.5 grams of CO2 per km").

It's like the difference between:
- **Classification:** "Will it rain today?" → Yes or No
- **Regression:** "How many millimeters of rain will fall?" → 12.5mm

Our project uses regression because CO2 emissions are a continuous number, not a category.

## How Is the CO2 Actually Calculated?

In real life, CO2 emissions depend on how much fuel a car burns. The formula is:

**CO2 (g/km) = Fuel Consumption (L/100km) x CO2 Factor (kg/L) x 10**

Where the CO2 factor depends on fuel type:
- Regular/Premium Gasoline: 2.31 kg CO2 per litre
- Diesel: 2.66 kg CO2 per litre
- Ethanol (E85): 1.61 kg CO2 per litre
- Hybrid: Uses gasoline factor (2.31) but ~40% less fuel consumption
- Electric: 0 — no fuel burned, no tailpipe CO2

So a car that uses 10 L/100km of regular gasoline produces:
10 x 2.31 x 10 = **231 g/km of CO2**

A hybrid version of the same car might use only 6 L/100km:
6 x 2.31 x 10 = **138.6 g/km** — that's 40% less!

An electric car: **0 g/km** of tailpipe CO2.

## What Is a Confidence Interval?

When the model predicts "245.9 g/km", how sure is it? A confidence interval answers this.

For XGBoost, we look at predictions from different subsets of its internal trees. If all subsets agree closely, the model is very confident. If they disagree, there's more uncertainty.

We show a **90% confidence interval** — meaning the true value is very likely within this range. For example: "245.2 — 246.6 g/km" means the model is quite certain the answer is around 245-246.

## What Is the Carbon Footprint Calculator?

The prediction tells you CO2 per kilometer. But how much does that add up over a year?

**Annual CO2 = CO2 (g/km) x Annual Distance (km) / 1,000,000 = tonnes per year**

Example: A car producing 200 g/km driven 15,000 km/year:
200 x 15,000 = 3,000,000 g = **3.0 tonnes of CO2 per year**

To offset this, you'd need to plant about **136 trees** (each tree absorbs ~22 kg CO2/year).

The calculator also shows how you compare to:
- Electric vehicles (0 tonnes)
- Hybrids (~1.5 tonnes)
- Average cars (~2.7 tonnes)
- SUVs/Pickups (~4.5 tonnes)

## What Does Each File Do?

| File | Purpose |
|------|---------|
| `generate_dataset.py` | Creates 7,000 vehicle records with 12 features including weight, year, hybrid, and electric types |
| `train_model.py` | Teaches 6 ML models, compares them, and saves the best one (XGBoost) |
| `app.py` | The main website (routes, 5 prediction modes, validation, recommendations, footprint, REST API) |
| `templates/base.html` | The overall page layout (dark theme with green accents, Predict dropdown with 5 modes) |
| `templates/login.html` | Login and registration page |
| `templates/home.html` | Home page with stats and recent predictions |
| `templates/predict.html` | The form where you enter car details — shows prediction, confidence interval, footprint, recommendations, warnings |
| `templates/presets.html` | Quick preset cards for 12 popular real-world vehicles with instant predictions |
| `templates/compare.html` | Side-by-side comparison of up to 3 vehicles with visual bar chart and "Greenest" badge |
| `templates/batch.html` | CSV upload page for bulk predictions with downloadable results and sample template |
| `templates/interactive.html` | Real-time slider-based prediction — drag sliders and watch CO2 update instantly |
| `templates/calculator.html` | Standalone carbon footprint calculator with comparison chart and tree offset |
| `templates/history.html` | Shows all past predictions in a table with color-coded ratings |
| `templates/dashboard.html` | Charts comparing the 6 ML models (R², MAE, RMSE, rating distribution) |
| `templates/about.html` | Information about CO2, v2 features, REST API reference, and tech stack |
| `final_co2.csv` | The dataset (7,000 records, 12 columns — created by generate_dataset.py) |
| `best_model.pkl` | The trained XGBoost model (created by train_model.py) |
| `encoders.pkl` | Converts text labels (like "Toyota") to numbers for the model |
| `scaler.pkl` | Normalizes number ranges so the model works better |
| `models_info.json` | Performance metrics for all 6 models |
| `carbon_emissions.db` | SQLite database storing user accounts and prediction history |

## How to Run It Yourself

1. Install Python 3.8+
2. Run `pip install -r requirements.txt`
3. Run `python generate_dataset.py` (creates the dataset with 7,000 records)
4. Run `python train_model.py` (trains 6 models, saves the best)
5. Run `python app.py` (starts the website)
6. Open http://localhost:5012 in your browser
7. Login with username: `admin`, password: `admin123`

Or with Docker:
```bash
docker build -t carbon-emission .
docker run -p 5012:5012 carbon-emission
```

## What Changed in v2?

| Feature | v1 | v2 |
|---------|----|----|
| Input features | 9 | 11 (added Vehicle Weight, Model Year) |
| Fuel types | 4 (Gas, Premium, Diesel, Ethanol) | 6 (+ Hybrid, Electric) |
| Best model | Random Forest (R² 99.34%) | XGBoost (R² 99.72%) |
| Confidence interval | No | Yes (90% range from model trees) |
| Input validation | Basic range checks | Smart class-based validation + EV checks |
| Carbon footprint | No | Yes (annual tonnes, trees to offset, comparison) |
| Recommendations | No | Yes (eco-friendly tips per prediction) |
| REST API | No | Yes (`/api/predict`, `/api/validate`) |
| Electric vehicles | Not supported | Full support (0 CO2, auto-zero fields) |
| Hybrid vehicles | Not supported | Full support (~40% less fuel consumption) |
| Auto-fill on class change | No | Yes (suggests midpoint engine/weight/cylinders) |
| Pages | 6 | 7 (added Calculator) |

## What Changed in v3?

v3 added **4 new prediction modes** so users can get CO2 predictions in different ways:

| Feature | v2 | v3 |
|---------|----|----|
| Prediction modes | 1 (Form Entry) | 5 (Form, Presets, Compare, Batch, Interactive) |
| Quick Presets | No | 12 popular vehicles with one-click predictions |
| Vehicle Comparison | No | Side-by-side compare up to 3 vehicles |
| Batch Prediction | No | CSV upload → bulk predictions → download results |
| Interactive Sliders | No | Real-time prediction as you drag sliders |
| Predict navbar | Single link | Dropdown menu with 5 modes |
| REST API endpoints | 2 | 3 (added `/api/predict-live` for real-time) |
| Templates | 8 | 12 (added presets, compare, batch, interactive) |

## Why Does This Matter?

- Cars produce about 4.6 metric tons of CO2 per year on average
- Transportation is the largest source of CO2 emissions in many countries
- Knowing a car's CO2 output helps people make greener choices
- Governments use CO2 data to set emission standards and fuel efficiency rules
- This kind of prediction helps in planning carbon reduction strategies
- The rise of hybrid and electric vehicles is critical for reducing transportation emissions
- A carbon footprint calculator helps individuals understand their personal environmental impact
