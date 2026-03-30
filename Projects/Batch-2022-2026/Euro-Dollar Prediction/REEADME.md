# Euro–Dollar Forex Prediction System

A Machine Learning-based web application for predicting EUR/USD foreign exchange movements using historical market data and advanced predictive models.

## Features

- Historical EUR/USD data analysis
- Machine Learning-based price prediction
- Data visualization (trend graphs & moving averages)
- Feature engineering (technical indicators)
- Model comparison (Linear Regression, Random Forest, LSTM, etc.)
- Performance evaluation (MAE, RMSE, Accuracy)
- Simple web interface (if applicable)

---

## Requirements

- Python 3.8+
- pip
- Virtual Environment (recommended)
- Flask
- pandas
- numpy
- matplotlib
- scikit-learn
- tensorflow
- keras

---

## Installation

```bash# 1. Clone the repository
git clone <repository-url>
cd Euro-Dollar-Prediction

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

## Running

```bash
python app.py
```

Open **http://localhost:5000** in your browser.

---

## Stopping

```bash
pkill -9 -f "python app.py"
```

---

## Project Structure

```
Euro-Dollar-Prediction/
│
├── app.py                         # Main Flask application
├── requirements.txt               # Project dependencies
├── EUR_USD_Last_5_Years.csv       # Historical forex dataset
├── XY_train.csv                   # Processed training dataset
│
├── templates/                     # HTML Templates
│   ├── base.html
│   ├── home.html
│   ├── eda.html
│   ├── linear_regression.html
│   ├── lstm.html
│   ├── performance.html
│   ├── predict.html
│   └── upload.html
│
├── static/
│   ├── css/
│   ├── eda/
│   ├── lstm_results/
│   ├── lstm_v1/
│   ├── outputs_lr/
│   └── performance/
│
└── views/                         # Flask route logic
```
