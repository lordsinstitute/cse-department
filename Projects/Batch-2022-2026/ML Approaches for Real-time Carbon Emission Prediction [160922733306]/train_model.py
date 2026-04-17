"""
Train 6 regression models for CO2 emissions prediction.
Algorithms: Linear Regression, Random Forest, Decision Tree, XGBoost, AdaBoost, Lasso.
Saves best model, encoders, scaler, and metrics.

v2: Added Vehicle_Weight and Model_Year features.
"""

import os
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'final_co2.csv')

CATEGORICAL_COLS = ['Make', 'Vehicle_Class', 'Transmission', 'Fuel_Type']
NUMERIC_COLS = ['Engine_Size', 'Cylinders', 'Vehicle_Weight', 'Model_Year',
                'Fuel_Consumption_City', 'Fuel_Consumption_Hwy', 'Fuel_Consumption_Comb']
TARGET = 'CO2_Emissions'


def main():
    print('=' * 60)
    print('CO2 Emissions — Model Training')
    print('=' * 60)

    # Load data
    data = pd.read_csv(CSV_PATH, index_col=0)
    print(f'Dataset: {data.shape[0]} rows, {data.shape[1]} columns')

    # Encode categorical features
    encoders = {}
    for col in CATEGORICAL_COLS:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
        encoders[col] = le
        print(f'Encoded {col}: {len(le.classes_)} classes')

    # Save encoders
    enc_path = os.path.join(BASE_DIR, 'encoders.pkl')
    joblib.dump(encoders, enc_path)
    print(f'Encoders saved to {enc_path}')

    # Split features and target
    feature_cols = CATEGORICAL_COLS + NUMERIC_COLS
    X = data[feature_cols]
    y = data[TARGET]

    # Train-test split (70-30)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42
    )
    print(f'Train: {X_train.shape[0]}, Test: {X_test.shape[0]}')

    # Scale numeric features
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    X_train_scaled[NUMERIC_COLS] = scaler.fit_transform(X_train[NUMERIC_COLS])
    X_test_scaled[NUMERIC_COLS] = scaler.transform(X_test[NUMERIC_COLS])

    # Save scaler
    scaler_path = os.path.join(BASE_DIR, 'scaler.pkl')
    joblib.dump(scaler, scaler_path)
    print(f'Scaler saved to {scaler_path}')

    # Define models
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
        'Decision Tree': DecisionTreeRegressor(random_state=42),
        'XGBoost': XGBRegressor(n_estimators=100, random_state=42, verbosity=0),
        'AdaBoost': AdaBoostRegressor(n_estimators=100, random_state=42),
        'Lasso': Lasso(alpha=1.0),
    }

    # Train and evaluate each model
    results = {}
    best_r2 = -999
    best_name = None
    best_model = None

    for name, model in models.items():
        print(f'\n{"=" * 50}')
        print(f'Training {name}')
        print('=' * 50)

        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)

        r2 = round(r2_score(y_test, y_pred) * 100, 2)
        mae = round(mean_absolute_error(y_test, y_pred), 2)
        mse = round(mean_squared_error(y_test, y_pred), 2)
        rmse = round(np.sqrt(mean_squared_error(y_test, y_pred)), 2)

        results[name] = {
            'r2': r2,
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
        }

        print(f'R² Score:  {r2}%')
        print(f'MAE:       {mae} g/km')
        print(f'RMSE:      {rmse} g/km')

        if r2 > best_r2:
            best_r2 = r2
            best_name = name
            best_model = model

    # Save best model
    model_path = os.path.join(BASE_DIR, 'best_model.pkl')
    joblib.dump(best_model, model_path)
    print(f'\nBest model: {best_name} (R²={best_r2}%)')
    print(f'Saved to {model_path}')

    # Save all metrics
    all_info = {
        'models': results,
        'best_model': best_name,
        'features': feature_cols,
        'categorical_features': CATEGORICAL_COLS,
        'numeric_features': NUMERIC_COLS,
        'train_size': int(X_train.shape[0]),
        'test_size': int(X_test.shape[0]),
    }

    info_path = os.path.join(BASE_DIR, 'models_info.json')
    with open(info_path, 'w') as f:
        json.dump(all_info, f, indent=2)
    print(f'Metrics saved to {info_path}')

    # Print summary
    print(f'\n{"=" * 70}')
    print('Model Comparison Summary')
    print(f'{"=" * 70}')
    print(f'{"Model":<22} {"R² (%)":>8} {"MAE":>10} {"RMSE":>10}')
    print('-' * 55)
    for name, m in results.items():
        print(f'{name:<22} {m["r2"]:>7.2f}% {m["mae"]:>9.2f} {m["rmse"]:>9.2f}')
    print(f'\nBest: {best_name} (R²={best_r2}%)')
    print('=' * 70)


if __name__ == '__main__':
    main()
