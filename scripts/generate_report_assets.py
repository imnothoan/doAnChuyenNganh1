from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reports" / "figures"
INK = "#111111"
MID = "#555555"
LIGHT = "#F2F2F2"
WHITE = "#FFFFFF"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "text.color": INK,
        "axes.edgecolor": INK,
        "figure.facecolor": WHITE,
    }
)


def _setup(width: float = 12, height: float = 7):
    fig, ax = plt.subplots(figsize=(width, height), dpi=180)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax


def _save(fig, name: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_DIR / name, bbox_inches="tight", facecolor=WHITE, pad_inches=0.18)
    plt.close(fig)


def _box(ax, xy, w, h, text, fc=WHITE, ec=INK, fontsize=9, lw=1.5):
    patch = Rectangle(xy, w, h, linewidth=lw, edgecolor=INK, facecolor=WHITE)
    ax.add_patch(patch)
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center", fontsize=fontsize, wrap=True, color=INK)
    return patch


def _ellipse(ax, xy, w, h, text, fc=WHITE, ec=INK, fontsize=8):
    patch = Ellipse((xy[0] + w / 2, xy[1] + h / 2), w, h, linewidth=1.4, edgecolor=INK, facecolor=WHITE)
    ax.add_patch(patch)
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center", fontsize=fontsize, wrap=True, color=INK)
    return patch


def _arrow(ax, start, end, text: str = "", color=INK, rad=0.0, fontsize=8):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=12,
        linewidth=1.3,
        color=INK,
        connectionstyle=f"arc3,rad={rad}",
    )
    ax.add_patch(arrow)
    if text:
        ax.text((start[0] + end[0]) / 2, (start[1] + end[1]) / 2 + 2, text, ha="center", fontsize=fontsize, color=INK)


def _line(ax, start, end, lw: float = 1.3) -> None:
    ax.plot([start[0], end[0]], [start[1], end[1]], color=INK, lw=lw)


def architecture_diagram() -> None:
    fig, ax = _setup()
    ax.text(50, 96, "Layered Architecture", ha="center", fontsize=15, fontweight="bold")
    _box(ax, (8, 76), 84, 13, "Presentation Layer\nStreamlit UI: input, dashboard, history, feedback", "#dbeafe", "#1d4ed8", 10)
    _box(ax, (8, 54), 84, 15, "Core Engine Layer\nNLP preprocessing, TF-IDF vectorization, ML inference, risk scoring, explainability", "#dcfce7", "#15803d", 10)
    _box(ax, (8, 31), 40, 15, "Model Artifacts\nbaseline_best.joblib\nmodel_metadata.json", "#fef3c7", "#b45309", 9)
    _box(ax, (52, 31), 40, 15, "Data Layer\nSupabase/PostgreSQL\nlocal JSONL fallback", "#fee2e2", "#b91c1c", 9)
    _box(ax, (8, 9), 84, 13, "External Inputs\nVFND dataset, optional public datasets, user feedback, news URL/text", "#f1f5f9", "#475569", 9)
    _arrow(ax, (50, 76), (50, 69))
    _arrow(ax, (42, 54), (28, 46), "load")
    _arrow(ax, (58, 54), (72, 46), "store")
    _arrow(ax, (50, 22), (50, 31))
    _save(fig, "report_architecture.png")


def use_case_diagram() -> None:
    fig, ax = _setup()
    ax.text(50, 96, "Use Case Diagram", ha="center", fontsize=15, fontweight="bold")
    ax.add_patch(Rectangle((22, 10), 70, 78, linewidth=1.5, edgecolor=INK, facecolor=WHITE))
    ax.text(57, 84, "News Reliability Assessment System", ha="center", fontsize=9)
    ax.add_patch(Circle((10, 65), 3, fill=False, ec=INK, lw=1.4))
    ax.plot([10, 10], [62, 51], color=INK, lw=1.4)
    ax.plot([5, 15], [58, 58], color=INK, lw=1.4)
    ax.plot([10, 6], [51, 44], color=INK, lw=1.4)
    ax.plot([10, 14], [51, 44], color=INK, lw=1.4)
    ax.text(10, 39, "General User", ha="center", fontsize=9)
    ax.add_patch(Circle((10, 25), 3, fill=False, ec=INK, lw=1.4))
    ax.plot([10, 10], [22, 13], color=INK, lw=1.4)
    ax.plot([5, 15], [18, 18], color=INK, lw=1.4)
    ax.plot([10, 6], [13, 7], color=INK, lw=1.4)
    ax.plot([10, 14], [13, 7], color=INK, lw=1.4)
    ax.text(10, 3, "Developer", ha="center", fontsize=9)
    cases = [
        ((32, 70), "Analyze\ntext"),
        ((32, 53), "Analyze\nURL"),
        ((58, 70), "View\nexplanation"),
        ((58, 53), "Submit\nfeedback"),
        ((76, 40), "View\nhistory"),
        ((39, 24), "Train\nmodel"),
        ((66, 24), "Evaluate\npipeline"),
    ]
    for pos, text in cases:
        _ellipse(ax, pos, 15, 10, text)
    for start, target in [
        ((16, 62), (32, 75)),
        ((16, 59), (32, 58)),
        ((16, 56), (58, 75)),
        ((16, 53), (58, 58)),
        ((16, 50), (76, 45)),
    ]:
        _line(ax, start, target)
    for start, target in [((16, 20), (39, 29)), ((16, 17), (66, 29))]:
        _line(ax, start, target)
    _save(fig, "report_use_case.png")


