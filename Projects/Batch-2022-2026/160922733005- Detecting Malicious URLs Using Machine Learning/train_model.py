"""
Train ML models for Malicious URL Detection.
Compares: Logistic Regression, KNN, SVM, Naive Bayes, Decision Tree,
          Random Forest, Gradient Boosting, MLP.
Generates EDA visualizations and saves the best model.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report)
import pickle
import json
import os
import warnings
warnings.filterwarnings('ignore')

VIS_DIR = 'static/vis'
os.makedirs(VIS_DIR, exist_ok=True)


def load_and_prepare():
    """Load dataset and prepare features."""
    df = pd.read_csv('malicious_urls.csv')

    # Feature columns (everything except ID, url, label)
    feature_cols = [c for c in df.columns if c not in ['ID', 'url', 'label']]
    X = df[feature_cols]
    y = df['label']

    print(f'  Total records: {len(df)}')
    print(f'  Features: {len(feature_cols)}')
    print(f'  Legitimate: {(y == 0).sum()} | Malicious: {(y == 1).sum()}')

    return df, X, y, feature_cols


def generate_visualizations(df, feature_cols):
    """Generate EDA visualizations for the web app."""
    sns.set_theme(style='darkgrid')

    # 1. Label Distribution (Pie Chart)
    fig, ax = plt.subplots(figsize=(6, 6))
    counts = df['label'].value_counts()
    ax.pie(counts, labels=['Legitimate', 'Malicious'], autopct='%1.1f%%',
           colors=['#2ecc71', '#e74c3c'], startangle=90,
           textprops={'fontsize': 13, 'fontweight': 'bold'})
    ax.set_title('URL Distribution', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/label_dist.png', dpi=100)
    plt.close()

    # 2. URL Length Distribution
    fig, ax = plt.subplots(figsize=(10, 5))
    df[df['label'] == 0]['url_length'].hist(bins=50, alpha=0.6, label='Legitimate', color='#2ecc71', ax=ax)
    df[df['label'] == 1]['url_length'].hist(bins=50, alpha=0.6, label='Malicious', color='#e74c3c', ax=ax)
    ax.set_title('URL Length Distribution', fontsize=14, fontweight='bold')
    ax.set_xlabel('URL Length')
    ax.set_ylabel('Count')
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/url_length.png', dpi=100)
    plt.close()

    # 3. HTTPS vs HTTP
    fig, ax = plt.subplots(figsize=(8, 5))
    ct = pd.crosstab(df['has_https'].map({0: 'HTTP', 1: 'HTTPS'}),
                     df['label'].map({0: 'Legitimate', 1: 'Malicious'}))
    ct.plot(kind='bar', color=['#2ecc71', '#e74c3c'], ax=ax)
    ax.set_title('Protocol (HTTP vs HTTPS) by Label', fontsize=14, fontweight='bold')
    ax.set_xlabel('Protocol')
    ax.set_ylabel('Count')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/https_dist.png', dpi=100)
    plt.close()

    # 4. IP Address Presence
    fig, ax = plt.subplots(figsize=(8, 5))
    ct = pd.crosstab(df['has_ip'].map({0: 'No IP', 1: 'Has IP'}),
                     df['label'].map({0: 'Legitimate', 1: 'Malicious'}))
    ct.plot(kind='bar', color=['#2ecc71', '#e74c3c'], ax=ax)
    ax.set_title('IP Address in URL by Label', fontsize=14, fontweight='bold')
    ax.set_xlabel('IP Address Present')
    ax.set_ylabel('Count')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/ip_dist.png', dpi=100)
    plt.close()

    # 5. Suspicious Words Count
    fig, ax = plt.subplots(figsize=(10, 5))
    df[df['label'] == 0]['n_suspicious_words'].hist(bins=10, alpha=0.6, label='Legitimate', color='#2ecc71', ax=ax)
    df[df['label'] == 1]['n_suspicious_words'].hist(bins=10, alpha=0.6, label='Malicious', color='#e74c3c', ax=ax)
    ax.set_title('Suspicious Words Count', fontsize=14, fontweight='bold')
    ax.set_xlabel('Number of Suspicious Words')
    ax.set_ylabel('Count')
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/suspicious_words.png', dpi=100)
    plt.close()

    # 6. Domain Length Distribution
    fig, ax = plt.subplots(figsize=(10, 5))
    df[df['label'] == 0]['domain_length'].hist(bins=40, alpha=0.6, label='Legitimate', color='#2ecc71', ax=ax)
    df[df['label'] == 1]['domain_length'].hist(bins=40, alpha=0.6, label='Malicious', color='#e74c3c', ax=ax)
    ax.set_title('Domain Length Distribution', fontsize=14, fontweight='bold')
    ax.set_xlabel('Domain Length')
    ax.set_ylabel('Count')
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/domain_length.png', dpi=100)
    plt.close()

    # 7. Number of Subdomains
    fig, ax = plt.subplots(figsize=(10, 5))
    df[df['label'] == 0]['n_subdomains'].hist(bins=10, alpha=0.6, label='Legitimate', color='#2ecc71', ax=ax)
    df[df['label'] == 1]['n_subdomains'].hist(bins=10, alpha=0.6, label='Malicious', color='#e74c3c', ax=ax)
    ax.set_title('Number of Subdomains', fontsize=14, fontweight='bold')
    ax.set_xlabel('Subdomains')
    ax.set_ylabel('Count')
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/subdomains.png', dpi=100)
    plt.close()

    # 8. Correlation Heatmap
    fig, ax = plt.subplots(figsize=(14, 11))
    numeric = df[feature_cols + ['label']]
    corr = numeric.corr()
    sns.heatmap(corr, annot=False, cmap='RdYlBu_r', ax=ax, linewidths=0.3, fmt='.1f')
    ax.set_title('Feature Correlation Heatmap', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/correlation.png', dpi=100)
    plt.close()

    # 9. Special Characters Ratio
    fig, ax = plt.subplots(figsize=(10, 5))
    df[df['label'] == 0]['special_ratio'].hist(bins=30, alpha=0.6, label='Legitimate', color='#2ecc71', ax=ax)
    df[df['label'] == 1]['special_ratio'].hist(bins=30, alpha=0.6, label='Malicious', color='#e74c3c', ax=ax)
    ax.set_title('Special Character Ratio', fontsize=14, fontweight='bold')
    ax.set_xlabel('Ratio of Special Characters')
    ax.set_ylabel('Count')
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/special_ratio.png', dpi=100)
    plt.close()

    # 10. URL Depth
    fig, ax = plt.subplots(figsize=(10, 5))
    df[df['label'] == 0]['url_depth'].hist(bins=15, alpha=0.6, label='Legitimate', color='#2ecc71', ax=ax)
    df[df['label'] == 1]['url_depth'].hist(bins=15, alpha=0.6, label='Malicious', color='#e74c3c', ax=ax)
    ax.set_title('URL Path Depth', fontsize=14, fontweight='bold')
    ax.set_xlabel('Depth (number of path segments)')
    ax.set_ylabel('Count')
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/url_depth.png', dpi=100)
    plt.close()

    print(f'  Saved 10 visualizations to {VIS_DIR}/')


def train_models(X, y, feature_cols):
    """Train multiple ML models and compare performance."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        'Logistic Regression': make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=42)),
        'K-Nearest Neighbors': make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)),
        'SVM': make_pipeline(StandardScaler(), SVC(kernel='rbf', probability=True, random_state=42)),
        'Naive Bayes': GaussianNB(),
        'Decision Tree': DecisionTreeClassifier(max_depth=20, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, max_depth=4,
                                                         learning_rate=0.1, random_state=42),
        'MLP Neural Network': make_pipeline(StandardScaler(), MLPClassifier(hidden_layer_sizes=(100, 50),
                                                                             max_iter=500, random_state=42)),
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
            'accuracy': acc, 'precision': prec, 'recall': rec,
            'f1': f1, 'confusion_matrix': cm
        }
        print(f'    Accuracy: {acc}%  F1: {f1}%')

        if acc > best_acc:
            best_acc = acc
            best_name = name
            best_model = model

    # Save best model
    with open('url_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    print(f'\n  Best model: {best_name} ({best_acc}%) -> saved to url_model.pkl')

    # Feature importance (from Random Forest)
    rf = models['Random Forest']
    importance = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(10, 8))
    importance.plot(kind='barh', color='#e67e22', ax=ax)
    ax.set_title('Feature Importance (Random Forest)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Importance')
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/feature_importance.png', dpi=100)
    plt.close()

    # Confusion matrix for best model
    y_pred_best = best_model.predict(X_test)
    cm_best = confusion_matrix(y_test, y_pred_best)

    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(cm_best, annot=True, fmt='d', cmap='YlOrBr',
                xticklabels=['Legitimate', 'Malicious'],
                yticklabels=['Legitimate', 'Malicious'], ax=ax)
    ax.set_title(f'Confusion Matrix ({best_name})', fontsize=14, fontweight='bold')
    ax.set_ylabel('Actual')
    ax.set_xlabel('Predicted')
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/confusion_matrix.png', dpi=100)
    plt.close()

    # Save all results
    with open('models_info.json', 'w') as f:
        json.dump({
            'models': results,
            'best_model': best_name,
            'features': feature_cols,
            'test_size': len(X_test),
            'train_size': len(X_train)
        }, f, indent=2)

    return results


if __name__ == '__main__':
    print('=' * 55)
    print('Malicious URL Detection - Model Training')
    print('=' * 55)

    print('\n[1/3] Loading dataset...')
    df, X, y, feature_cols = load_and_prepare()

    print('\n[2/3] Generating EDA visualizations...')
    generate_visualizations(df, feature_cols)

    print('\n[3/3] Training ML models...')
    results = train_models(X, y, feature_cols)

    print('\n' + '=' * 55)
    print('Results Summary:')
    print('=' * 55)
    for name, m in sorted(results.items(), key=lambda x: -x[1]['accuracy']):
        print(f'  {name}: Accuracy={m["accuracy"]}% F1={m["f1"]}%')

    print(f'\nFiles saved:')
    print(f'  url_model.pkl       (Best trained model)')
    print(f'  models_info.json    (All metrics)')
    print(f'  static/vis/         (12 visualizations)')
    print('Done!')
