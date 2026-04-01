import pandas as pd
import joblib
import scipy.sparse as sp
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

from xgboost import XGBClassifier

from preprocessing import preprocess_dataframe, vectorize_text
from config import TRAIN_PATH, MODEL_PATH, VECTORIZER_PATH, EVAL_PATH


# ----------------------------
# Load dataset
# ----------------------------

df = pd.read_csv(TRAIN_PATH)

df = preprocess_dataframe(df)


# ----------------------------
# Text Vectorization
# ----------------------------

X_text, vectorizer = vectorize_text(df['clean_tweet'])


# ----------------------------
# Numeric Features
# ----------------------------

numeric_features = df[['followers','following','actions',
                       'tweet_length','follower_following_ratio']].values

X = sp.hstack((X_text, numeric_features))


y = df['Type'].map({'Quality':0, 'Spam':1})


# ----------------------------
# Train/Test Split
# ----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# ----------------------------
# Best Model (XGBoost)
# ----------------------------

model = XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    eval_metric='logloss'
)


print("Training Best Model (XGBoost)...")

model.fit(X_train, y_train)


# ----------------------------
# Predictions
# ----------------------------

preds = model.predict(X_test)


# ----------------------------
# Classification Report
# ----------------------------

report = classification_report(y_test, preds)

print("\n===== CLASSIFICATION REPORT =====\n")

print(report)

with open(EVAL_PATH + "best_model_classification_report.txt", "w") as f:
    f.write(report)


# ----------------------------
# Confusion Matrix
# ----------------------------

cm = confusion_matrix(y_test, preds)

print("\n===== CONFUSION MATRIX =====\n")

print(cm)


# ----------------------------
# Confusion Matrix Plot
# ----------------------------

plt.figure(figsize=(6,5))

sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")

plt.title("Best Model Confusion Matrix (XGBoost)")

plt.xlabel("Predicted")

plt.ylabel("Actual")

plt.savefig(EVAL_PATH + "best_model_confusion_matrix.png")

plt.close()


# ----------------------------
# Save Model
# ----------------------------

joblib.dump(model, MODEL_PATH)

joblib.dump(vectorizer, VECTORIZER_PATH)

print("\nModel saved successfully.")