from __future__ import annotations

from hashlib import sha256
from typing import Any

import numpy as np

from src.features.text_preprocessing import (
    basic_clean_text,
    find_suspicious_terms,
    text_statistics,
)

RELIABLE_LABEL = 0
UNRELIABLE_LABEL = 1

LABEL_DISPLAY = {
    RELIABLE_LABEL: {
        "name": "reliable",
        "vi": "Reliable",
        "description": "The content is closer to reliable news patterns learned by the model.",
    },
    UNRELIABLE_LABEL: {
        "name": "unreliable",
        "vi": "Unreliable",
        "description": "The content contains patterns associated with fake news, clickbait, or low reliability.",
    },
}


def label_name(label: int) -> str:
    return LABEL_DISPLAY.get(int(label), LABEL_DISPLAY[UNRELIABLE_LABEL])["name"]


def label_vi(label: int) -> str:
    return LABEL_DISPLAY.get(int(label), LABEL_DISPLAY[UNRELIABLE_LABEL])["vi"]


def _sigmoid(value: np.ndarray | float) -> np.ndarray | float:
    clipped = np.clip(value, -50, 50)
    return 1.0 / (1.0 + np.exp(-clipped))


def _classes_from_model(model: Any) -> list[int]:
    classes = getattr(model, "classes_", None)
    if classes is None and hasattr(model, "named_steps"):
        clf = model.named_steps.get("clf")
        classes = getattr(clf, "classes_", None)
    if classes is None:
        return [RELIABLE_LABEL, UNRELIABLE_LABEL]
    return [int(item) for item in classes]


def predict_probabilities(model: Any, texts: list[str]) -> list[dict[str, float]]:
    classes = _classes_from_model(model)
    outputs: list[dict[str, float]] = []

    if hasattr(model, "predict_proba"):
        raw = model.predict_proba(texts)
        for row in raw:
            by_label = {label_name(label): float(prob) for label, prob in zip(classes, row)}
            outputs.append(
                {
                    "reliable": float(np.clip(by_label.get("reliable", 0.0), 0.0, 1.0)),
                    "unreliable": float(np.clip(by_label.get("unreliable", 0.0), 0.0, 1.0)),
                }
            )
        return outputs

    if hasattr(model, "decision_function"):
        raw_scores = np.asarray(model.decision_function(texts))
        if raw_scores.ndim == 1:
            positive_label = classes[-1] if classes else UNRELIABLE_LABEL
            positive_probs = np.asarray(_sigmoid(raw_scores), dtype=float)
            for positive_prob in positive_probs:
                if positive_label == UNRELIABLE_LABEL:
                    unreliable = float(positive_prob)
                else:
                    unreliable = float(1.0 - positive_prob)
                outputs.append({"reliable": 1.0 - unreliable, "unreliable": unreliable})
            return outputs

    predictions = model.predict(texts)
    for pred in predictions:
        unreliable = 1.0 if int(pred) == UNRELIABLE_LABEL else 0.0
        outputs.append({"reliable": 1.0 - unreliable, "unreliable": unreliable})
    return outputs


def lexical_risk_score(suspicious_terms: list[dict[str, str | int]], stats: dict[str, int | float]) -> float:
    weights = {
        "credibility": 0.22,
        "clickbait": 0.16,
        "emotion": 0.12,
    }
    score = 0.0
    for item in suspicious_terms:
        category = str(item.get("category", ""))
        count = int(item.get("count", 1))
        score += weights.get(category, 0.08) * min(count, 3)

    score += min(int(stats.get("exclamation_marks", 0)) * 0.04, 0.12)
    score += min(int(stats.get("question_marks", 0)) * 0.025, 0.075)
    score += min(float(stats.get("uppercase_ratio", 0.0)) * 0.35, 0.1)
    return float(np.clip(score, 0.0, 0.95))


def predict_reliability(text: str, model: Any, model_name: str = "") -> dict[str, Any]:
    clean_text = basic_clean_text(text)
    if not clean_text:
        raise ValueError("Input text is empty after cleaning.")

    model_predicted_label = int(model.predict([clean_text])[0])
    model_probabilities = predict_probabilities(model, [clean_text])[0]
    suspicious_terms = find_suspicious_terms(clean_text)
    stats = text_statistics(clean_text)
    lexical_risk = lexical_risk_score(suspicious_terms, stats)
    risk_score = max(model_probabilities["unreliable"], lexical_risk)
    probabilities = {"reliable": 1.0 - risk_score, "unreliable": risk_score}
    predicted_label = UNRELIABLE_LABEL if risk_score >= 0.5 else RELIABLE_LABEL
    confidence = probabilities[label_name(predicted_label)]
    record_id = sha256(f"{clean_text}::{predicted_label}::{confidence:.6f}".encode("utf-8")).hexdigest()[:16]

    return {
        "id": record_id,
        "text": clean_text,
        "model_name": model_name,
        "predicted_label": predicted_label,
        "model_predicted_label": model_predicted_label,
        "label_name": label_name(predicted_label),
        "label_vi": label_vi(predicted_label),
        "label_description": LABEL_DISPLAY[predicted_label]["description"],
        "confidence": float(np.clip(confidence, 0.0, 1.0)),
        "risk_score": float(np.clip(risk_score, 0.0, 1.0)),
        "probabilities": probabilities,
        "model_probabilities": model_probabilities,
        "lexical_risk_score": lexical_risk,
        "suspicious_terms": suspicious_terms,
        "text_stats": stats,
    }
