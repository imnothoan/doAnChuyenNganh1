from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from src.utils.config import CFG, ensure_directories

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class MetricResult:
    accuracy: float
    precision_macro: float
    recall_macro: float
    f1_macro: float
    precision_weighted: float
    recall_weighted: float
    f1_weighted: float
    roc_auc: float | None


def format_prediction_output(label: int, confidence: float, probabilities: np.ndarray) -> dict:
    probs = np.asarray(probabilities).flatten()
    if probs.shape[0] == 1:
        probs = np.array([1 - probs[0], probs[0]])
    return {
        "predicted_label": int(label),
        "confidence": float(np.clip(confidence, 0.0, 1.0)),
        "probabilities": {
            "unreliable": float(np.clip(probs[0], 0.0, 1.0)),
            "reliable": float(np.clip(probs[1], 0.0, 1.0)),
        },
    }


def _load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train = pd.read_csv(CFG.data_processed_dir / "train.csv")
    val = pd.read_csv(CFG.data_processed_dir / "val.csv")
    test = pd.read_csv(CFG.data_processed_dir / "test.csv")
    return train, val, test


def _compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_score: np.ndarray | None = None) -> MetricResult:
    roc_auc = None
    if y_score is not None and len(np.unique(y_true)) == 2:
        try:
            roc_auc = float(roc_auc_score(y_true, y_score))
        except Exception:
            roc_auc = None

    return MetricResult(
        accuracy=float(accuracy_score(y_true, y_pred)),
        precision_macro=float(precision_score(y_true, y_pred, average="macro", zero_division=0)),
        recall_macro=float(recall_score(y_true, y_pred, average="macro", zero_division=0)),
        f1_macro=float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        precision_weighted=float(precision_score(y_true, y_pred, average="weighted", zero_division=0)),
        recall_weighted=float(recall_score(y_true, y_pred, average="weighted", zero_division=0)),
        f1_weighted=float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
        roc_auc=roc_auc,
    )


def _save_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, name: str) -> None:
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(cm, cmap="Blues")
    ax.set_title(f"Confusion Matrix - {name}")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    for (i, j), value in np.ndenumerate(cm):
        ax.text(j, i, str(value), ha="center", va="center")
    fig.tight_layout()
    fig.savefig(CFG.reports_figures_dir / f"confusion_matrix_{name}.png", dpi=150)
    plt.close(fig)


def _build_models() -> dict[str, Pipeline]:
    return {
        "lr": Pipeline(
            [
                ("tfidf", TfidfVectorizer(max_features=30000, ngram_range=(1, 2))),
                ("clf", LogisticRegression(max_iter=200, random_state=CFG.random_state)),
            ]
        ),
        "svm": Pipeline(
            [
                ("tfidf", TfidfVectorizer(max_features=30000, ngram_range=(1, 2))),
                ("clf", LinearSVC()),
            ]
        ),
        "nb": Pipeline(
            [
                ("tfidf", TfidfVectorizer(max_features=30000, ngram_range=(1, 2))),
                ("clf", MultinomialNB()),
            ]
        ),
    }


def train_baseline_models() -> dict[str, dict]:
    ensure_directories()
    train_df, val_df, test_df = _load_data()

    x_train = train_df["text"].fillna("")
    y_train = train_df["label"].astype(int).to_numpy()
    x_test = test_df["text"].fillna("")
    y_test = test_df["label"].astype(int).to_numpy()

    models = _build_models()
    all_metrics: dict[str, dict] = {}

    for name, model in models.items():
        logger.info("Training %s model", name)
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)

        y_score = None
        if hasattr(model, "predict_proba"):
            y_score = model.predict_proba(x_test)[:, 1]
        elif hasattr(model, "decision_function"):
            decision = model.decision_function(x_test)
            y_score = 1.0 / (1.0 + np.exp(-decision))

        metrics = _compute_metrics(y_test, y_pred, y_score)
        all_metrics[name] = asdict(metrics)
        _save_confusion_matrix(y_test, y_pred, name)

        if name == "lr":
            joblib.dump(model, CFG.models_artifacts_dir / "baseline_lr.joblib")
        if name == "svm":
            joblib.dump(model, CFG.models_artifacts_dir / "baseline_svm.joblib")

    (CFG.reports_dir / "metrics_baseline.json").write_text(
        json.dumps(all_metrics, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = ["# Model Comparison", "", "| Model | Accuracy | F1 Macro | F1 Weighted | ROC-AUC |", "|---|---:|---:|---:|---:|"]
    for name, metric in all_metrics.items():
        lines.append(
            f"| {name} | {metric['accuracy']:.4f} | {metric['f1_macro']:.4f} | {metric['f1_weighted']:.4f} | {metric['roc_auc'] if metric['roc_auc'] is not None else 'N/A'} |"
        )
    (CFG.reports_dir / "model_comparison.md").write_text("\n".join(lines), encoding="utf-8")

    return all_metrics


if __name__ == "__main__":
    train_baseline_models()