def activity_diagram() -> None:
    fig, ax = _setup(10, 12)
    ax.text(50, 97, "Activity Diagram: Text Analysis", ha="center", fontsize=15, fontweight="bold")
    steps = [
        ("Start", "#e2e8f0"),
        ("User enters text or URL", "#dbeafe"),
        ("Validate input", "#dbeafe"),
        ("Clean and normalize text", "#dcfce7"),
        ("Load cached model", "#dcfce7"),
        ("Run ML inference", "#dcfce7"),
        ("Detect suspicious terms", "#fef3c7"),
        ("Compute final risk score", "#fef3c7"),
        ("Render charts and explanation", "#fee2e2"),
        ("Save prediction to Supabase", "#fee2e2"),
        ("Collect optional feedback", "#fee2e2"),
        ("End", "#e2e8f0"),
    ]
    y = 88
    prev_center = None
    for text, color in steps:
        if text in {"Start", "End"}:
            ax.add_patch(Ellipse((50, y), 25, 7, fc=WHITE, ec=INK, lw=1.4))
            ax.text(50, y, text, ha="center", va="center", fontsize=9)
            center = (50, y)
        else:
            _box(ax, (30, y - 4), 40, 8, text, color, "#475569", 9)
            center = (50, y)
        if prev_center:
            _arrow(ax, (prev_center[0], prev_center[1] - 4), (center[0], center[1] + 4))
        prev_center = center
        y -= 7.5
    _save(fig, "report_activity_analysis.png")


def sequence_diagram() -> None:
    fig, ax = _setup(13, 8)
    ax.text(50, 96, "Sequence Diagram: Prediction Workflow", ha="center", fontsize=15, fontweight="bold")
    actors = [("User", 10), ("Streamlit UI", 28), ("Core Engine", 48), ("Model Artifact", 68), ("Supabase", 88)]
    for name, x in actors:
        _box(ax, (x - 7, 84), 14, 7, name, "#f8fafc", "#334155", 8)
        ax.plot([x, x], [15, 84], color=MID, lw=1, linestyle="--")
    messages = [
        (10, 28, 77, "submit text/url"),
        (28, 48, 69, "clean input"),
        (48, 68, 61, "load cached model"),
        (68, 48, 53, "pipeline object"),
        (48, 48, 45, "predict + score"),
        (48, 28, 37, "result + explanation"),
        (28, 88, 29, "insert prediction"),
        (88, 28, 21, "stored record"),
    ]
    for x1, x2, y, text in messages:
        _arrow(ax, (x1, y), (x2, y), text=text, fontsize=7)
    _save(fig, "report_sequence_prediction.png")


def class_diagram() -> None:
    fig, ax = _setup(14, 8)
    ax.text(50, 96, "Class / Module Diagram", ha="center", fontsize=15, fontweight="bold")
    classes = [
        ((5, 70), 24, 17, "StreamlitApp\n- model selection\n- render result\n- feedback form"),
        ((38, 70), 24, 17, "InferenceEngine\n- predict_reliability()\n- risk_score()\n- probabilities()"),
        ((71, 70), 24, 17, "Explainability\n- explain_linear_prediction()\n- top tokens"),
        ((5, 38), 24, 19, "TextPreprocessor\n- normalize_unicode()\n- preprocess_for_ml()\n- suspicious terms"),
        ((38, 38), 24, 19, "TrainingPipeline\n- prepare data\n- train baselines\n- export artifacts"),
        ((71, 38), 24, 19, "SupabaseClient\n- insert_prediction()\n- insert_feedback()\n- list_predictions()"),
        ((22, 11), 24, 16, "Configuration\n- paths\n- env variables\n- allowed domains"),
        ((56, 11), 24, 16, "Evaluation\n- artifact check\n- metrics\n- confusion matrix"),
    ]
    for xy, w, h, text in classes:
        _box(ax, xy, w, h, text, "#f8fafc", "#334155", 8)
    _arrow(ax, (29, 78), (38, 78))
    _arrow(ax, (62, 78), (71, 78))
    _arrow(ax, (17, 70), (17, 57))
    _arrow(ax, (50, 70), (50, 57))
    _arrow(ax, (83, 70), (83, 57))
    _arrow(ax, (50, 38), (50, 27))
    _arrow(ax, (83, 38), (68, 27))
    _arrow(ax, (17, 38), (34, 27))
    _save(fig, "report_class_module.png")


