# House Price Prediction — Project Explanation

This document explains the House Price Prediction project in simple language that anyone can understand.

## What is This Project?

This is a website that can predict how much a house in California might cost. You tell it some basic information about the house and its neighborhood, and it uses a trained computer brain (called a machine learning model) to estimate the price.

Think of it like a real estate agent who has looked at thousands of houses and learned what makes some expensive and others cheap. Except instead of a person, it's a computer that learned from data.

## Why Was This Project Built?

Buying a house is one of the biggest financial decisions people make. Knowing a fair price helps:
- Buyers avoid overpaying
- Sellers set reasonable prices
- Real estate agents provide better advice
- Banks decide how much to lend

This project shows how machine learning can analyze patterns in housing data to make price predictions automatically.

## How Does It Work?

### Step 1: The Data

The project uses a dataset about California housing. Each row represents a neighborhood (called a "census block") and contains 9 pieces of information:

| Feature | What It Means | Example |
|---------|--------------|---------|
| Longitude | How far east/west the neighborhood is | -122.23 (San Francisco area) |
| Latitude | How far north/south the neighborhood is | 37.88 |
| Housing Median Age | The typical age of houses in that area | 41 years |
| Total Rooms | How many rooms are in all the houses combined | 880 |
| Total Bedrooms | How many bedrooms are in all the houses combined | 129 |
| Population | How many people live in that area | 322 |
| Households | How many families/groups live there | 126 |
| Median Income | The typical yearly income of people there (in tens of thousands) | 8.33 means $83,300 |
| Ocean Proximity | How close the neighborhood is to the ocean | NEAR BAY, INLAND, etc. |

The **target** (what we want to predict) is the **median house value** — the typical price of a house in that neighborhood.

### Step 2: Training the Model

The computer learns from 10,000 examples. Here's how:

1. **Split the data** — 80% is used for learning (training), 20% is used for testing
2. **Show the training examples** — The computer sees the 9 features and the actual price for each neighborhood
3. **Find patterns** — It learns rules like:
   - Higher income → higher price
   - Near the ocean → higher price
   - Inland → lower price
   - More rooms per household → higher price
4. **Test itself** — It predicts prices for the 20% it hasn't seen and checks how close it got

### Step 3: Choosing the Best Model

We train 5 different types of models and compare them:

| Model | How It Works (Simple Explanation) | Accuracy (R²) |
|-------|----------------------------------|----------------|
| Linear Regression | Draws a straight line through the data | 0.85 |
| Ridge Regression | Same as above but prevents overfitting | 0.85 |
| Decision Tree | Makes yes/no decisions in a tree structure | 0.85 |
| Random Forest | Uses 100 decision trees and averages their answers | 0.88 |
| **Gradient Boosting** | Builds trees one at a time, each fixing the previous one's mistakes | **0.89** |

**Gradient Boosting wins** because it has the highest R² score (0.89), meaning it explains 89% of the variation in house prices.

### Step 4: Making Predictions

When you enter features on the website:
1. The values are converted into numbers the model understands
2. The trained Gradient Boosting model processes them
3. It outputs a predicted price
4. The prediction is saved to your history

## What is R² Score?

R² (called "R-squared") tells us how good the model is at predicting:
- **R² = 1.0** means perfect predictions (never happens in real life)
- **R² = 0.89** means the model explains 89% of price variations — very good!
- **R² = 0.0** means the model is no better than just guessing the average price
- **R² < 0** means the model is worse than guessing (bad model)

## What is MAE and RMSE?

These measure how far off the predictions are, in dollars:

- **MAE (Mean Absolute Error)** = $20,267 — on average, the prediction is about $20,000 off from the real price
- **RMSE (Root Mean Squared Error)** = $25,273 — similar to MAE but penalizes big errors more heavily

For houses worth $100,000 to $500,000, being off by $20,000 is pretty reasonable!

## What is Gradient Boosting?

Imagine you're trying to guess someone's weight:

1. **First guess:** You start with the average weight of all people — say 70 kg. You're probably off for most individuals.
2. **Second guess:** You look at how wrong you were for each person. People who are taller, you were probably too low. So you adjust: "If tall, add 10 kg."
3. **Third guess:** You look at remaining errors. People who exercise a lot weigh less. Adjustment: "If exercises frequently, subtract 5 kg."
4. **Repeat 200 times:** Each time, you find patterns in your remaining errors and add a small correction.

That's Gradient Boosting! Each "guess" is a small decision tree, and they add up to a very accurate model. The word "gradient" refers to the mathematical technique used to find the best corrections.

## How Does the Website Work?

### The Server (Flask)

Flask is a Python web framework — it receives requests from your browser and sends back web pages. When you visit a URL like `/predict`:
1. Flask checks if you're logged in
2. If it's a GET request, it shows the prediction form
3. If it's a POST request (you submitted the form), it runs the model and shows results

### The Database (SQLite)

SQLite is a lightweight database stored in a single file (`housing.db`). It has two tables:
- **users** — stores everyone's login information (passwords are encrypted)
- **predictions** — stores every prediction made, linked to the user who made it

### Authentication

When you register:
1. Your password is hashed (scrambled) using PBKDF2-SHA256 — even if someone sees the database, they can't read your password
2. Your account is saved

When you log in:
1. The system hashes the password you typed
2. It compares it with the stored hash
3. If they match, you get a session cookie (like a digital wristband at a water park)
4. This cookie tells the server "this person is logged in" for every page they visit

### The Visualizations

Seven charts are generated when the model is trained:
1. **Price Distribution** — histogram showing how many houses are at each price level
2. **Correlation Heatmap** — shows which features are related to each other
3. **Feature Importance** — which features matter most for prediction
4. **Ocean Proximity** — how location type affects price
5. **Geographic Map** — prices plotted on a map of California
6. **Model Comparison** — R² scores of all 5 models
7. **Income vs Price** — scatter plot showing income's effect on price

## Key Findings from the Data

1. **Median Income is the strongest predictor** — higher income neighborhoods have higher house prices
2. **Ocean proximity matters** — houses near the bay or ocean are worth more than inland houses
3. **Location coordinates help** — longitude and latitude encode geographic value (coastal vs inland)
4. **Housing age has moderate impact** — very new houses tend to be slightly more expensive
5. **Population density is less important** — the number of people matters less than income and location

## Important Note

This is a student project for educational purposes. The predictions are based on synthetic data that mimics real California housing patterns. For actual house purchases:
- Consult a licensed real estate agent
- Get a professional appraisal
- Consider factors this model doesn't capture (school quality, crime rate, specific house features, market trends)

## Summary

This project demonstrates:
1. **Data Generation** — creating realistic synthetic housing data
2. **Machine Learning** — training and comparing 5 regression models
3. **Web Development** — building a Flask application with authentication
4. **Data Visualization** — creating informative EDA charts
5. **Model Deployment** — serving predictions via a web interface
6. **Database Management** — storing users and prediction history in SQLite

It shows how AI and machine learning can be applied to real-world problems like real estate valuation.
