from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np

from src.features.text_preprocessing import basic_clean_text
from src.utils.config import CFG


def explain_linear_prediction(text: str, model_path: Path | None = None, top_k: int = 10) -> dict:
    model_path = model_path or (CFG.models_artifacts_dir / "baseline_lr.joblib")
    pipeline = joblib.load(model_path)

    clean_text = basic_clean_text(text)
    vectorizer = pipeline.named_steps["tfidf"]
    classifier = pipeline.named_steps["clf"]
    x = vectorizer.transform([clean_text])

    if hasattr(classifier, "predict_proba"):
        proba = classifier.predict_proba(x)[0]
        confidence = float(np.max(proba))
    else:
        decision = classifier.decision_function(x)[0]
        confidence = float(1 / (1 + np.exp(-decision)))

    pred = int(pipeline.predict([clean_text])[0])

    feature_names = np.array(vectorizer.get_feature_names_out())
    coefs = classifier.coef_[0]
    contrib = x.toarray()[0] * coefs

    top_positive_idx = np.argsort(contrib)[-top_k:][::-1]
    top_negative_idx = np.argsort(contrib)[:top_k]

    result = {
        "text": clean_text,
        "predicted_label": pred,
        "confidence": confidence,
        "top_positive_tokens": [
            {"token": feature_names[i], "contribution": float(contrib[i])}
            for i in top_positive_idx
            if contrib[i] > 0
        ],
        "top_negative_tokens": [
            {"token": feature_names[i], "contribution": float(contrib[i])}
            for i in top_negative_idx
            if contrib[i] < 0
        ],
        "explanation_summary": "Các từ có trọng số dương đẩy dự đoán về reliable, trọng số âm đẩy về unreliable.",
    }
    return result


def save_explanation_json(text: str, output_file: Path | None = None) -> Path:
    output_file = output_file or (CFG.reports_dir / "explanations_sample.json")
    explanation = explain_linear_prediction(text)
    output_file.write_text(json.dumps(explanation, indent=2, ensure_ascii=False), encoding="utf-8")
    return output_file