def erd_diagram() -> None:
    fig, ax = _setup(12, 7)
    ax.text(50, 96, "Database ERD", ha="center", fontsize=15, fontweight="bold")
    pred = (
        "predictions\n"
        "PK id: bigserial\n"
        "client_prediction_id: text unique\n"
        "input_type: text\n"
        "text: text\n"
        "model_name: text\n"
        "predicted_label: integer\n"
        "confidence: double\n"
        "risk_score: double\n"
        "probabilities: jsonb\n"
        "suspicious_terms: jsonb\n"
        "created_at: timestamptz"
    )
    feed = (
        "feedback\n"
        "PK id: bigserial\n"
        "FK prediction_id: bigint\n"
        "prediction_client_id: text\n"
        "is_correct: boolean\n"
        "comment: text\n"
        "created_at: timestamptz"
    )
    _box(ax, (7, 25), 38, 57, pred, "#eef2ff", "#4338ca", 8)
    _box(ax, (58, 34), 35, 40, feed, "#ecfdf5", "#047857", 8)
    _arrow(ax, (58, 54), (45, 54), "feedback references prediction", "#475569")
    ax.text(50, 17, "Relationship: one prediction can receive zero or many feedback records.", ha="center", fontsize=9)
    _save(fig, "report_database_erd.png")


def training_pipeline_diagram() -> None:
    fig, ax = _setup(14, 6)
    ax.text(50, 94, "Training and Evaluation Pipeline", ha="center", fontsize=15, fontweight="bold")
    items = [
        ("Raw dataset\nVFND", "#dbeafe"),
        ("Schema\nnormalization", "#dbeafe"),
        ("Cleaning and\ndeduplication", "#dcfce7"),
        ("Train / val /\ntest split", "#dcfce7"),
        ("TF-IDF\nfeatures", "#fef3c7"),
        ("Train 4\nbaselines", "#fef3c7"),
        ("Compare by\nvalidation F1", "#fee2e2"),
        ("Export best\nmodel + reports", "#fee2e2"),
    ]
    x = 3
    centers = []
    for text, color in items:
        _box(ax, (x, 47), 10.8, 24, text, color, "#334155", 7.8)
        centers.append((x + 10.8, 59))
        x += 12.2
    for i in range(len(centers) - 1):
        _arrow(ax, centers[i], (centers[i + 1][0] - 10.8, centers[i + 1][1]))
    _box(ax, (18, 16), 25, 13, "Metrics\nAccuracy, Precision, Recall, F1, ROC-AUC", "#f8fafc", "#475569", 8)
    _box(ax, (57, 16), 25, 13, "Artifacts\nbaseline_best.joblib, metadata, confusion matrices", "#f8fafc", "#475569", 8)
    _arrow(ax, (77, 47), (69, 29), color="#475569")
    _save(fig, "report_training_pipeline.png")


def deployment_diagram() -> None:
    fig, ax = _setup()
    ax.text(50, 96, "Deployment View", ha="center", fontsize=15, fontweight="bold")
    _box(ax, (6, 64), 25, 17, "User Browser\nlocal or cloud access", "#dbeafe", "#1d4ed8", 9)
    _box(ax, (38, 64), 25, 17, "Streamlit Runtime\napp/streamlit_app.py", "#dcfce7", "#15803d", 9)
    _box(ax, (69, 64), 25, 17, "Supabase Cloud\nPostgreSQL + REST API", "#fee2e2", "#b91c1c", 9)
    _box(ax, (38, 35), 25, 17, "Local Model Store\nmodels/artifacts", "#fef3c7", "#b45309", 9)
    _box(ax, (6, 20), 25, 14, "GitHub Repository\nsource code + notebook", "#f8fafc", "#475569", 8)
    _box(ax, (69, 20), 25, 14, "Google Colab\nretraining workflow", "#f8fafc", "#475569", 8)
    _arrow(ax, (31, 72), (38, 72), "HTTP")
    _arrow(ax, (63, 72), (69, 72), "SDK")
    _arrow(ax, (50, 64), (50, 52), "load model")
    _arrow(ax, (31, 27), (38, 39), "clone/run")
    _arrow(ax, (81, 34), (63, 43), "export artifact", rad=0.12)
    _save(fig, "report_deployment_view.png")


