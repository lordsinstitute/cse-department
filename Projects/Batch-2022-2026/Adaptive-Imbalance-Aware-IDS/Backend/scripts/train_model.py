"""
Train the NIDS detector on CICIDS2017 or UNSW-NB15 CSV data.

Usage:
  python -m scripts.train_model --dataset cicids --path data/raw/MachineLearningCSV.csv
  python -m scripts.train_model --dataset unsw --path data/raw/UNSW_NB15_traintest.csv --max-rows 100000
"""

import argparse
import json
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data.datasets import get_dataset_path, load_cicids_csv, load_unsw_csv
from app.ml.train_pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(description="Train NIDS ML model")
    parser.add_argument("--dataset", choices=["cicids", "unsw"], default="cicids")
    parser.add_argument("--path", type=str, help="Path to CSV (overrides env)")
    parser.add_argument("--max-rows", type=int, default=None)
    parser.add_argument("--output-dir", type=str, default="models")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--val-size", type=float, default=0.1")
    args = parser.parse_args()

    path = args.path or get_dataset_path(args.dataset)
    if not path or not os.path.isfile(path):
        print("Error: CSV not found. Set --path or put CICIDS/UNSW CSV in data/raw/")
        sys.exit(1)

    if args.dataset == "cicids":
        rows_labels = list(load_cicids_csv(path, max_rows=args.max_rows))
    else:
        rows_labels = list(load_unsw_csv(path, max_rows=args.max_rows))

    if not rows_labels:
        print("Error: No rows loaded from CSV")
        sys.exit(1)

    feature_rows = [r for r, _ in rows_labels]
    labels = [lbl for _, lbl in rows_labels]
    print(f"Loaded {len(feature_rows)} samples, {len(set(labels))} classes")

    results = run_pipeline(
        feature_rows,
        labels,
        output_dir=args.output_dir,
        test_size=args.test_size,
        val_size=args.val_size,
        save_model=True,
    )

    print("\n--- Test set metrics ---")
    t = results["test"]
    print(f"Accuracy:  {t['accuracy']:.4f}")
    print(f"Precision: {t['precision']:.4f}")
    print(f"Recall:   {t['recall']:.4f}")
    print(f"F1:       {t['f1']:.4f}")
    print("\nConfusion matrix (labels):", t["labels"])
    for row in t["confusion_matrix"]:
        print(row)
    print("\nClassification report:\n", t["classification_report"])
    print("Model saved to:", results.get("model_path"))


if __name__ == "__main__":
    main()
