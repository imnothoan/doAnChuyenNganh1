from __future__ import annotations

import ipaddress
import json
import socket
import sys
from datetime import datetime
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
        raise ValueError("The URL is invalid, non-public, or not listed in ALLOWED_NEWS_DOMAINS.")

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


@st.cache_resource(show_spinner="Loading model...")
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


def _load_metrics() -> dict:
    metrics_path = CFG.reports_dir / "metrics_baseline.json"
    if not metrics_path.exists():
        return {}
    return json.loads(metrics_path.read_text(encoding="utf-8"))


def _inject_style() -> None:
    st.markdown(
        """
        <style>
        .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
        .result-band {
            border-left: 6px solid #6b7280;
            padding: 0.95rem 1rem;
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
        .small-note {
            color: #4b5563;
            font-size: 0.92rem;
            line-height: 1.45;
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


def _risk_band(score: float) -> tuple[str, str]:
    if score < 0.35:
        return "Low", "The text currently shows limited unreliable-news signals."
    if score < 0.65:
        return "Medium", "The text has mixed signals and should be reviewed carefully."
    return "High", "The text contains strong unreliable-news or clickbait-like signals."


def _source_signal(result: dict) -> str:
    ml_risk = float(result["model_probabilities"]["unreliable"])
    lexical_risk = float(result["lexical_risk_score"])
    if lexical_risk > ml_risk + 0.05:
        return "Main driver: suspicious wording and punctuation."
    if ml_risk > lexical_risk + 0.05:
        return "Main driver: TF-IDF text patterns learned by the model."
    return "Main driver: ML and lexical signals are similar."


def _format_suspicious_terms(rows: list[dict]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame(columns=["Term", "Category", "Count"])
    return pd.DataFrame(rows).rename(columns={"term": "Term", "category": "Category", "count": "Count"})


def _format_stats(stats: dict) -> pd.DataFrame:
    labels = {
        "characters": "Characters",
        "words": "Words",
        "sentences": "Sentences",
        "exclamation_marks": "Exclamation marks",
        "question_marks": "Question marks",
        "uppercase_ratio": "Uppercase ratio",
    }
    return pd.DataFrame(
        [{"Metric": labels.get(key, key), "Value": value} for key, value in stats.items()]
    )


def _format_token_rows(rows: list[dict], direction: str) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame(columns=["Token", "Contribution", "Interpretation"])
    interpretation = (
        "Higher positive value pushes the classifier toward unreliable."
        if direction == "unreliable"
        else "More negative value pushes the classifier toward reliable."
    )
    formatted = []
    for row in rows:
        formatted.append(
            {
                "Token": row.get("token", ""),
                "Contribution": f"{float(row.get('contribution', 0.0)):.4f}",
                "Interpretation": interpretation,
            }
        )
    return pd.DataFrame(formatted)


def _format_input_tokens(rows: list[dict]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame(columns=["Token", "TF-IDF"])
    return pd.DataFrame(
        [{"Token": row.get("token", ""), "TF-IDF": f"{float(row.get('tfidf', 0.0)):.4f}"} for row in rows]
    )


def _model_comparison_df(metrics: dict) -> pd.DataFrame:
    names = {
        "lr": "Logistic Regression",
        "svm": "Linear SVM",
        "rf": "Random Forest",
        "nb": "Multinomial Naive Bayes",
    }
    rows = []
    for key, item in metrics.items():
        validation = item.get("validation", {})
        test = item.get("test", {})
        rows.append(
            {
                "Model": names.get(key, key),
                "Validation F1 macro": validation.get("f1_macro"),
                "Test accuracy": test.get("accuracy"),
                "Test F1 macro": test.get("f1_macro"),
                "Test ROC-AUC": test.get("roc_auc"),
            }
        )
    return pd.DataFrame(rows)


def _build_case_report(result: dict, explanation: dict) -> str:
    band, band_description = _risk_band(float(result["risk_score"]))
    suspicious_terms = result.get("suspicious_terms") or []
    unreliable_tokens = explanation.get("top_unreliable_tokens") or []
    reliable_tokens = explanation.get("top_reliable_tokens") or []

    def token_lines(rows: list[dict]) -> str:
        if not rows:
            return "- None"
        return "\n".join(f"- {row.get('token')}: {float(row.get('contribution', 0.0)):.4f}" for row in rows[:8])

    def suspicious_lines(rows: list[dict]) -> str:
        if not rows:
            return "- None"
        return "\n".join(
            f"- {row.get('term')} ({row.get('category')}), count={row.get('count')}" for row in rows[:12]
        )

    return f"""# News Reliability Assessment Report

Generated at: {datetime.now().isoformat(timespec="seconds")}

## Assessment

- Final label: {result["label_name"].title()}
- Risk band: {band}
- Risk score: {result["risk_score"]:.4f}
- Confidence: {result["confidence"]:.4f}
- ML risk: {result["model_probabilities"]["unreliable"]:.4f}
- Lexical risk: {result["lexical_risk_score"]:.4f}
- Interpretation: {band_description} {_source_signal(result)}

## Suspicious Signals

{suspicious_lines(suspicious_terms)}

## Token Contributions

### Pushes Toward Unreliable

{token_lines(unreliable_tokens)}

### Pushes Toward Reliable

{token_lines(reliable_tokens)}

## Important Note

This report is a decision-support output. It highlights linguistic and model-based risk signals, but it does not replace professional fact-checking or external evidence verification.

## Input Text

{result["text"]}
"""


def _render_interpretation(result: dict) -> None:
    band, band_description = _risk_band(float(result["risk_score"]))
    label = result["label_name"].title()
    st.markdown(
        f"""
        <div class="result-band {result["label_name"]}">
            <strong>Assessment:</strong> {label}<br>
            <strong>Risk band:</strong> {band} ({result["risk_score"]:.1%})<br>
            <span>{band_description} {_source_signal(result)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Evidence breakdown", expanded=True):
        st.markdown(
            f"""
            - **Model signal:** `{result["model_probabilities"]["unreliable"]:.1%}` unreliable risk from TF-IDF text patterns.
            - **Lexical signal:** `{result["lexical_risk_score"]:.1%}` risk from suspicious terms and punctuation.
            - **Final score:** the system uses the stronger risk signal for screening, then shows the label above.
            """
        )

    with st.expander("Metric guide", expanded=False):
        st.markdown(
            """
            - **Risk score:** screening score for unreliable or clickbait-like content.
            - **Confidence:** score assigned to the displayed label.
            - **ML risk:** signal from the trained machine learning model.
            - **Lexical risk:** signal from suspicious terms and punctuation.
            - **Token contribution:** TF-IDF tokens that push the model toward reliable or unreliable.
            """
        )


def _render_result(result: dict, explanation: dict) -> None:
    _render_interpretation(result)

    stats = result["text_stats"]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Risk score", f"{result['risk_score']:.1%}")
    col2.metric("Confidence", f"{result['confidence']:.1%}")
    col3.metric("ML risk", f"{result['model_probabilities']['unreliable']:.1%}")
    col4.metric("Lexical risk", f"{result['lexical_risk_score']:.1%}")

    st.progress(result["risk_score"], text="Unreliable / clickbait risk level")
    chart_df = pd.DataFrame(
        [
            {"Class": "Reliable", "Score": result["probabilities"]["reliable"]},
            {"Class": "Unreliable", "Score": result["probabilities"]["unreliable"]},
        ]
    ).set_index("Class")
    st.bar_chart(chart_df, y="Score", height=240)

    left, right = st.columns([1.35, 1])
    with left:
        st.subheader("Highlighted input")
        preview_text = result["text"][:6000]
        if len(result["text"]) > len(preview_text):
            preview_text += " ..."
        st.markdown(
            f'<div class="article-preview">{highlight_suspicious_terms(preview_text)}</div>',
            unsafe_allow_html=True,
        )

    with right:
        st.subheader("Suspicious signals")
        if result["suspicious_terms"]:
            st.dataframe(_format_suspicious_terms(result["suspicious_terms"]), use_container_width=True, hide_index=True)
        else:
            st.info("No suspicious keywords were detected by the current rule set.")

        st.subheader("Text statistics")
        st.dataframe(_format_stats(stats), use_container_width=True, hide_index=True)

    st.subheader("Model explanation")
    token_left, token_right = st.columns(2)
    with token_left:
        st.markdown("**Pushes toward unreliable**")
        rows = explanation.get("top_unreliable_tokens") or []
        st.dataframe(_format_token_rows(rows, "unreliable"), use_container_width=True, hide_index=True)
    with token_right:
        st.markdown("**Pushes toward reliable**")
        rows = explanation.get("top_reliable_tokens") or []
        st.dataframe(_format_token_rows(rows, "reliable"), use_container_width=True, hide_index=True)

    if not explanation.get("top_unreliable_tokens") and not explanation.get("top_reliable_tokens"):
        st.markdown("**Prominent TF-IDF input tokens**")
        st.dataframe(_format_input_tokens(explanation.get("top_input_tokens", [])), use_container_width=True, hide_index=True)

    st.subheader("Case report")
    st.markdown(
        "Export a compact analysis report for defense, reviewer workflow, or later model-error review."
    )
    st.download_button(
        "Download analysis report",
        data=_build_case_report(result, explanation),
        file_name=f"news_reliability_report_{result['id']}.md",
        mime="text/markdown",
    )


def _render_feedback(client: SupabaseClient) -> None:
    result = st.session_state.get("last_prediction")
    if not result:
        return

    with st.form("feedback_form", clear_on_submit=True):
        vote = st.radio("Was this prediction correct?", ["Correct", "Incorrect", "Not sure"], horizontal=True)
        comment = st.text_input("Optional feedback note")
        submitted = st.form_submit_button("Submit feedback")
        if submitted:
            is_correct = None if vote == "Not sure" else vote == "Correct"
            client.insert_feedback(
                {
                    "prediction_client_id": result["id"],
                    "is_correct": is_correct,
                    "comment": comment,
                }
            )
            st.success("Feedback saved.")


def _render_history(client: SupabaseClient) -> None:
    rows = client.list_predictions(limit=50)
    if not rows:
        st.info("No analysis history yet.")
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
    display = df[visible].rename(
        columns={
            "created_at": "Created at",
            "input_type": "Input type",
            "model_name": "Model",
            "label_name": "Label",
            "confidence": "Confidence",
            "risk_score": "Risk score",
            "lexical_risk_score": "Lexical risk",
            "text": "Text preview",
        }
    )
    st.dataframe(display, use_container_width=True, hide_index=True)


def _render_dashboard(client: SupabaseClient, metadata: dict) -> None:
    st.subheader("Project Dashboard")
    st.markdown(
        "This dashboard is used during defense to show that the project includes model evaluation, "
        "workflow coverage, review history, and benchmark-inspired design decisions."
    )

    final_metrics = metadata.get("best_model_test_after_refit", {}) if metadata else {}
    dataset_sizes = metadata.get("dataset_sizes", {}) if metadata else {}
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Best model", str(metadata.get("best_model", "N/A")).upper() if metadata else "N/A")
    col2.metric("Final accuracy", f"{final_metrics.get('accuracy', 0):.4f}")
    col3.metric("Final F1 macro", f"{final_metrics.get('f1_macro', 0):.4f}")
    col4.metric("Test samples", str(dataset_sizes.get("test", "N/A")))

    st.subheader("Dataset and training evidence")
    st.dataframe(
        pd.DataFrame(
            [
                {"Item": "Source dataset", "Evidence": "VFND Vietnamese fake news dataset plus normalized local splits"},
                {"Item": "Label convention", "Evidence": "0 = reliable/real, 1 = unreliable/fake/clickbait"},
                {"Item": "Train/validation/test", "Evidence": "350 / 75 / 75 samples after cleaning and deduplication"},
                {"Item": "Feature extraction", "Evidence": "TF-IDF vectors from cleaned Vietnamese news text"},
                {"Item": "Training scripts", "Evidence": "download_data.py -> prepare_data.py -> train_baseline.py"},
                {"Item": "Selection rule", "Evidence": "Best model selected by validation F1 macro, then refit before final test"},
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )

    metrics = _load_metrics()
    comparison = _model_comparison_df(metrics)
    if not comparison.empty:
        st.subheader("Model benchmark")
        st.dataframe(comparison, use_container_width=True, hide_index=True)
        chart = comparison.set_index("Model")[["Test F1 macro", "Test ROC-AUC"]]
        st.bar_chart(chart, height=260)

    st.subheader("Workflow coverage")
    st.dataframe(
        pd.DataFrame(
            [
                {"Module": "Article input", "Implemented evidence": "Text mode, URL mode, prepared article cases"},
                {"Module": "NLP/ML inference", "Implemented evidence": "TF-IDF pipeline, four baseline models, best-model artifact"},
                {"Module": "Visual explanation", "Implemented evidence": "Risk band, ML risk, lexical risk, token contribution"},
                {"Module": "Review workflow", "Implemented evidence": "History tab, Supabase storage, feedback form"},
                {"Module": "Export/report", "Implemented evidence": "Downloadable per-case markdown report"},
                {"Module": "Evaluation", "Implemented evidence": "Accuracy, F1 macro, ROC-AUC, confusion matrices"},
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Benchmark-inspired design")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Reference pattern": "Fact-checking tools such as Full Fact AI",
                    "Relevant idea": "Use AI to prioritize and explain suspicious claims",
                    "Project implementation": "ML risk, lexical risk, token-level explanation",
                },
                {
                    "Reference pattern": "NewsGuard-style credibility labels",
                    "Relevant idea": "Show a visible rating plus supporting criteria",
                    "Project implementation": "Assessment Summary, risk band, explanation panels",
                },
                {
                    "Reference pattern": "Reviewer-oriented fact-checking workflow",
                    "Relevant idea": "Keep history and feedback for later review",
                    "Project implementation": "Supabase prediction history and feedback loop",
                },
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Confusion matrix")
    figure_map = {
        "Logistic Regression": CFG.reports_figures_dir / "confusion_matrix_lr.png",
        "Linear SVM": CFG.reports_figures_dir / "confusion_matrix_svm.png",
        "Random Forest": CFG.reports_figures_dir / "confusion_matrix_rf.png",
        "Multinomial Naive Bayes": CFG.reports_figures_dir / "confusion_matrix_nb.png",
    }
    selected_figure = st.selectbox("Model confusion matrix", list(figure_map.keys()))
    figure_path = figure_map[selected_figure]
    if figure_path.exists():
        st.image(str(figure_path), caption=f"{selected_figure} confusion matrix")

    rows = client.list_predictions(limit=200)
    if rows:
        history = pd.DataFrame(rows)
        st.subheader("Reviewer history summary")
        h1, h2, h3 = st.columns(3)
        h1.metric("Stored predictions", len(history))
        if "risk_score" in history.columns:
            h2.metric("Average risk", f"{pd.to_numeric(history['risk_score'], errors='coerce').mean():.2%}")
        if "label_name" in history.columns:
            unreliable_rate = (history["label_name"].astype(str) == "unreliable").mean()
            h3.metric("Unreliable share", f"{unreliable_rate:.2%}")
    else:
        st.info("No stored predictions yet. Analyze a prepared article case and submit feedback to populate reviewer history.")


def main() -> None:
    ensure_directories()
    st.set_page_config(page_title="News Reliability Assessment", layout="wide")
    _inject_style()

    st.title("Machine Learning-based News Reliability Assessment")
    st.caption("Vietnamese news reliability screening with NLP/ML inference, explanation, history, and feedback.")

    model_options = _available_model_options()
    if not model_options:
        st.error(
            "No model artifact was found. Run `python3 scripts/download_data.py`, "
            "`python3 scripts/prepare_data.py`, and `python3 scripts/train_baseline.py` first."
        )
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
        final_metrics = metadata.get("best_model_test_after_refit", {})
        if final_metrics:
            st.sidebar.markdown("**Final test metrics**")
            st.sidebar.write(f"Accuracy: `{final_metrics.get('accuracy', 0):.4f}`")
            st.sidebar.write(f"F1 macro: `{final_metrics.get('f1_macro', 0):.4f}`")

    analyze_tab, dashboard_tab, history_tab = st.tabs(["Analyze", "Dashboard", "History"])

    with analyze_tab:
        st.subheader("Input")
        input_mode = st.radio("Input mode", ["Text", "URL"], horizontal=True)
        input_text = ""

        if input_mode == "Text":
            st.caption(
                "Paste Vietnamese news text for reliability assessment."
            )
            input_text = st.text_area(
                "Vietnamese news content",
                height=230,
                placeholder="Paste a Vietnamese headline or article content here...",
                key="news_text_input",
            )
        else:
            st.info(
                "Paste a public article URL from an allowed news domain. The extracted content will be displayed "
                "before analysis."
            )
            url = st.text_input("Article URL")
            if not CFG.allowed_news_domains:
                st.info("Set ALLOWED_NEWS_DOMAINS in `.env` to enable URL analysis.")
            if url:
                try:
                    input_text = _extract_text_from_url(url)
                    st.success("Article text extracted.")
                    st.text_area("Extracted content", input_text, height=180)
                except Exception as exc:
                    st.error(f"Could not read the URL: {exc}")

        if st.button("Analyze", type="primary", use_container_width=False):
            clean_text = basic_clean_text(input_text)
            if not clean_text:
                st.warning("Please provide valid text or a valid URL before analysis.")
            else:
                result = predict_reliability(clean_text, model, model_name=selected_model_label)
                explanation = explain_linear_prediction(clean_text, model=model, top_k=12)
                payload = _prediction_payload(result, explanation, input_mode.lower())
                client.insert_prediction(payload)
                st.session_state["last_prediction"] = result
                st.session_state["last_explanation"] = explanation
                st.success("Analysis completed and saved to history.")

        result = st.session_state.get("last_prediction")
        explanation = st.session_state.get("last_explanation")
        if result and explanation:
            _render_result(result, explanation)
            _render_feedback(client)

    with dashboard_tab:
        _render_dashboard(client, metadata)

    with history_tab:
        _render_history(client)


if __name__ == "__main__":
    main()