def feedback_loop_diagram() -> None:
    fig, ax = _setup(12, 7)
    ax.text(50, 96, "Feedback Loop for Model Improvement", ha="center", fontsize=15, fontweight="bold")
    nodes = [
        ((8, 58), "User\nfeedback"),
        ((34, 58), "Supabase\nstorage"),
        ((60, 58), "Review and\nclean labels"),
        ((34, 26), "Retraining\nnotebook"),
        ((60, 26), "New model\nartifact"),
        ((82, 42), "Streamlit\napp update"),
    ]
    for xy, text in nodes:
        _box(ax, xy, 16, 12, text, "#f8fafc", "#334155", 8)
    _arrow(ax, (24, 64), (34, 64))
    _arrow(ax, (50, 64), (60, 64))
    _arrow(ax, (68, 58), (42, 38), rad=-0.18)
    _arrow(ax, (50, 32), (60, 32))
    _arrow(ax, (76, 32), (82, 45))
    _arrow(ax, (82, 48), (24, 64), rad=0.22)
    _save(fig, "report_feedback_loop.png")


def ui_layout_diagram() -> None:
    fig, ax = _setup(13, 8)
    ax.text(50, 96, "Streamlit Interface Layout", ha="center", fontsize=15, fontweight="bold")
    _box(ax, (5, 10), 18, 78, "Sidebar\n\nModel selector\nLabel convention\nBest model\nMetadata", "#f8fafc", "#475569", 8)
    _box(ax, (27, 76), 68, 12, "Header\nMachine Learning-based News Reliability Assessment", "#dbeafe", "#1d4ed8", 9)
    _box(ax, (27, 58), 68, 14, "Input Area\nText area or URL input + Analyze button", "#ffffff", "#64748b", 9)
    _box(ax, (27, 42), 20, 11, "Risk score", "#fee2e2", "#b91c1c", 8)
    _box(ax, (51, 42), 20, 11, "Confidence", "#dcfce7", "#15803d", 8)
    _box(ax, (75, 42), 20, 11, "ML / lexical risk", "#fef3c7", "#b45309", 8)
    _box(ax, (27, 22), 33, 15, "Highlighted text\nSuspicious keywords", "#fff7ed", "#c2410c", 8)
    _box(ax, (64, 22), 31, 15, "Charts and token explanation", "#eef2ff", "#4338ca", 8)
    _box(ax, (27, 10), 68, 8, "History tab and feedback form", "#ecfdf5", "#047857", 8)
    _save(fig, "report_ui_layout.png")


def result_dashboard_diagram() -> None:
    fig, ax = _setup(13, 7)
    ax.text(50, 96, "Result Visualization Dashboard", ha="center", fontsize=15, fontweight="bold")
    _box(ax, (6, 74), 88, 12, "Prediction Result\nLabel: Reliable or Unreliable | Confidence | Explanation summary", "#f8fafc", "#334155", 9)
    _box(ax, (6, 54), 20, 13, "Risk score\n92.0%", "#fee2e2", "#b91c1c", 9)
    _box(ax, (30, 54), 20, 13, "Confidence\n91.9%", "#dcfce7", "#15803d", 9)
    _box(ax, (54, 54), 20, 13, "ML risk", "#fef3c7", "#b45309", 9)
    _box(ax, (78, 54), 16, 13, "Lexical risk", "#fef3c7", "#b45309", 9)
    _box(ax, (6, 24), 42, 23, "Highlighted article preview\nmark suspicious terms such as clickbait,\nemotional manipulation and credibility warnings", "#fff7ed", "#c2410c", 8)
    _box(ax, (54, 24), 40, 23, "Token explanation table\nTop terms pushing toward reliable/unreliable\nText statistics and suspicious term table", "#eef2ff", "#4338ca", 8)
    _box(ax, (6, 8), 88, 10, "Saved record: predictions table | Feedback: correct / incorrect / uncertain", "#ecfdf5", "#047857", 8)
    _save(fig, "report_result_dashboard.png")


def main() -> int:
    architecture_diagram()
    use_case_diagram()
    activity_diagram()
    sequence_diagram()
    class_diagram()
    erd_diagram()
    training_pipeline_diagram()
    deployment_diagram()
    feedback_loop_diagram()
    ui_layout_diagram()
    result_dashboard_diagram()
    print(f"Generated report figures in {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
