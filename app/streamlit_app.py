from __future__ import annotations

import ipaddress
import json
import socket
import sys
from pathlib import Path
from urllib.parse import urlparse, urlunparse

import joblib
import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.supabase_client import SupabaseClient
from src.explainability.explain import explain_linear_prediction
from src.features.text_preprocessing import basic_clean_text, highlight_suspicious_terms
from src.models.inference import RELIABLE_LABEL, UNRELIABLE_LABEL, predict_reliability
from src.utils.config import CFG, ensure_directories


MODEL_FILES = {
    "Best model": "baseline_best.joblib",
    "Logistic Regression": "baseline_lr.joblib",
    "Linear SVM": "baseline_svm.joblib",
    "Random Forest": "baseline_rf.joblib",
    "Naive Bayes": "baseline_nb.joblib",
}


def _build_allowed_public_url(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return None

    host = parsed.hostname
    if not host or host in {"localhost"}:
        return None

    if not CFG.allowed_news_domains:
        return None

    normalized_host = host.lower()
    if normalized_host not in CFG.allowed_news_domains:
        return None

    resolved_ips: set[ipaddress.IPv4Address | ipaddress.IPv6Address] = set()
    try:
        resolved_ips.add(ipaddress.ip_address(host))
    except ValueError:
        try:
            for item in socket.getaddrinfo(host, None):
                resolved_ips.add(ipaddress.ip_address(item[4][0]))
        except OSError:
            return None

    is_public = all(
        not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast)
        for ip in resolved_ips
    )
    if not is_public:
        return None

    safe_path = parsed.path or "/"
    return urlunparse((parsed.scheme, parsed.netloc, safe_path, "", parsed.query, ""))


