from __future__ import annotations

import logging
import os
from typing import Any, Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import (
    AdaBoostClassifier,
    BaggingClassifier,
    RandomForestClassifier,
    VotingClassifier,
)
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import learning_curve, train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

logger = logging.getLogger(__name__)


class MLService:
    def __init__(self, model_path: str, dataset_path: str, static_pimg: str) -> None:
        self.model_path = model_path
        self.dataset_path = dataset_path
        self.static_pimg = static_pimg
        self._model = None
        self._load_model()

    def _load_model(self) -> None:
        if not os.path.exists(self.model_path):
            logger.warning("Model file not found: %s", self.model_path)
            return
        try:
            import tensorflow as tf
            self._model = tf.keras.models.load_model(self.model_path)
            logger.info("Model loaded: %s", self.model_path)
        except Exception as exc:
            logger.error("Failed to load model: %s", exc)
            self._model = None

    def _preprocess(self, dataset_path: str) -> tuple[np.ndarray, np.ndarray]:
        dataset = pd.read_csv(dataset_path)
        X = dataset.iloc[:, :-2].values
        Y = dataset.iloc[:, 12].values

        label_encoders: list[LabelEncoder] = []
        for i in range(11):
            le = LabelEncoder()
            X[:, i] = le.fit_transform(X[:, i].astype(str))
            label_encoders.append(le)

        imputer_const = SimpleImputer(missing_values=np.nan, strategy="constant")
        X[:, [8]] = imputer_const.fit_transform(X[:, [8]])

        imputer_mean = SimpleImputer(missing_values=np.nan, strategy="mean")
        X[:, [10]] = imputer_mean.fit_transform(X[:, [10]])

        X = np.array(X, dtype=np.float64)
        sc = StandardScaler()
        X = sc.fit_transform(X)

        y_le = LabelEncoder()
        Y = y_le.fit_transform(Y)

        indices = np.arange(X.shape[0])
        np.random.shuffle(indices)
        X, Y = X[indices], Y[indices]

        pca = PCA(n_components=10)
        X = pca.fit_transform(X)
        return X, Y

    def _save_learning_curve(
        self, model: Any, X: np.ndarray, Y: np.ndarray, title: str, filename: str
    ) -> None:
        train_sizes, train_scores, test_scores = learning_curve(
            model, X, Y, cv=10, scoring="accuracy", n_jobs=-1,
            train_sizes=np.linspace(0.01, 1.0, 50),
        )
        train_mean = np.mean(train_scores, axis=1)
        train_std = np.std(train_scores, axis=1)
        test_mean = np.mean(test_scores, axis=1)
        test_std = np.std(test_scores, axis=1)

        plt.figure(figsize=(10, 10))
        plt.plot(train_sizes, train_mean, "--", color="#111111", label="Train score")
        plt.plot(train_sizes, test_mean, color="#111111", label="Test score")
        plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, color="#e4f2f7")
        plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, color="#e4f2f7")
        plt.title(title)
        plt.xlabel("Training Size")
        plt.ylabel("Accuracy")
        plt.legend(loc="best")
        plt.tight_layout()
        plt.savefig(os.path.join(self.static_pimg, filename))
        plt.close()

    def _calc_metrics(
        self, predict: np.ndarray, y_test: np.ndarray, name: str
    ) -> dict[str, float]:
        return {
            "name": name,
            "accuracy": round(accuracy_score(y_test, predict) * 100, 2),
            "precision": round(precision_score(y_test, predict, average="macro") * 100, 2),
            "recall": round(recall_score(y_test, predict, average="macro") * 100, 2),
            "fscore": round(f1_score(y_test, predict, average="macro") * 100, 2),
        }

    def predict(self, params: list[float]) -> int:
        if self._model is None:
            raise RuntimeError("No model loaded. Train a model first.")
        x_new = np.array([params])
        y_new = self._model.predict(x_new)
        result = int(round(float(y_new[0][0])))
        logger.info("Prediction made: %d", result)
        return result

    def predict_batch(self, records: list[list[float]]) -> list[int]:
        if self._model is None:
            raise RuntimeError("No model loaded. Train a model first.")
        x_new = np.array(records)
        y_new = self._model.predict(x_new)
        return [int(round(float(y[0]))) for y in y_new]

    def compare_algorithms(self) -> list[dict[str, float]]:
        logger.info("Starting algorithm comparison")
        X, Y = self._preprocess(self.dataset_path)
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

        results: list[dict[str, float]] = []

        models: list[tuple[str, Any, str]] = [
            ("Bagging Classifier", BaggingClassifier(estimator=SVC(), n_estimators=10, random_state=20), "bag.jpg"),
            ("Gaussian Naive Bayes", GaussianNB(), "gnb.jpg"),
            ("AdaBoost Classifier", AdaBoostClassifier(n_estimators=100, random_state=0), "ab.jpg"),
            (
                "Voting Classifier",
                VotingClassifier(
                    estimators=[
                        ("lr", LogisticRegression(multi_class="multinomial", random_state=1)),
                        ("rf", RandomForestClassifier(n_estimators=50, random_state=1)),
                        ("gnb", GaussianNB()),
                    ],
                    voting="hard",
                ),
                "vc.jpg",
            ),
            ("Decision Tree Classifier", DecisionTreeClassifier(criterion="gini"), "dt.jpg"),
        ]

        for name, model, plot_file in models:
            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            metrics = self._calc_metrics(pred, y_test, name)
            results.append(metrics)
            self._save_learning_curve(
                model, X, Y,
                f"Spam score distribution by {name}",
                plot_file,
            )
            logger.info("Completed: %s — Accuracy: %.2f%%", name, metrics["accuracy"])

        # Comparison bar chart
        names = [r["name"] for r in results]
        metrics_keys = ["accuracy", "precision", "recall", "fscore"]
        x = np.arange(len(names))
        width = 0.2
        fig, ax = plt.subplots(figsize=(14, 7))
        for i, key in enumerate(metrics_keys):
            ax.bar(x + i * width, [r[key] for r in results], width, label=key.capitalize())
        ax.set_xticks(x + width * 1.5)
        ax.set_xticklabels(names, rotation=15, ha="right")
        ax.set_title("All Algorithms Comparison")
        ax.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(self.static_pimg, "Algcomp.jpg"))
        plt.close()

        return results

    def create_model(self) -> dict[str, Any]:
        try:
            from keras.layers import Dense
            from keras.models import Sequential
        except ImportError:
            raise RuntimeError(
                "TensorFlow/Keras not installed. Install with: pip install tensorflow"
            )

        logger.info("Starting model training")
        X, Y = self._preprocess(self.dataset_path)
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

        model = Sequential([
            Dense(4, input_shape=(10,), activation="relu"),
            Dense(4, activation="relu"),
            Dense(1, activation="sigmoid"),
        ])
        model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
        history = model.fit(
            X_train, y_train,
            validation_data=(X_test, y_test),
            epochs=200, verbose=0,
        )

        eval_result = model.evaluate(X_train, y_train, verbose=0)
        accuracy = float(eval_result[1]) * 100

        # Accuracy plot
        plt.figure()
        plt.plot(history.history["accuracy"], label="Train")
        plt.plot(history.history["val_accuracy"], label="Validation")
        plt.title("Model Accuracy")
        plt.ylabel("Accuracy")
        plt.xlabel("Epoch")
        plt.legend()
        plt.savefig(os.path.join(self.static_pimg, "macc.jpg"))
        plt.close()

        # Loss plot
        plt.figure()
        plt.plot(history.history["loss"], label="Train")
        plt.plot(history.history["val_loss"], label="Validation")
        plt.title("Model Loss")
        plt.ylabel("Loss")
        plt.xlabel("Epoch")
        plt.legend()
        plt.savefig(os.path.join(self.static_pimg, "mloss.jpg"))
        plt.close()

        model.save(self.model_path)
        self._model = model
        logger.info("Model saved: %s — Accuracy: %.2f%%", self.model_path, accuracy)
        return {"accuracy": round(accuracy, 2), "model_path": self.model_path}
