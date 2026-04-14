from __future__ import annotations

from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup

from src.explainability.explain import explain_linear_prediction
from src.features.text_preprocessing import basic_clean_text
from src.models.train_baseline import format_prediction_output
from src.utils.config import CFG, ensure_directories


def _extract_text_from_url(url: str) -> str:
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.text.strip() if soup.title and soup.title.text else ""
    paragraphs = " ".join(p.get_text(" ", strip=True) for p in soup.find_all("p"))
    return basic_clean_text(f"{title}. {paragraphs}")


def _load_model(model_path: Path):
    return joblib.load(model_path)


def _save_history(record: dict) -> None:
    history_file = CFG.data_processed_dir / "prediction_history.csv"
    ensure_directories()
    if history_file.exists():
        df = pd.read_csv(history_file)
    else:
        df = pd.DataFrame(columns=["timestamp", "input_type", "text", "predicted_label", "confidence", "explanation"])
    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    df.to_csv(history_file, index=False, encoding="utf-8")


def main() -> None:
    st.set_page_config(page_title="Vietnamese News Reliability", layout="wide")
    st.title("📰 Vietnamese News Reliability Evaluator")

    model_path = CFG.models_artifacts_dir / "baseline_lr.joblib"
    if not model_path.exists():
        st.error("Chưa có model baseline. Hãy chạy: make train")
        return

    model = _load_model(model_path)
    input_mode = st.radio("Chọn kiểu nhập", ["Text", "URL"], horizontal=True)

    text_input = ""
    if input_mode == "Text":
        text_input = st.text_area("Nhập nội dung tin tức", height=180)
    else:
        url = st.text_input("Nhập URL bài báo")
        if url:
            try:
                text_input = _extract_text_from_url(url)
                st.success("Đã trích xuất nội dung từ URL.")
            except Exception as exc:
                st.error(f"Không thể đọc URL: {exc}")

    if st.button("Dự đoán", type="primary"):
        clean = basic_clean_text(text_input)
        if not clean:
            st.warning("Vui lòng nhập văn bản hoặc URL hợp lệ.")
            return

        pred = int(model.predict([clean])[0])
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba([clean])[0]
            confidence = float(max(probs))
        else:
            decision = model.decision_function([clean])[0]
            confidence = float(1 / (1 + pow(2.718281828, -decision)))
            probs = [1 - confidence, confidence]

        formatted = format_prediction_output(pred, confidence, probs)
        label_text = "Reliable (Tin đáng tin)" if pred == 1 else "Unreliable (Tin nghi ngờ)"

        st.subheader("Kết quả")
        st.write(f"**Nhãn dự đoán:** {label_text}")
        st.write(f"**Độ tin cậy:** {formatted['confidence']:.4f}")

        explanation = explain_linear_prediction(clean, model_path=model_path, top_k=8)
        st.subheader("Giải thích")
        st.write(explanation["explanation_summary"])

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Từ khóa nghiêng về reliable**")
            st.json(explanation["top_positive_tokens"])
        with col2:
            st.markdown("**Từ khóa nghiêng về unreliable**")
            st.json(explanation["top_negative_tokens"])

        _save_history(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "input_type": input_mode.lower(),
                "text": clean,
                "predicted_label": pred,
                "confidence": formatted["confidence"],
                "explanation": explanation["explanation_summary"],
            }
        )
        st.success("Đã lưu lịch sử dự đoán vào data/processed/prediction_history.csv")


if __name__ == "__main__":
    main()
