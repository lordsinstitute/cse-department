from flask import Flask, render_template, request
import os
import joblib
import numpy as np

from train_agents_ai.agent_system import detect_spam

app = Flask(__name__)

MODEL_PATH = "models/twitter_spam_model.pkl"
VECTORIZER_PATH = "models/tfidf_vectorizer.pkl"

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


EDA_FOLDER = "static/eda"
EVAL_FOLDER = "static/eval"


@app.route("/")
def home():
    return render_template("home.html")


# -----------------------------
# ML PAGES
# -----------------------------

@app.route("/ml/eda")
def eda():

    images = os.listdir(EDA_FOLDER)

    return render_template(
        "ml/eda.html",
        images=images
    )


@app.route("/ml/compare")
def compare():

    files = os.listdir(EVAL_FOLDER)

    matrices = [f for f in files if f.startswith("confusion_")]

    reports = [f for f in files if f.startswith("classification_report_")]

    return render_template(
        "ml/compare.html",
        matrices=matrices,
        reports=reports
    )


@app.route("/ml/best")
def best_model():

    files = os.listdir(EVAL_FOLDER)

    matrix = [f for f in files if "best_model_confusion" in f]

    report = [f for f in files if "best_model_classification" in f]

    report_text = ""

    if report:
        with open(os.path.join(EVAL_FOLDER, report[0])) as f:
            report_text = f.read()

    return render_template(
        "ml/best_model.html",
        matrix=matrix,
        report=report,
        report_text=report_text
    )


@app.route("/ml/predict", methods=["GET","POST"])
def ml_predict():

    result = None
    confidence = None

    if request.method == "POST":

        tweet = request.form["tweet"]

        followers = int(request.form["followers"])
        following = int(request.form["following"])
        actions = int(request.form["actions"])

        tweet_vec = vectorizer.transform([tweet])

        features = np.array([[followers,following,actions, len(tweet), followers/(following+1)]])

        from scipy.sparse import hstack

        X = hstack((tweet_vec,features))

        pred = model.predict(X)[0]

        prob = model.predict_proba(X)[0].max()

        label = "Spam" if pred==1 else "Quality"

        result = label
        confidence = round(prob*100,2)

    return render_template(
        "ml/prediction.html",
        result=result,
        confidence=confidence
    )


# -----------------------------
# AGENTIC AI
# -----------------------------

import json

def clean_json(data):

    # If already dictionary, return it
    if isinstance(data, dict):
        return data

    # If string, clean it
    if isinstance(data, str):

        text = data.strip()

        if text.startswith("```"):
            text = text.split("```")[1]

        text = text.replace("json", "", 1).strip()

        return json.loads(text)

    return {}

@app.route("/agentic_ai", methods=["GET","POST"])
def agentic():
    output = None

    if request.method == "POST":
        tweet = request.form["tweet"]
        followers = int(request.form["followers"])
        following = int(request.form["following"])
        actions = int(request.form["actions"])

        result = detect_spam(tweet, followers, following, actions)

        output = {
            "content": clean_json(result["content_agent"]),
            "behavior": clean_json(result["behavior_agent"]),
            "link": clean_json(result["link_agent"]),
            "decision": clean_json(result["decision"])
        }

    return render_template(
        "agentic/agentic_ai1.html",
        output=output
    )

if __name__ == "__main__":
    app.run(debug=True)