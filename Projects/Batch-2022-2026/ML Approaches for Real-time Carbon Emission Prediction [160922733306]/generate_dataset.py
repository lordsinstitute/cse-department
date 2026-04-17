"""
Generate synthetic vehicle CO2 emissions dataset.
~7,000 records with realistic correlations between vehicle specs and CO2 output.
Based on Canadian light-duty vehicle fuel consumption ratings (2022).

Improvements over v1:
  - Vehicle weight (kg) correlated with class
  - Model year (2015-2025) affects emissions
  - Hybrid and Electric fuel types
  - Realistic make-class combinations (no 12-cyl compacts)
"""

import os
import numpy as np
import pandas as pd

np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Vehicle configuration tables ---

VEHICLE_CLASSES = {
    'Subcompact':    {'engine_range': (1.0, 1.8), 'cyl_range': (3, 4),  'weight_range': (900, 1200),  'prob': 0.08},
    'Minicompact':   {'engine_range': (1.0, 2.0), 'cyl_range': (3, 4),  'weight_range': (850, 1150),  'prob': 0.05},
    'Compact':       {'engine_range': (1.4, 2.5), 'cyl_range': (4, 4),  'weight_range': (1100, 1450), 'prob': 0.20},
    'Mid-size':      {'engine_range': (1.8, 3.5), 'cyl_range': (4, 6),  'weight_range': (1300, 1700), 'prob': 0.20},
    'Full-size':     {'engine_range': (2.5, 5.0), 'cyl_range': (6, 8),  'weight_range': (1600, 2100), 'prob': 0.10},
    'SUV':           {'engine_range': (2.0, 5.5), 'cyl_range': (4, 8),  'weight_range': (1500, 2500), 'prob': 0.22},
    'Pickup':        {'engine_range': (3.0, 6.5), 'cyl_range': (6, 8),  'weight_range': (1800, 2800), 'prob': 0.10},
    'Station wagon': {'engine_range': (1.6, 3.0), 'cyl_range': (4, 6),  'weight_range': (1200, 1600), 'prob': 0.05},
}

MAKES = ['Toyota', 'Honda', 'Ford', 'BMW', 'Hyundai',
         'Chevrolet', 'Nissan', 'Mercedes-Benz', 'Kia', 'Volkswagen']

TRANSMISSIONS = ['Automatic', 'Manual', 'CVT']
TRANSMISSION_WEIGHTS = [0.55, 0.20, 0.25]

# Fuel types now include Hybrid and Electric
FUEL_TYPES = ['Regular Gasoline', 'Premium Gasoline', 'Diesel', 'Ethanol (E85)', 'Hybrid', 'Electric']
FUEL_TYPE_WEIGHTS = [0.38, 0.18, 0.12, 0.07, 0.15, 0.10]

# CO2 emission factors (kg CO2 per litre of fuel burned)
# Source: Natural Resources Canada
CO2_FACTORS = {
    'Regular Gasoline': 2.31,
    'Premium Gasoline': 2.31,
    'Diesel': 2.66,
    'Ethanol (E85)': 1.61,
    'Hybrid': 2.31,       # Same fuel but ~40% less consumption
    'Electric': 0.0,      # Zero tailpipe emissions
}

NUM_RECORDS = 7000


