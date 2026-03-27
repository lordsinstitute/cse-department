import os

TRAIN_PATH = "../data/train.csv"

EDA_PATH = "../static/eda/"
EVAL_PATH = "../static/eval/"

MODEL_PATH = "../models/twitter_spam_model.pkl"
VECTORIZER_PATH = "../models/tfidf_vectorizer.pkl"

os.makedirs(EDA_PATH, exist_ok=True)
os.makedirs(EVAL_PATH, exist_ok=True)
os.makedirs("../models", exist_ok=True)