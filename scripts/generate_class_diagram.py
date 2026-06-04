"""Generate academic UML Package/Module Diagram for Word reports."""
from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reports" / "figures"
BLACK = "#000000"
GRAY = "#555555"
WHITE = "#FFFFFF"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "text.color": BLACK,
    "figure.facecolor": WHITE,
})

def _package(ax, x, y, w, h, title, content, fs=7.5, bg=WHITE):
    tab_w = min(w * 0.55, 16)
    tab_h = 3.2
    body_h = h - tab_h
    pts = [
        (x, y),
        (x + w, y),
        (x + w, y + body_h),
        (x + tab_w, y + body_h),
        (x + tab_w, y + h),
        (x, y + h)
    ]
    ax.add_patch(plt.Polygon(pts, closed=True, fc=bg, ec=BLACK, lw=1.2))
    ax.text(x + tab_w/2, y + body_h + tab_h/2, title, ha="center", va="center", fontsize=fs+1.5, fontweight="bold")
    if content:
        ax.text(x + w/2, y + body_h/2, content, ha="center", va="center", fontsize=fs, linespacing=1.4)

def _dependency(ax, s, e):
    arr = FancyArrowPatch(s, e, arrowstyle="->", mutation_scale=15,
                          lw=1.2, color=BLACK, linestyle="--", shrinkA=0, shrinkB=0)
    ax.add_patch(arr)


def generate() -> None:
    fig, ax = plt.subplots(figsize=(10, 10.5), dpi=220)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.text(50, 95, "Figure 5. Class and module diagram",
            ha="center", fontsize=12, style="italic", color=BLACK)

    # Top Level
    _package(ax, 36, 70, 28, 16, "app/", "streamlit_app.py\n- Renders UI, handles input\n- Displays results, history\n- Collects feedback")

    # Core Engine (src)
    src_x, src_y = 3, 8
    src_w, src_h = 94, 52
    _package(ax, src_x, src_y, src_w, src_h, "src/", "", bg="#F9F9F9")

    # Inside src: Row 2
    _package(ax, 6, 34, 26, 17, "features", "- Cleans text\n- Extracts suspicious terms\n- Computes text statistics")
    _package(ax, 37, 34, 26, 17, "models", "- Trains models\n- Loads artifacts\n- Runs inference\n- Calculates risk score")
    _package(ax, 68, 34, 26, 17, "explainability", "- Generates token-level\n  explanations for\n  model output")

    # Inside src: Row 1
    _package(ax, 6, 12, 26, 17, "data", "- Downloads datasets\n- Normalizes schema\n- Prepares splits\n- Connects to Supabase")
    _package(ax, 37, 12, 26, 17, "utils", "- Stores configuration\n- Paths & shared helpers")
    _package(ax, 68, 12, 26, 17, "evaluation", "- Verifies artifacts\n- Evaluates pipeline\n  readiness")

    # Dependencies
    _dependency(ax, (50, 70), (50, 60))      # app -> src
    
    # Legend
    _dependency(ax, (70, 3), (78, 3))
    ax.text(80, 3, "Depends on", fontsize=8, va="center", color=GRAY, style="italic")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / "report_class_module.png"
    fig.savefig(path, bbox_inches="tight", facecolor=WHITE, pad_inches=0.25, dpi=220)
    plt.close(fig)
    print(f"✓ {path}")


if __name__ == "__main__":
    generate()
