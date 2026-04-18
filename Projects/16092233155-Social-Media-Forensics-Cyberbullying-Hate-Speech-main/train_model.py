import pandas as pd
import numpy as np
import re
import os
import json
import joblib
import warnings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

warnings.filterwarnings('ignore')

LABEL_MAP = {0: "Hate Speech", 1: "Offensive", 2: "Clean"}
VIS_DIR = "static/vis"
os.makedirs(VIS_DIR, exist_ok=True)

# --- Text Preprocessing ---

try:
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
except Exception:
    import nltk
    nltk.download('stopwords', quiet=True)
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))


def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\.\S+', '', text)       # remove URLs
    text = re.sub(r'@\w+', '', text)                     # remove mentions
    text = re.sub(r'#\w+', '', text)                     # remove hashtags
    text = re.sub(r'[^a-zA-Z\s]', '', text)              # remove special chars/numbers
    text = re.sub(r'\s+', ' ', text).strip()              # normalize whitespace
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return ' '.join(words)


# --- EDA Visualizations ---

def generate_visualizations(df):
    plt.style.use('seaborn-v0_8-darkgrid')
    colors = ['#ef4444', '#f59e0b', '#22c55e']

    # 1. Class Distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    counts = df['label'].value_counts().sort_index()
    bars = ax.bar([LABEL_MAP[i] for i in counts.index], counts.values, color=colors)
    for bar, count in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
                str(count), ha='center', fontweight='bold', fontsize=12)
    ax.set_title('Class Distribution', fontsize=14, fontweight='bold')
    ax.set_ylabel('Count')
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/class_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  [1/8] Class distribution")

    # 2. Text Length Distribution
    fig, ax = plt.subplots(figsize=(10, 5))
    for label, color in zip([0, 1, 2], colors):
        subset = df[df['label'] == label]['text'].str.len()
        ax.hist(subset, bins=30, alpha=0.6, color=color, label=LABEL_MAP[label])
    ax.set_title('Text Length Distribution by Class', fontsize=14, fontweight='bold')
    ax.set_xlabel('Character Count')
    ax.set_ylabel('Frequency')
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/text_length_dist.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  [2/8] Text length distribution")

    # 3. Word Count Distribution
    fig, ax = plt.subplots(figsize=(10, 5))
    for label, color in zip([0, 1, 2], colors):
        subset = df[df['label'] == label]['text'].apply(lambda x: len(str(x).split()))
        ax.hist(subset, bins=25, alpha=0.6, color=color, label=LABEL_MAP[label])
    ax.set_title('Word Count Distribution by Class', fontsize=14, fontweight='bold')
    ax.set_xlabel('Word Count')
    ax.set_ylabel('Frequency')
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/word_count_dist.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  [3/8] Word count distribution")

    # 4. Word Cloud — Hate Speech
    try:
        from wordcloud import WordCloud
        hate_text = ' '.join(df[df['label'] == 0]['clean_text'].values)
        wc = WordCloud(width=800, height=400, background_color='black',
                       colormap='Reds', max_words=100).generate(hate_text)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Word Cloud — Hate Speech', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{VIS_DIR}/wordcloud_hate.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("  [4/8] Word cloud (hate speech)")
    except ImportError:
        # Generate bar chart of top words instead
        from collections import Counter
        hate_words = ' '.join(df[df['label'] == 0]['clean_text'].values).split()
        top_words = Counter(hate_words).most_common(20)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.barh([w[0] for w in top_words][::-1], [w[1] for w in top_words][::-1], color='#ef4444')
        ax.set_title('Top 20 Words — Hate Speech', fontsize=14, fontweight='bold')
        ax.set_xlabel('Frequency')
        plt.tight_layout()
        plt.savefig(f'{VIS_DIR}/wordcloud_hate.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("  [4/8] Top words (hate speech) — wordcloud not installed, using bar chart")

    # 5. Word Cloud — Clean
    try:
        from wordcloud import WordCloud
        clean_text = ' '.join(df[df['label'] == 2]['clean_text'].values)
        wc = WordCloud(width=800, height=400, background_color='black',
                       colormap='Greens', max_words=100).generate(clean_text)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Word Cloud — Clean Text', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{VIS_DIR}/wordcloud_clean.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("  [5/8] Word cloud (clean)")
    except ImportError:
        from collections import Counter
        clean_words = ' '.join(df[df['label'] == 2]['clean_text'].values).split()
        top_words = Counter(clean_words).most_common(20)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.barh([w[0] for w in top_words][::-1], [w[1] for w in top_words][::-1], color='#22c55e')
        ax.set_title('Top 20 Words — Clean Text', fontsize=14, fontweight='bold')
        ax.set_xlabel('Frequency')
        plt.tight_layout()
        plt.savefig(f'{VIS_DIR}/wordcloud_clean.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("  [5/8] Top words (clean) — wordcloud not installed, using bar chart")

    # 6. Top TF-IDF Features per Class
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    tfidf_temp = TfidfVectorizer(max_features=1000, stop_words='english')
    X_temp = tfidf_temp.fit_transform(df['clean_text'])
    feature_names = tfidf_temp.get_feature_names_out()
    for idx, (label, color, ax) in enumerate(zip([0, 1, 2], colors, axes)):
        mask = (df['label'] == label).values
        mean_tfidf = X_temp[mask].mean(axis=0).A1
        top_idx = mean_tfidf.argsort()[-15:][::-1]
        top_words_list = [feature_names[i] for i in top_idx]
        top_values = [mean_tfidf[i] for i in top_idx]
        ax.barh(top_words_list[::-1], top_values[::-1], color=color)
        ax.set_title(f'Top Features — {LABEL_MAP[label]}', fontweight='bold')
        ax.set_xlabel('Mean TF-IDF Score')
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/top_features.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  [6/8] Top TF-IDF features")

    print("  [7/8] Model comparison — generated after training")
    print("  [8/8] Confusion matrix — generated after training")


# --- Model Training ---

def train_models(X_train, X_test, y_train, y_test):
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Naive Bayes": MultinomialNB(),
        "SVM": CalibratedClassifierCV(LinearSVC(max_iter=2000, random_state=42), cv=3),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5, n_jobs=-1),
    }

    results = {}
    best_model = None
    best_accuracy = 0
    best_name = ""

    for name, model in models.items():
        print(f"  Training {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()

        results[name] = {
            "accuracy": round(acc * 100, 2),
            "precision": round(prec * 100, 2),
            "recall": round(rec * 100, 2),
            "f1": round(f1 * 100, 2),
            "confusion_matrix": cm,
        }
        print(f"    Accuracy: {acc*100:.2f}%  F1: {f1*100:.2f}%")

        if acc > best_accuracy:
            best_accuracy = acc
            best_model = model
            best_name = name

    return results, best_model, best_name


def plot_model_comparison(results):
    names = list(results.keys())
    accuracies = [results[n]["accuracy"] for n in names]
    f1s = [results[n]["f1"] for n in names]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    bars1 = ax1.barh(names[::-1], [accuracies[i] for i in range(len(names)-1, -1, -1)],
                     color=['#ef4444' if a == max(accuracies) else '#64748b' for a in reversed(accuracies)])
    ax1.set_title('Model Accuracy Comparison (%)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Accuracy (%)')
    for bar, val in zip(bars1, reversed(accuracies)):
        ax1.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                 f'{val}%', va='center', fontweight='bold')

    bars2 = ax2.barh(names[::-1], [f1s[i] for i in range(len(names)-1, -1, -1)],
                     color=['#ef4444' if f == max(f1s) else '#64748b' for f in reversed(f1s)])
    ax2.set_title('Model F1 Score Comparison (%)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('F1 Score (%)')
    for bar, val in zip(bars2, reversed(f1s)):
        ax2.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                 f'{val}%', va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/model_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  [7/8] Model comparison saved")


def plot_confusion_matrix(y_test, best_model, X_test, best_name):
    y_pred = best_model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    labels = [LABEL_MAP[i] for i in sorted(LABEL_MAP.keys())]

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Reds', xticklabels=labels, yticklabels=labels, ax=ax)
    ax.set_title(f'Confusion Matrix — {best_name}', fontsize=14, fontweight='bold')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    plt.tight_layout()
    plt.savefig(f'{VIS_DIR}/confusion_matrix.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  [8/8] Confusion matrix saved")


# --- Main ---

def main():
    print("Loading dataset...")
    df = pd.read_csv("hate_speech_data.csv")
    print(f"  {len(df)} rows loaded")

    print("\nPreprocessing text...")
    df['clean_text'] = df['text'].apply(preprocess_text)
    # Remove empty texts after preprocessing
    df = df[df['clean_text'].str.strip().str.len() > 0].reset_index(drop=True)
    print(f"  {len(df)} rows after cleaning")

    print("\nGenerating EDA visualizations...")
    generate_visualizations(df)

    print("\nVectorizing text with TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), min_df=2)
    X = vectorizer.fit_transform(df['clean_text'])
    y = df['label'].values
    print(f"  Feature matrix: {X.shape}")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"  Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")

    print("\nTraining models...")
    results, best_model, best_name = train_models(X_train, X_test, y_train, y_test)

    print(f"\nBest model: {best_name} ({results[best_name]['accuracy']}%)")

    plot_model_comparison(results)
    plot_confusion_matrix(y_test, best_model, X_test, best_name)

    # Save model and vectorizer
    joblib.dump(best_model, "hate_speech_model.pkl")
    joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
    print("\nModel saved: hate_speech_model.pkl")
    print("Vectorizer saved: tfidf_vectorizer.pkl")

    # Save models info
    info = {
        "models": results,
        "best_model": best_name,
        "train_size": X_train.shape[0],
        "test_size": X_test.shape[0],
        "n_features": X.shape[1],
        "labels": LABEL_MAP,
    }
    with open("models_info.json", "w") as f:
        json.dump(info, f, indent=2)
    print("Metrics saved: models_info.json")

    print("\n--- Classification Report (Best Model) ---")
    y_pred = best_model.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=list(LABEL_MAP.values())))


if __name__ == "__main__":
    main()
