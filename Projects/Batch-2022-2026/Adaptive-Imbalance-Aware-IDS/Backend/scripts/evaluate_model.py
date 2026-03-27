"""
Evaluate the trained NIDS model on a test CSV.

Prints confusion matrix, accuracy, precision, recall, F1, and false positive rate.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data.datasets import load_cicids_csv, load_unsw_csv
from app.data.features import features_to_vector
from app.data.features import FEATURE_NAMES
from app.ml.train_pipeline import evaluate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=["cicids", "unsw"], default="cicids")
    parser.add_argument("--path", type=str, required=True)
    parser.add_argument("--model-path", type=str, default="models/detector.joblib")
    parser.add_argument("--max-rows", type=int, default=None)
    args = parser.parse_args()

    if not os.path.isfile(args.model_path):
        print(f"Model not found: {args.model_path}. Train first with scripts.train_model")
        sys.exit(1)

    import joblib
    bundle = joblib.load(args.model_path)
    model = bundle["model"]
    le = bundle["label_encoder"]

    if args.dataset == "cicids":
        rows_labels = list(load_cicids_csv(args.path, max_rows=args.max_rows))
    else:
        rows_labels = list(load_unsw_csv(args.path, max_rows=args.max_rows))

    feature_rows = [r for r, _ in rows_labels]
    labels = [lbl for _, lbl in rows_labels]
    X = [features_to_vector(r, FEATURE_NAMES) for r in feature_rows]
    import numpy as np
    X = np.array(X)
    y = []
    for lbl in labels:
        if lbl in le.classes_:
            y.append(lbl)
        else:
            y.append("unknown")
    y = le.transform(y)

    metrics = evaluate(model, X, y, le)
    tn = 0
    fp = 0
    fn = 0
    tp = 0
    cm = metrics["confusion_matrix"]
    labels_list = metrics["labels"]
    if len(labels_list) == 2 and len(cm) == 2:
        # binary: assume benign=0, malicious=1
        tn, fp, fn, tp = cm[0][0], cm[0][1], cm[1][0], cm[1][1]
    else:
        # multiclass: benign vs rest
        if "benign" in labels_list:
            benign_idx = labels_list.index("benign")
            tn = cm[benign_idx][benign_idx]
            fp = sum(cm[benign_idx][j] for j in range(len(labels_list)) if j != benign_idx)
            fn = sum(cm[i][benign_idx] for i in range(len(labels_list)) if i != benign_idx)
            tp = sum(cm[i][j] for i in range(len(labels_list)) for j in range(len(labels_list)) if i != benign_idx and j != benign_idx)

    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    print("Accuracy:", metrics["accuracy"])
    print("Precision:", metrics["precision"])
    print("Recall:", metrics["recall"])
    print("F1:", metrics["f1"])
    print("False positive rate (benign predicted as attack):", fpr)
    print("Confusion matrix:\n", metrics["confusion_matrix"])
    print("Labels:", metrics["labels"])
    print("\nClassification report:\n", metrics["classification_report"])


if __name__ == "__main__":
    main()
