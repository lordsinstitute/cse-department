import pandas as pd
import numpy as np
import json
import joblib
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# Load dataset
df = pd.read_csv('housing.csv')
print(f'Loaded {len(df)} rows')

# Preprocessing
df['total_bedrooms'] = df['total_bedrooms'].fillna(df['total_bedrooms'].mean())
ocean_map = {cat: i for i, cat in enumerate(sorted(df['ocean_proximity'].unique()))}
df['ocean_proximity_encoded'] = df['ocean_proximity'].map(ocean_map)

# Save ocean mapping for app.py
FEATURE_ORDER = ['longitude', 'latitude', 'housing_median_age', 'total_rooms',
                 'total_bedrooms', 'population', 'households', 'median_income',
                 'ocean_proximity_encoded']

# Outlier removal
df = df[df['median_house_value'] < 500001]
df = df[df['population'] < 25000]
print(f'After filtering: {len(df)} rows')

X = df[FEATURE_ORDER]
y = df['median_house_value']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train 6 models
models = {
    'Linear Regression': LinearRegression(),
    'Ridge Regression': Ridge(alpha=1.0),
    'Decision Tree': DecisionTreeRegressor(random_state=42, max_depth=10),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=200, random_state=42, learning_rate=0.1),
}

# Try LightGBM
try:
    import lightgbm as lgb
    models['LightGBM'] = lgb.LGBMRegressor(n_estimators=200, random_state=42, verbose=-1)
except ImportError:
    print('LightGBM not installed, skipping')

results = {}
best_model_name = None
best_r2 = -999

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = round(r2_score(y_test, y_pred), 4)
    n = len(y_test)
    p = X_test.shape[1]
    adj_r2 = round(1 - (1 - r2) * (n - 1) / (n - p - 1), 4)
    mae = round(mean_absolute_error(y_test, y_pred), 2)
    mse = round(mean_squared_error(y_test, y_pred), 2)
    rmse = round(np.sqrt(mse), 2)

    results[name] = {'R2': r2, 'Adj_R2': adj_r2, 'MAE': mae, 'MSE': mse, 'RMSE': rmse}
    print(f'{name}: R²={r2}, MAE={mae}, RMSE={rmse}')

    if r2 > best_r2:
        best_r2 = r2
        best_model_name = name

# Save best model
best_model = models[best_model_name]
joblib.dump(best_model, 'housing_model.pkl')
print(f'\nBest model: {best_model_name} (R²={best_r2})')

# Save metadata
info = {
    'best_model': best_model_name,
    'feature_order': FEATURE_ORDER,
    'ocean_map': ocean_map,
    'results': results
}
with open('models_info.json', 'w') as f:
    json.dump(info, f, indent=2)

# ---- Generate EDA Visualizations ----
os.makedirs('static/vis', exist_ok=True)
plt.style.use('dark_background')
colors = {'primary': '#3b82f6', 'accent': '#06b6d4', 'bg': '#1b263b'}

# 1. Price distribution
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(df['median_house_value'], bins=50, color=colors['primary'], edgecolor='white', alpha=0.8)
ax.set_title('Distribution of House Prices', fontsize=14, fontweight='bold')
ax.set_xlabel('Median House Value ($)')
ax.set_ylabel('Frequency')
fig.savefig('static/vis/price_dist.png', dpi=100, bbox_inches='tight', facecolor='#0d1b2a')
plt.close()

# 2. Correlation heatmap
fig, ax = plt.subplots(figsize=(10, 8))
numeric_cols = df.select_dtypes(include=[np.number]).columns
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=ax, linewidths=0.5)
ax.set_title('Feature Correlation Heatmap', fontsize=14, fontweight='bold')
fig.savefig('static/vis/correlation.png', dpi=100, bbox_inches='tight', facecolor='#0d1b2a')
plt.close()

# 3. Feature importance (from best tree-based model)
if hasattr(best_model, 'feature_importances_'):
    importances = best_model.feature_importances_
else:
    importances = np.abs(best_model.coef_) if hasattr(best_model, 'coef_') else np.zeros(len(FEATURE_ORDER))
fig, ax = plt.subplots(figsize=(10, 6))
sorted_idx = np.argsort(importances)
ax.barh([FEATURE_ORDER[i] for i in sorted_idx], importances[sorted_idx], color=colors['primary'])
ax.set_title(f'Feature Importance ({best_model_name})', fontsize=14, fontweight='bold')
ax.set_xlabel('Importance')
fig.savefig('static/vis/feature_importance.png', dpi=100, bbox_inches='tight', facecolor='#0d1b2a')
plt.close()

# 4. Ocean proximity vs price
fig, ax = plt.subplots(figsize=(10, 6))
ocean_groups = df.groupby('ocean_proximity')['median_house_value'].median().sort_values()
ax.barh(ocean_groups.index, ocean_groups.values, color=colors['primary'])
ax.set_title('Median House Price by Ocean Proximity', fontsize=14, fontweight='bold')
ax.set_xlabel('Median House Value ($)')
fig.savefig('static/vis/ocean_proximity.png', dpi=100, bbox_inches='tight', facecolor='#0d1b2a')
plt.close()

# 5. Location scatter
fig, ax = plt.subplots(figsize=(10, 8))
scatter = ax.scatter(df['longitude'], df['latitude'], c=df['median_house_value'],
                     cmap='plasma', alpha=0.5, s=5)
plt.colorbar(scatter, ax=ax, label='Median House Value ($)')
ax.set_title('House Prices by Location', fontsize=14, fontweight='bold')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
fig.savefig('static/vis/location_scatter.png', dpi=100, bbox_inches='tight', facecolor='#0d1b2a')
plt.close()

# 6. Model comparison
fig, ax = plt.subplots(figsize=(10, 6))
model_names = list(results.keys())
r2_scores = [results[m]['R2'] for m in model_names]
bars = ax.bar(model_names, r2_scores, color=colors['primary'])
for bar, name in zip(bars, model_names):
    if name == best_model_name:
        bar.set_color('#22c55e')
ax.set_title('Model Comparison (R² Score)', fontsize=14, fontweight='bold')
ax.set_ylabel('R² Score')
ax.set_ylim(0, 1)
plt.xticks(rotation=30, ha='right')
fig.savefig('static/vis/model_comparison.png', dpi=100, bbox_inches='tight', facecolor='#0d1b2a')
plt.close()

# 7. Income vs price scatter
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df['median_income'], df['median_house_value'], alpha=0.3, s=5, color=colors['accent'])
ax.set_title('Median Income vs House Price', fontsize=14, fontweight='bold')
ax.set_xlabel('Median Income (tens of thousands)')
ax.set_ylabel('Median House Value ($)')
fig.savefig('static/vis/income_vs_price.png', dpi=100, bbox_inches='tight', facecolor='#0d1b2a')
plt.close()

print(f'\n7 EDA visualizations saved to static/vis/')
print('Training complete!')
