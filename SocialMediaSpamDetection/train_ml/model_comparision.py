import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.sparse as sp

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from xgboost import XGBClassifier

from preprocessing import preprocess_dataframe, vectorize_text
from config import TRAIN_PATH, EVAL_PATH


# ----------------------------
# Load dataset
# ----------------------------

df = pd.read_csv(TRAIN_PATH)
df = preprocess_dataframe(df)


# ----------------------------
# Text vectorization
# ----------------------------

X_text, vectorizer = vectorize_text(df['clean_tweet'])


# ----------------------------
# Numeric features
# ----------------------------

numeric_features = df[['followers','following','actions',
                       'tweet_length','follower_following_ratio']].values

X = sp.hstack((X_text, numeric_features))
y = df['Type'].map({'Quality':0, 'Spam':1})


# ----------------------------
# Train test split
# ----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# ----------------------------
# Models
# ----------------------------

models = {

    "LogisticRegression": LogisticRegression(max_iter=1000),
    "NaiveBayes": MultinomialNB(),
    "RandomForest": RandomForestClassifier(n_estimators=200),
    "SVM": LinearSVC(),
    "XGBoost": XGBClassifier(
        eval_metric='logloss',
        use_label_encoder=False
    )
}


results = {}


# ----------------------------
# Training loop
# ----------------------------

for name, model in models.items():

    print(f"Training {name}")
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    results[name] = acc

    # ----------------------------
    # Save classification report
    # ----------------------------

    report = classification_report(y_test, preds)

    with open(EVAL_PATH + f"classification_report_{name}.txt", "w") as f:
        f.write(report)


    # ----------------------------
    # Confusion Matrix
    # ----------------------------

    cm = confusion_matrix(y_test, preds)
    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title(f"{name} Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.savefig(EVAL_PATH + f"confusion_{name}.png")
    plt.close()
    print(f"{name} Accuracy:", acc)


# ----------------------------
# Accuracy Comparison Graph
# ----------------------------

plt.figure(figsize=(8,6))

sns.barplot(x=list(results.keys()), y=list(results.values()))
plt.ylabel("Accuracy")
plt.xlabel("Models")
plt.title("Model Accuracy Comparison")
plt.xticks(rotation=30)
plt.savefig(EVAL_PATH + "model_accuracy_comparison.png")
plt.close()


print("Evaluation results saved in static/eval/")