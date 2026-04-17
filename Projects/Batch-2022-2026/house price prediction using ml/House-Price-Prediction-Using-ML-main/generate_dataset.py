import pandas as pd
import numpy as np

np.random.seed(42)
N = 10000

# California-like coordinates
longitude = np.random.uniform(-124.35, -114.31, N)
latitude = np.random.uniform(32.54, 41.95, N)

housing_median_age = np.random.randint(1, 52, N).astype(float)
total_rooms = np.random.lognormal(mean=7.5, sigma=0.6, size=N).astype(int).clip(2, 40000).astype(float)
total_bedrooms = (total_rooms * np.random.uniform(0.1, 0.3, N)).astype(int).clip(1, 7000).astype(float)
population = np.random.lognormal(mean=7.0, sigma=0.8, size=N).astype(int).clip(3, 35000).astype(float)
households = (total_bedrooms * np.random.uniform(0.8, 1.2, N)).astype(int).clip(1, 6100).astype(float)
median_income = np.random.lognormal(mean=1.2, sigma=0.6, size=N).clip(0.5, 15.0)

# Ocean proximity based on longitude
ocean_cats = []
for lon, lat in zip(longitude, latitude):
    if lon > -118 and lat < 34.5:
        ocean_cats.append('<1H OCEAN')
    elif lon < -122:
        ocean_cats.append('NEAR OCEAN')
    elif lon > -119 and lat > 37:
        ocean_cats.append('INLAND')
    elif lon < -121 and lat > 37:
        ocean_cats.append('NEAR BAY')
    else:
        ocean_cats.append(np.random.choice(['<1H OCEAN', 'INLAND', 'NEAR OCEAN', 'NEAR BAY']))
ocean_proximity = np.array(ocean_cats)
# Sprinkle a few ISLAND
island_idx = np.random.choice(N, 5, replace=False)
ocean_proximity[island_idx] = 'ISLAND'

# Target: median_house_value influenced by income, location, age
base_price = median_income * 30000
location_bonus = np.where(ocean_proximity == 'NEAR BAY', 60000,
                 np.where(ocean_proximity == 'NEAR OCEAN', 50000,
                 np.where(ocean_proximity == '<1H OCEAN', 40000,
                 np.where(ocean_proximity == 'ISLAND', 80000, 0))))
age_factor = np.where(housing_median_age < 20, 20000, np.where(housing_median_age > 40, -10000, 0))
noise = np.random.normal(0, 25000, N)
median_house_value = (base_price + location_bonus + age_factor + noise).clip(15000, 500001)

# Add ~3% missing values to total_bedrooms
missing_idx = np.random.choice(N, int(N * 0.03), replace=False)
total_bedrooms_with_nan = total_bedrooms.copy()
total_bedrooms_with_nan[missing_idx] = np.nan

df = pd.DataFrame({
    'longitude': np.round(longitude, 2),
    'latitude': np.round(latitude, 2),
    'housing_median_age': housing_median_age,
    'total_rooms': total_rooms,
    'total_bedrooms': total_bedrooms_with_nan,
    'population': population,
    'households': households,
    'median_income': np.round(median_income, 4),
    'ocean_proximity': ocean_proximity,
    'median_house_value': np.round(median_house_value, 0)
})

df.to_csv('housing.csv', index=False)
print(f'Dataset created: {len(df)} rows, {len(df.columns)} columns')
print(f'Ocean proximity distribution:\n{df["ocean_proximity"].value_counts()}')
print(f'Price range: ${df["median_house_value"].min():,.0f} - ${df["median_house_value"].max():,.0f}')
print(f'Missing total_bedrooms: {df["total_bedrooms"].isna().sum()}')
