from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
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

from src.features.text_preprocessing import preprocess_for_ml
from src.models.inference import RELIABLE_LABEL, UNRELIABLE_LABEL, label_name, predict_probabilities
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


def format_prediction_output(
    label: int,
    confidence: float,
    probabilities: np.ndarray,
    class_order: list[int] | np.ndarray | None = None,
) -> dict:
    probs = np.asarray(probabilities).flatten()
    if class_order is None:
        class_order = [RELIABLE_LABEL, UNRELIABLE_LABEL] if probs.shape[0] == 2 else [int(label)]

    probability_map = {"reliable": 0.0, "unreliable": 0.0}
    if probs.shape[0] == 1:
        probability_map[label_name(label)] = float(probs[0])
        other_name = "reliable" if label_name(label) == "unreliable" else "unreliable"
        probability_map[other_name] = float(1.0 - probs[0])
    else:
        for class_label, prob in zip(class_order, probs):
            probability_map[label_name(int(class_label))] = float(prob)

    normalized_confidence = probability_map.get(label_name(label), confidence)
    return {
        "predicted_label": int(label),
        "label_name": label_name(int(label)),
        "confidence": float(np.clip(normalized_confidence, 0.0, 1.0)),
        "probabilities": {
            "reliable": float(np.clip(probability_map["reliable"], 0.0, 1.0)),
            "unreliable": float(np.clip(probability_map["unreliable"], 0.0, 1.0)),
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
    cm = confusion_matrix(y_true, y_pred, labels=[RELIABLE_LABEL, UNRELIABLE_LABEL])
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(cm, cmap="Blues")
    ax.set_title(f"Confusion Matrix - {name}")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_xticks([0, 1], ["Reliable", "Unreliable"], rotation=30, ha="right")
    ax.set_yticks([0, 1], ["Reliable", "Unreliable"])
    for (i, j), value in np.ndenumerate(cm):
        ax.text(j, i, str(value), ha="center", va="center")
    fig.tight_layout()
    fig.savefig(CFG.reports_figures_dir / f"confusion_matrix_{name}.png", dpi=150)
    plt.close(fig)


def _tfidf_vectorizer() -> TfidfVectorizer:
    return TfidfVectorizer(
        max_features=50000,
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.95,
        sublinear_tf=True,
        lowercase=False,
        preprocessor=preprocess_for_ml,
        token_pattern=r"(?u)\b\w+\b",
    )


def _build_models() -> dict[str, Pipeline]:
    return {
        "lr": Pipeline(
            [
                ("tfidf", _tfidf_vectorizer()),
                ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=CFG.random_state)),
            ]
        ),
        "svm": Pipeline(
            [
                ("tfidf", _tfidf_vectorizer()),
                ("clf", LinearSVC(class_weight="balanced", random_state=CFG.random_state)),
            ]
        ),
        "rf": Pipeline(
            [
                ("tfidf", _tfidf_vectorizer()),
                (
                    "clf",
                    RandomForestClassifier(
                        n_estimators=300,
                        class_weight="balanced_subsample",
                        random_state=CFG.random_state,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
        "nb": Pipeline(
            [
                ("tfidf", _tfidf_vectorizer()),
                ("clf", MultinomialNB(alpha=0.5)),
            ]
        ),
    }


def _unreliable_scores(model: Pipeline, x_values: pd.Series) -> np.ndarray:
    probability_rows = predict_probabilities(model, x_values.fillna("").astype(str).tolist())
    return np.array([item["unreliable"] for item in probability_rows], dtype=float)


def _evaluate_model(model: Pipeline, x_values: pd.Series, y_true: np.ndarray) -> MetricResult:
    y_pred = model.predict(x_values.fillna(""))
    y_score = _unreliable_scores(model, x_values)
    return _compute_metrics(y_true, y_pred, y_score)


def train_baseline_models() -> dict[str, dict]:
    ensure_directories()
    train_df, val_df, test_df = _load_data()

    x_train = train_df["text"].fillna("")
    y_train = train_df["label"].astype(int).to_numpy()
    x_val = val_df["text"].fillna("")
    y_val = val_df["label"].astype(int).to_numpy()
    x_test = test_df["text"].fillna("")
    y_test = test_df["label"].astype(int).to_numpy()

    models = _build_models()
    all_metrics: dict[str, dict] = {}
    fitted_models: dict[str, Pipeline] = {}

    for name, model in models.items():
        logger.info("Training %s model", name)
        model.fit(x_train, y_train)
        fitted_models[name] = model

        val_metrics = _evaluate_model(model, x_val, y_val)
        test_metrics = _evaluate_model(model, x_test, y_test)
        all_metrics[name] = {
            "validation": asdict(val_metrics),
            "test": asdict(test_metrics),
        }
        _save_confusion_matrix(y_test, model.predict(x_test), name)
        joblib.dump(model, CFG.models_artifacts_dir / f"baseline_{name}.joblib")

    best_model_name = max(
        all_metrics,
        key=lambda item: (
            all_metrics[item]["validation"]["f1_macro"],
            all_metrics[item]["validation"]["accuracy"],
        ),
    )
    best_model = clone(models[best_model_name])
    x_train_val = pd.concat([x_train, x_val], ignore_index=True)
    y_train_val = np.concatenate([y_train, y_val])
    best_model.fit(x_train_val, y_train_val)
    best_test_metrics = _evaluate_model(best_model, x_test, y_test)
    joblib.dump(best_model, CFG.models_artifacts_dir / "baseline_best.joblib")

    (CFG.reports_dir / "metrics_baseline.json").write_text(
        json.dumps(all_metrics, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    metadata = {
        "best_model": best_model_name,
        "trained_with": {
            "python": ".".join(map(str, __import__("sys").version_info[:3])),
            "scikit_learn": sklearn.__version__,
        },
        "label_convention": {
            "0": "reliable/real",
            "1": "unreliable/fake/clickbait",
        },
        "class_order": [RELIABLE_LABEL, UNRELIABLE_LABEL],
        "dataset_sizes": {
            "train": len(train_df),
            "validation": len(val_df),
            "test": len(test_df),
        },
        "best_model_test_after_refit": asdict(best_test_metrics),
    }
    (CFG.models_reports_dir / "model_metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        "# Model Comparison",
        "",
        f"Best model selected by validation F1 macro: **{best_model_name}**.",
        "",
        "Label convention: `0 = reliable/real`, `1 = unreliable/fake/clickbait`.",
        "",
        "| Model | Val Acc | Val F1 Macro | Test Acc | Test F1 Macro | Test ROC-AUC |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, metric in all_metrics.items():
        val_metric = metric["validation"]
        test_metric = metric["test"]
        roc_auc = test_metric["roc_auc"] if test_metric["roc_auc"] is not None else "N/A"
        lines.append(
            f"| {name} | {val_metric['accuracy']:.4f} | {val_metric['f1_macro']:.4f} | {test_metric['accuracy']:.4f} | {test_metric['f1_macro']:.4f} | {roc_auc if isinstance(roc_auc, str) else f'{roc_auc:.4f}'} |"
        )
    (CFG.reports_dir / "model_comparison.md").write_text("\n".join(lines), encoding="utf-8")

    return {"metrics": all_metrics, "metadata": metadata}


if __name__ == "__main__":
    train_baseline_models()