def _extract_text_from_url(url: str) -> str:
    safe_url = _build_allowed_public_url(url)
    if safe_url is None:
        raise ValueError("URL không hợp lệ, không public, hoặc chưa nằm trong ALLOWED_NEWS_DOMAINS.")

    response = requests.get(
        safe_url,
        timeout=15,
        verify=True,
        allow_redirects=False,
        headers={"User-Agent": "NewsReliabilityAssessment/1.0"},
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.text.strip() if soup.title and soup.title.text else ""
    paragraphs = " ".join(p.get_text(" ", strip=True) for p in soup.find_all("p"))
    return basic_clean_text(f"{title}. {paragraphs}")


def _available_model_options() -> dict[str, Path]:
    options: dict[str, Path] = {}
    for label, filename in MODEL_FILES.items():
        path = CFG.models_artifacts_dir / filename
        if path.exists():
            options[label] = path
    return options


@st.cache_resource(show_spinner="Đang tải model...")
def _load_model(model_path: str):
    return joblib.load(model_path)


@st.cache_resource
def _supabase_client() -> SupabaseClient:
    return SupabaseClient()


def _load_metadata() -> dict:
    metadata_path = CFG.models_reports_dir / "model_metadata.json"
    if not metadata_path.exists():
        return {}
    return json.loads(metadata_path.read_text(encoding="utf-8"))


def _inject_style() -> None:
    st.markdown(
        """
        <style>
        .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
        .result-band {
            border-left: 6px solid #6b7280;
            padding: 0.85rem 1rem;
            background: #f8fafc;
            margin: 0.25rem 0 1rem 0;
        }
        .result-band.reliable { border-left-color: #15803d; }
        .result-band.unreliable { border-left-color: #b91c1c; }
        .article-preview {
            max-height: 360px;
            overflow: auto;
            line-height: 1.65;
            border: 1px solid #e5e7eb;
            padding: 1rem;
            background: #ffffff;
        }
        mark.suspicious-term {
            background: #fde68a;
            color: #111827;
            padding: 0.05rem 0.2rem;
            border-radius: 4px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _prediction_payload(result: dict, explanation: dict, input_type: str) -> dict:
    return {
        "client_prediction_id": result["id"],
        "input_type": input_type,
        "text": result["text"],
        "model_name": result["model_name"],
        "predicted_label": result["predicted_label"],
        "label_name": result["label_name"],
        "confidence": result["confidence"],
        "risk_score": result["risk_score"],
        "probabilities": result["probabilities"],
        "model_probabilities": result["model_probabilities"],
        "lexical_risk_score": result["lexical_risk_score"],
        "suspicious_terms": result["suspicious_terms"],
        "explanation": explanation["explanation_summary"],
    }


def _render_result(result: dict, explanation: dict) -> None:
    status_class = "unreliable" if result["predicted_label"] == UNRELIABLE_LABEL else "reliable"
    st.markdown(
        f"""
        <div class="result-band {status_class}">
            <strong>Kết luận:</strong> {result["label_vi"]}<br>
            <span>{result["label_description"]}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    stats = result["text_stats"]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Risk score", f"{result['risk_score']:.1%}")
    col2.metric("Confidence", f"{result['confidence']:.1%}")
    col3.metric("ML risk", f"{result['model_probabilities']['unreliable']:.1%}")
    col4.metric("Lexical risk", f"{result['lexical_risk_score']:.1%}")

    st.progress(result["risk_score"], text="Mức rủi ro tin giả/clickbait")
    chart_df = pd.DataFrame(
        [
            {"Nhãn": "Đáng tin", "Điểm": result["probabilities"]["reliable"]},
            {"Nhãn": "Nghi ngờ", "Điểm": result["probabilities"]["unreliable"]},
        ]
    ).set_index("Nhãn")
    st.bar_chart(chart_df, y="Điểm", height=240)

    left, right = st.columns([1.35, 1])
    with left:
        st.subheader("Văn bản đã highlight")
        preview_text = result["text"][:6000]
        if len(result["text"]) > len(preview_text):
            preview_text += " ..."
        st.markdown(
            f'<div class="article-preview">{highlight_suspicious_terms(preview_text)}</div>',
            unsafe_allow_html=True,
        )

    with right:
        st.subheader("Dấu hiệu đáng nghi")
        if result["suspicious_terms"]:
            st.dataframe(pd.DataFrame(result["suspicious_terms"]), use_container_width=True, hide_index=True)
        else:
            st.info("Không phát hiện từ khóa giật gân trong bộ luật hiện tại.")

        st.subheader("Thống kê nhanh")
        stats_df = pd.DataFrame([stats]).T.rename(columns={0: "Giá trị"})
        st.dataframe(stats_df, use_container_width=True)

    st.subheader("Giải thích từ mô hình")
    token_left, token_right = st.columns(2)
    with token_left:
        st.markdown("**Đẩy về nhóm nghi ngờ**")
        rows = explanation.get("top_unreliable_tokens") or []
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    with token_right:
        st.markdown("**Đẩy về nhóm đáng tin**")
        rows = explanation.get("top_reliable_tokens") or []
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    if not explanation.get("top_unreliable_tokens") and not explanation.get("top_reliable_tokens"):
        st.markdown("**Token TF-IDF nổi bật**")
        st.dataframe(pd.DataFrame(explanation.get("top_input_tokens", [])), use_container_width=True, hide_index=True)


def _render_feedback(client: SupabaseClient) -> None:
    result = st.session_state.get("last_prediction")
    if not result:
        return

    with st.form("feedback_form", clear_on_submit=True):
        vote = st.radio("Kết quả dự đoán này đúng không?", ["Đúng", "Sai", "Không chắc"], horizontal=True)
        comment = st.text_input("Ghi chú phản hồi")
        submitted = st.form_submit_button("Gửi feedback")
        if submitted:
            is_correct = None if vote == "Không chắc" else vote == "Đúng"
            client.insert_feedback(
                {
                    "prediction_client_id": result["id"],
                    "is_correct": is_correct,
                    "comment": comment,
                }
            )
            st.success("Đã lưu feedback.")


def _render_history(client: SupabaseClient) -> None:
    rows = client.list_predictions(limit=50)
    if not rows:
        st.info("Chưa có lịch sử phân tích.")
        return

    df = pd.DataFrame(rows)
    wanted = [
        "created_at",
        "input_type",
        "model_name",
        "label_name",
        "confidence",
        "risk_score",
        "lexical_risk_score",
        "text",
    ]
    visible = [col for col in wanted if col in df.columns]
    if "text" in df.columns:
        df["text"] = df["text"].astype(str).str.slice(0, 180)
    st.dataframe(df[visible], use_container_width=True, hide_index=True)


def main() -> None:
    ensure_directories()
    st.set_page_config(page_title="News Reliability Assessment", layout="wide")
    _inject_style()

    st.title("Machine Learning-based News Reliability Assessment")
    st.caption("Layered architecture: Streamlit UI, NLP/ML core, Supabase/PostgreSQL storage.")

    model_options = _available_model_options()
    if not model_options:
        st.error("Chưa có model artifact. Chạy `make data`, `make prepare`, rồi `make train` trước.")
        return

    metadata = _load_metadata()
    selected_model_label = st.sidebar.selectbox("Model", list(model_options.keys()))
    selected_model_path = model_options[selected_model_label]
    model = _load_model(str(selected_model_path))
    client = _supabase_client()

    st.sidebar.markdown("**Label convention**")
    st.sidebar.write("`0 = reliable/real`")
    st.sidebar.write("`1 = unreliable/fake/clickbait`")
    if metadata:
        st.sidebar.markdown("**Best model**")
        st.sidebar.write(metadata.get("best_model", "N/A"))

    analyze_tab, history_tab = st.tabs(["Phân tích", "Lịch sử"])

    with analyze_tab:
        input_mode = st.radio("Kiểu nhập liệu", ["Text", "URL"], horizontal=True)
        input_text = ""

        if input_mode == "Text":
            input_text = st.text_area("Nội dung tin tức", height=220, placeholder="Dán tiêu đề hoặc nội dung bài báo...")
        else:
            url = st.text_input("URL bài báo")
            if not CFG.allowed_news_domains:
                st.info("Thiết lập ALLOWED_NEWS_DOMAINS trong `.env` để bật kiểm tra URL.")
            if url:
                try:
                    input_text = _extract_text_from_url(url)
                    st.success("Đã trích xuất nội dung từ URL.")
                    st.text_area("Nội dung trích xuất", input_text, height=180)
                except Exception as exc:
                    st.error(f"Không thể đọc URL: {exc}")

        if st.button("Phân tích", type="primary", use_container_width=False):
            clean_text = basic_clean_text(input_text)
            if not clean_text:
                st.warning("Vui lòng nhập văn bản hoặc URL hợp lệ.")
            else:
                result = predict_reliability(clean_text, model, model_name=selected_model_label)
                explanation = explain_linear_prediction(clean_text, model=model, top_k=12)
                payload = _prediction_payload(result, explanation, input_mode.lower())
                client.insert_prediction(payload)
                st.session_state["last_prediction"] = result
                st.session_state["last_explanation"] = explanation
                st.success("Đã phân tích và lưu lịch sử.")

        result = st.session_state.get("last_prediction")
        explanation = st.session_state.get("last_explanation")
        if result and explanation:
            _render_result(result, explanation)
            _render_feedback(client)

    with history_tab:
        _render_history(client)


if __name__ == "__main__":
    main()
