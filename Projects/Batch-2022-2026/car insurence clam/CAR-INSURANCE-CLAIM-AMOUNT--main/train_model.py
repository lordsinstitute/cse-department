"""
Train ML models for Car Insurance Claim Prediction.
Compares: Random Forest, Gradient Boosting, SVM, Logistic Regression.
Generates EDA visualizations and saves model metrics.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import pickle
import json
import os
import warnings
warnings.filterwarnings('ignore')

VIS_DIR = 'static/vis'
os.makedirs(VIS_DIR, exist_ok=True)


def load_and_preprocess():
    """Load dataset and encode categorical features."""
    df = pd.read_csv('Car_Insurance_Claim.csv')

    # Separate features and target
    X = df.drop(['ID', 'OUTCOME'], axis=1)
    y = df['OUTCOME']

    # Identify feature types
    categorical = [c for c in X.columns if not pd.api.types.is_numeric_dtype(X[c])]
    continuous = [c for c in X.columns if pd.api.types.is_numeric_dtype(X[c])]

    print(f'  Total features: {len(X.columns)}')
    print(f'  Categorical: {categorical}')
    print(f'  Continuous: {continuous}')

    # Label encode categorical features
    encoders = {}
    for col in categorical:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        encoders[col] = le

    # Save encoders
    with open('encoders.pkl', 'wb') as f:
        pickle.dump(encoders, f)

    return df, X, y, categorical, continuous, encoders


def generate_visualizations(df):
    """Generate EDA visualizations for the web app."""
    sns.set_theme(style='darkgrid')

    # 1. Gender vs Outcome
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(x='GENDER', hue='OUTCOME', data=df, palette='YlOrBr_r', ax=ax)
    ax.set_title('Gender vs Claim Outcome', fontsize=14, fontweight='bold')
    ax.legend(title='Outcome', labels=['No Claim', 'Claim Filed'])
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/gender.png', dpi=100)
    plt.close()

    # 2. Driving Experience vs Outcome
    fig, ax = plt.subplots(figsize=(8, 5))
    order = ['0-9y', '10-19y', '20-29y', '30y+']
    sns.countplot(x='DRIVING_EXPERIENCE', hue='OUTCOME', data=df, palette='YlOrBr_r',
                  ax=ax, order=order)
    ax.set_title('Driving Experience vs Claim Outcome', fontsize=14, fontweight='bold')
    ax.legend(title='Outcome', labels=['No Claim', 'Claim Filed'])
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/drive.png', dpi=100)
    plt.close()

    # 3. Vehicle Type vs Outcome
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(x='VEHICLE_TYPE', hue='OUTCOME', data=df, palette='YlOrBr_r', ax=ax)
    ax.set_title('Vehicle Type vs Claim Outcome', fontsize=14, fontweight='bold')
    ax.legend(title='Outcome', labels=['No Claim', 'Claim Filed'])
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/vtype.png', dpi=100)
    plt.close()

    # 4. Education vs Outcome
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(x='EDUCATION', hue='OUTCOME', data=df, palette='YlOrBr_r', ax=ax)
    ax.set_title('Education Level vs Claim Outcome', fontsize=14, fontweight='bold')
    ax.legend(title='Outcome', labels=['No Claim', 'Claim Filed'])
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/edu.png', dpi=100)
    plt.close()

    # 5. Vehicle Year vs Outcome
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(x='VEHICLE_YEAR', hue='OUTCOME', data=df, palette='YlOrBr_r', ax=ax)
    ax.set_title('Vehicle Year vs Claim Outcome', fontsize=14, fontweight='bold')
    ax.legend(title='Outcome', labels=['No Claim', 'Claim Filed'])
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/vyear.png', dpi=100)
    plt.close()

    # 6. Age vs Outcome
    fig, ax = plt.subplots(figsize=(8, 5))
    order = ['16-25', '26-39', '40-64', '65+']
    sns.countplot(x='AGE', hue='OUTCOME', data=df, palette='YlOrBr_r', ax=ax, order=order)
    ax.set_title('Age Group vs Claim Outcome', fontsize=14, fontweight='bold')
    ax.legend(title='Outcome', labels=['No Claim', 'Claim Filed'])
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/age.png', dpi=100)
    plt.close()

    # 7. Income vs Outcome
    fig, ax = plt.subplots(figsize=(8, 5))
    order = ['poverty', 'working class', 'middle class', 'upper class']
    sns.countplot(x='INCOME', hue='OUTCOME', data=df, palette='YlOrBr_r', ax=ax, order=order)
    ax.set_title('Income Level vs Claim Outcome', fontsize=14, fontweight='bold')
    ax.legend(title='Outcome', labels=['No Claim', 'Claim Filed'])
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/income.png', dpi=100)
    plt.close()

    # 8. Correlation heatmap (numeric columns only)
    fig, ax = plt.subplots(figsize=(10, 8))
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='YlOrBr', ax=ax, linewidths=0.5)
    ax.set_title('Feature Correlation Heatmap', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/correlation.png', dpi=100)
    plt.close()

    # 9. Outcome distribution pie chart
    fig, ax = plt.subplots(figsize=(6, 6))
    counts = df['OUTCOME'].value_counts()
    ax.pie(counts, labels=['No Claim', 'Claim Filed'], autopct='%1.1f%%',
           colors=['#2ecc71', '#e74c3c'], startangle=90,
           textprops={'fontsize': 13, 'fontweight': 'bold'})
    ax.set_title('Claim Distribution', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/outcome_dist.png', dpi=100)
    plt.close()

    print(f'  Saved 9 visualizations to {VIS_DIR}/')


def train_models(X, y):
    """Train multiple ML models and compare performance."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'SVM': make_pipeline(StandardScaler(), SVC(kernel='rbf', probability=True, random_state=42)),
        'Logistic Regression': make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42)),
    }

    results = {}
    best_acc = 0
    best_name = None
    best_model = None

    for name, model in models.items():
        print(f'  Training {name}...')
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = round(accuracy_score(y_test, y_pred) * 100, 2)
        prec = round(precision_score(y_test, y_pred) * 100, 2)
        rec = round(recall_score(y_test, y_pred) * 100, 2)
        f1 = round(f1_score(y_test, y_pred) * 100, 2)
        cm = confusion_matrix(y_test, y_pred).tolist()

        results[name] = {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1': f1,
            'confusion_matrix': cm
        }
        print(f'    Accuracy: {acc}%  F1: {f1}%')

        if acc > best_acc:
            best_acc = acc
            best_name = name
            best_model = model

    # Save best model
    with open('claim_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    print(f'\n  Best model: {best_name} ({best_acc}%) → saved to claim_model.pkl')

    # Feature importance (from Random Forest)
    rf = models['Random Forest']
    importance = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(10, 7))
    importance.plot(kind='barh', color='#e67e22', ax=ax)
    ax.set_title('Feature Importance (Random Forest)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Importance')
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/feature_importance.png', dpi=100)
    plt.close()

    # Save all results
    feature_list = list(X.columns)
    with open('models_info.json', 'w') as f:
        json.dump({
            'models': results,
            'best_model': best_name,
            'features': feature_list,
            'test_size': len(X_test),
            'train_size': len(X_train)
        }, f, indent=2)

    return results


if __name__ == '__main__':
    print('=' * 55)
    print('Car Insurance Claim Prediction - Model Training')
    print('=' * 55)

    print('\n[1/3] Loading and preprocessing dataset...')
    df, X, y, categorical, continuous, encoders = load_and_preprocess()

    print('\n[2/3] Generating EDA visualizations...')
    generate_visualizations(df)

    print('\n[3/3] Training ML models...')
    results = train_models(X, y)

    print('\n' + '=' * 55)
    print('Results Summary:')
    print('=' * 55)
    for name, metrics in results.items():
        print(f'  {name}: Accuracy={metrics["accuracy"]}% F1={metrics["f1"]}%')

    print(f'\nFiles saved:')
    print(f'  claim_model.pkl     (Best trained model)')
    print(f'  encoders.pkl        (Label encoders)')
    print(f'  models_info.json    (All metrics)')
    print(f'  static/vis/         (10 visualizations)')
    print('Done!')
