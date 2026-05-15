from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np

from src.features.text_preprocessing import basic_clean_text, find_suspicious_terms
from src.models.inference import RELIABLE_LABEL, UNRELIABLE_LABEL, label_vi, predict_probabilities
from src.utils.config import CFG


def _load_pipeline(model: Any | None = None, model_path: Path | None = None) -> Any:
    if model is not None:
        return model
    model_path = model_path or (CFG.models_artifacts_dir / "baseline_best.joblib")
    return joblib.load(model_path)


def _class_index(classifier: Any, class_label: int) -> int | None:
    classes = getattr(classifier, "classes_", None)
    if classes is None:
        return None
    matches = np.where(np.asarray(classes).astype(int) == class_label)[0]
    return int(matches[0]) if len(matches) else None


def _signed_feature_weights(classifier: Any) -> np.ndarray | None:
    if hasattr(classifier, "coef_"):
        weights = np.asarray(classifier.coef_)
        if weights.ndim == 2:
            weights = weights[0]
        classes = getattr(classifier, "classes_", np.array([RELIABLE_LABEL, UNRELIABLE_LABEL]))
        if int(classes[-1]) != UNRELIABLE_LABEL:
            weights = -weights
        return weights

    if hasattr(classifier, "feature_log_prob_"):
        reliable_idx = _class_index(classifier, RELIABLE_LABEL)
        unreliable_idx = _class_index(classifier, UNRELIABLE_LABEL)
        if reliable_idx is None or unreliable_idx is None:
            return None
        return np.asarray(classifier.feature_log_prob_[unreliable_idx] - classifier.feature_log_prob_[reliable_idx])

    return None


def explain_linear_prediction(
    text: str,
    model_path: Path | None = None,
    top_k: int = 10,
    model: Any | None = None,
) -> dict:
    pipeline = _load_pipeline(model=model, model_path=model_path)

    clean_text = basic_clean_text(text)
    vectorizer = pipeline.named_steps["tfidf"]
    classifier = pipeline.named_steps["clf"]
    x = vectorizer.transform([clean_text])

    pred = int(pipeline.predict([clean_text])[0])
    probabilities = predict_probabilities(pipeline, [clean_text])[0]
    confidence = probabilities["unreliable"] if pred == UNRELIABLE_LABEL else probabilities["reliable"]

    feature_names = np.array(vectorizer.get_feature_names_out())
    tfidf_values = x.toarray()[0]
    weights = _signed_feature_weights(classifier)

    if weights is not None:
        contrib = tfidf_values * weights
        top_unreliable_idx = np.argsort(contrib)[-top_k:][::-1]
        top_reliable_idx = np.argsort(contrib)[:top_k]

        top_unreliable_tokens = [
            {"token": feature_names[i], "contribution": float(contrib[i])}
            for i in top_unreliable_idx
            if contrib[i] > 0
        ]
        top_reliable_tokens = [
            {"token": feature_names[i], "contribution": float(contrib[i])}
            for i in top_reliable_idx
            if contrib[i] < 0
        ]
    else:
        active_idx = np.argsort(tfidf_values)[-top_k:][::-1]
        top_unreliable_tokens = []
        top_reliable_tokens = []

    top_input_tokens = [
        {"token": feature_names[i], "tfidf": float(tfidf_values[i])}
        for i in np.argsort(tfidf_values)[-top_k:][::-1]
        if tfidf_values[i] > 0
    ]

    result = {
        "text": clean_text,
        "predicted_label": pred,
        "predicted_label_vi": label_vi(pred),
        "confidence": confidence,
        "probabilities": probabilities,
        "top_unreliable_tokens": top_unreliable_tokens,
        "top_reliable_tokens": top_reliable_tokens,
        "top_positive_tokens": top_unreliable_tokens,
        "top_negative_tokens": top_reliable_tokens,
        "top_input_tokens": top_input_tokens,
        "suspicious_terms": find_suspicious_terms(clean_text),
        "explanation_summary": (
            "Với quy ước 1 = tin nghi ngờ, trọng số dương đẩy dự đoán về nhóm unreliable; "
            "trọng số âm đẩy dự đoán về nhóm reliable. Với mô hình phi tuyến, bảng TF-IDF "
            "hiển thị các từ nổi bật trong văn bản để hỗ trợ phân tích."
        ),
    }
    return result


def save_explanation_json(text: str, output_file: Path | None = None) -> Path:
    output_file = output_file or (CFG.reports_dir / "explanations_sample.json")
    explanation = explain_linear_prediction(text)
    output_file.write_text(json.dumps(explanation, indent=2, ensure_ascii=False), encoding="utf-8")
    return output_file