def generate_dataset():
    """Generate synthetic vehicle CO2 emissions data with realistic constraints."""
    records = []

    class_names = list(VEHICLE_CLASSES.keys())
    class_probs = [VEHICLE_CLASSES[c]['prob'] for c in class_names]

    for _ in range(NUM_RECORDS):
        # Pick vehicle class
        vclass = np.random.choice(class_names, p=class_probs)
        config = VEHICLE_CLASSES[vclass]

        # Model year (2015-2025) — newer cars tend to be more efficient
        model_year = int(np.random.choice(range(2015, 2026)))
        year_efficiency = 1.0 - (model_year - 2015) * 0.008  # ~0.8% improvement per year

        # Fuel type and transmission (determine early since fuel consumption depends on transmission)
        fuel_type = np.random.choice(FUEL_TYPES, p=FUEL_TYPE_WEIGHTS)
        if fuel_type == 'Electric':
            transmission = 'Automatic'
        else:
            transmission = np.random.choice(TRANSMISSIONS, p=TRANSMISSION_WEIGHTS)

        # Electric vehicles: zero fuel consumption, zero CO2
        if fuel_type == 'Electric':
            engine_size = 0.0
            cylinders = 0
            weight_low, weight_high = config['weight_range']
            vehicle_weight = int(np.random.uniform(weight_low + 200, weight_high + 300))  # EVs heavier (battery)
            fuel_city = 0.0
            fuel_hwy = 0.0
            fuel_comb = 0.0
            co2_emissions = 0.0
        else:
            # Engine size (correlated with class)
            engine_low, engine_high = config['engine_range']
            if fuel_type == 'Hybrid':
                # Hybrids tend toward smaller engines
                engine_size = round(np.random.uniform(engine_low, (engine_low + engine_high) / 2), 1)
            else:
                engine_size = round(np.random.uniform(engine_low, engine_high), 1)

            # Cylinders (correlated with engine size, constrained by class)
            cyl_low, cyl_high = config['cyl_range']
            if engine_size < 1.5:
                cylinders = 3
            elif engine_size < 2.5:
                cylinders = 4
            elif engine_size < 3.5:
                cylinders = np.random.choice([4, 6])
            elif engine_size < 5.0:
                cylinders = np.random.choice([6, 8])
            else:
                cylinders = np.random.choice([8, 10])
            cylinders = max(cyl_low, min(cyl_high, cylinders))

            # Vehicle weight (kg) — correlated with class
            weight_low, weight_high = config['weight_range']
            # Heavier engines → heavier vehicle
            weight_bias = (engine_size - engine_low) / max(engine_high - engine_low, 0.1) * 200
            vehicle_weight = int(np.random.uniform(weight_low, weight_high) + weight_bias)

            # Fuel consumption city (L/100km) — correlated with engine size and weight
            weight_factor = vehicle_weight / 1500.0  # Normalize around 1500 kg
            base_city = 4.0 + engine_size * 2.2 + cylinders * 0.25 + (weight_factor - 1.0) * 2.0
            if fuel_type == 'Hybrid':
                base_city *= 0.60  # Hybrids ~40% more efficient in city
            elif fuel_type == 'Diesel':
                base_city *= 0.85
            elif fuel_type == 'Ethanol (E85)':
                base_city *= 1.30
            if transmission == 'CVT':
                base_city *= 0.90
            elif transmission == 'Manual':
                base_city *= 0.95
            base_city *= year_efficiency  # Newer = more efficient
            fuel_city = round(max(3.0, min(22.0, base_city + np.random.normal(0, 0.6))), 1)

            # Fuel consumption highway (~65-80% of city)
            hwy_ratio = 0.72 if fuel_type == 'Hybrid' else np.random.uniform(0.68, 0.82)
            fuel_hwy = round(max(2.5, min(16.0, fuel_city * hwy_ratio + np.random.normal(0, 0.3))), 1)

            # Combined (55% city + 45% highway — standard weighting)
            fuel_comb = round(0.55 * fuel_city + 0.45 * fuel_hwy, 1)

            # CO2 emissions (g/km) = fuel_comb (L/100km) * CO2_factor (kg/L) * 10
            co2_factor = CO2_FACTORS[fuel_type]
            co2_base = fuel_comb * co2_factor * 10
            co2_emissions = round(max(0, min(520, co2_base + np.random.normal(0, 4))), 1)

        # Make
        make = np.random.choice(MAKES)

        records.append({
            'Make': make,
            'Model_Year': model_year,
            'Vehicle_Class': vclass,
            'Engine_Size': engine_size,
            'Cylinders': cylinders,
            'Vehicle_Weight': vehicle_weight,
            'Transmission': transmission,
            'Fuel_Type': fuel_type,
            'Fuel_Consumption_City': fuel_city,
            'Fuel_Consumption_Hwy': fuel_hwy,
            'Fuel_Consumption_Comb': fuel_comb,
            'CO2_Emissions': co2_emissions,
        })

    df = pd.DataFrame(records)
    csv_path = os.path.join(BASE_DIR, 'final_co2.csv')
    df.to_csv(csv_path, index=True)
    print(f'Dataset saved to {csv_path}')
    print(f'Shape: {df.shape}')
    print(f'\nColumn types:\n{df.dtypes}')
    print(f'\nCO2 Emissions stats:\n{df["CO2_Emissions"].describe()}')
    print(f'\nVehicle class distribution:\n{df["Vehicle_Class"].value_counts()}')
    print(f'\nFuel type distribution:\n{df["Fuel_Type"].value_counts()}')
    print(f'\nModel year range: {df["Model_Year"].min()} - {df["Model_Year"].max()}')
    print(f'\nVehicle weight stats:\n{df["Vehicle_Weight"].describe()}')

    return df


if __name__ == '__main__':
    print('=' * 60)
    print('Generating Synthetic Vehicle CO2 Emissions Dataset')
    print('=' * 60)
    generate_dataset()
    print('\nDone!')
