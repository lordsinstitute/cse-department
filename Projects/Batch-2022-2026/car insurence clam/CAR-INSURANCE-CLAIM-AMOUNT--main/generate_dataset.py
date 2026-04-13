"""
Generate synthetic Car Insurance Claim dataset.
Mimics real-world car insurance data with realistic distributions.
"""
import pandas as pd
import numpy as np

np.random.seed(42)

N = 10000  # Number of records


def generate_dataset():
    data = {
        'ID': range(1, N + 1),
        'AGE': np.random.choice(
            ['16-25', '26-39', '40-64', '65+'],
            N, p=[0.15, 0.35, 0.35, 0.15]
        ),
        'GENDER': np.random.choice(['male', 'female'], N, p=[0.52, 0.48]),
        'RACE': np.random.choice(
            ['majority', 'minority'],
            N, p=[0.65, 0.35]
        ),
        'DRIVING_EXPERIENCE': np.random.choice(
            ['0-9y', '10-19y', '20-29y', '30y+'],
            N, p=[0.25, 0.30, 0.25, 0.20]
        ),
        'EDUCATION': np.random.choice(
            ['none', 'high school', 'university'],
            N, p=[0.15, 0.45, 0.40]
        ),
        'INCOME': np.random.choice(
            ['poverty', 'working class', 'middle class', 'upper class'],
            N, p=[0.15, 0.30, 0.35, 0.20]
        ),
        'CREDIT_SCORE': np.round(np.random.uniform(0.0, 1.0, N), 6),
        'VEHICLE_OWNERSHIP': np.random.choice([0, 1], N, p=[0.45, 0.55]),
        'VEHICLE_YEAR': np.random.choice(
            ['before 2015', 'after 2015'],
            N, p=[0.45, 0.55]
        ),
        'MARRIED': np.random.choice([0, 1], N, p=[0.45, 0.55]),
        'CHILDREN': np.random.choice([0, 1], N, p=[0.50, 0.50]),
        'POSTAL_CODE': np.random.choice(
            [10238, 10065, 10068, 10007, 10009, 10048, 10032, 10081, 10015, 10022],
            N
        ),
        'ANNUAL_MILEAGE': np.round(np.random.uniform(5000, 25000, N), 0).astype(int),
        'VEHICLE_TYPE': np.random.choice(
            ['sedan', 'sports car'],
            N, p=[0.70, 0.30]
        ),
        'SPEEDING_VIOLATIONS': np.random.choice(
            [0, 1, 2, 3, 4, 5],
            N, p=[0.40, 0.25, 0.15, 0.10, 0.06, 0.04]
        ),
        'DUIS': np.random.choice(
            [0, 1, 2, 3],
            N, p=[0.70, 0.18, 0.08, 0.04]
        ),
        'PAST_ACCIDENTS': np.random.choice(
            [0, 1, 2, 3, 4, 5],
            N, p=[0.35, 0.25, 0.18, 0.12, 0.06, 0.04]
        ),
    }

    df = pd.DataFrame(data)

    # Generate OUTCOME based on realistic risk factors
    risk_score = np.zeros(N)

    # Age risk
    risk_score += np.where(df['AGE'] == '16-25', 0.15, 0)
    risk_score += np.where(df['AGE'] == '65+', 0.10, 0)

    # Experience risk (less experience = more risk)
    risk_score += np.where(df['DRIVING_EXPERIENCE'] == '0-9y', 0.15, 0)
    risk_score += np.where(df['DRIVING_EXPERIENCE'] == '10-19y', 0.05, 0)

    # Vehicle type risk
    risk_score += np.where(df['VEHICLE_TYPE'] == 'sports car', 0.12, 0)

    # Speeding violations
    risk_score += df['SPEEDING_VIOLATIONS'] * 0.08

    # DUIs
    risk_score += df['DUIS'] * 0.12

    # Past accidents
    risk_score += df['PAST_ACCIDENTS'] * 0.10

    # Credit score (lower = more risk)
    risk_score += (1 - df['CREDIT_SCORE']) * 0.08

    # Annual mileage (higher = more risk)
    risk_score += (df['ANNUAL_MILEAGE'] - 5000) / 20000 * 0.08

    # Vehicle year (older = more risk)
    risk_score += np.where(df['VEHICLE_YEAR'] == 'before 2015', 0.06, 0)

    # Add noise
    risk_score += np.random.normal(0, 0.08, N)

    # Convert to binary outcome
    threshold = np.percentile(risk_score, 74)  # ~26% claim rate
    df['OUTCOME'] = (risk_score >= threshold).astype(int)

    # Save
    df.to_csv('Car_Insurance_Claim.csv', index=False)

    total = len(df)
    claims = df['OUTCOME'].sum()
    print(f'Dataset generated: {total} records')
    print(f'  Claims filed (OUTCOME=1): {claims} ({claims/total*100:.1f}%)')
    print(f'  No claim (OUTCOME=0): {total - claims} ({(total-claims)/total*100:.1f}%)')
    print(f'  Columns: {list(df.columns)}')
    print(f'  Saved to: Car_Insurance_Claim.csv')


if __name__ == '__main__':
    generate_dataset()
