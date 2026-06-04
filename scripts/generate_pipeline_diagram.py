"""Generate academic Data Processing Pipeline Diagram for Word reports."""
from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

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

def _phase_box(ax, cx, cy, w, h, title, bullets):
    # Sharp academic rectangle with white fill
    ax.add_patch(Rectangle((cx - w/2, cy - h/2), w, h,
                           lw=1.2, ec=BLACK, fc=WHITE))
    
    # Title
    ax.text(cx, cy + h/2 - 2.5, title, ha="center", va="top", fontsize=9.5, fontweight="bold")
    # Separator
    ax.plot([cx - w/2, cx + w/2], [cy + h/2 - 5, cy + h/2 - 5], color=BLACK, lw=0.8)
    
    # Bullets
    bullet_y = cy + h/2 - 8.0
    for b in bullets:
        ax.text(cx - w/2 + 2.5, bullet_y, f"•  {b}", ha="left", va="center", fontsize=8.5)
        bullet_y -= 3.5

def _flow_arrow(ax, start, end):
    ax.add_patch(FancyArrowPatch(start, end,
                                 arrowstyle="-|>", mutation_scale=16,
                                 lw=1.2, color=BLACK))

def generate() -> None:
    fig, ax = plt.subplots(figsize=(8, 7.2), dpi=220)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 90)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.text(50, 86, "Figure 6. Training and evaluation pipeline",
            ha="center", fontsize=11.5, style="italic", color=BLACK)

    # Box dimensions
    W = 40
    
    # Y levels
    Y1 = 66
    Y2 = 36
    Y3 = 10
    
    # X columns
    X1 = 25
    X2 = 75

    # Phase 1
    h1 = 15
    _phase_box(ax, X1, Y1, W, h1, "Phase 1: Data Discovery", [
        "Download/locate raw datasets",
        "Discover CSV, JSON, TXT files"
    ])

    # Phase 2
    h2 = 22
    _phase_box(ax, X2, Y1, W, h2, "Phase 2: Cleaning", [
        "Normalize to common schema",
        "Clean text & drop invalid rows",
        "Binarize labels (0 and 1)",
        "Remove duplicated records"
    ])

    # Phase 3
    h3 = 12
    _phase_box(ax, X2, Y2, W, h3, "Phase 3: Splitting", [
        "Split into Train, Val, Test"
    ])

    # Phase 4
    h4 = 19
    _phase_box(ax, X1, Y2, W, h4, "Phase 4: Training", [
        "Train 4 baseline models",
        "Compare validation metrics",
        "Refit best on Train + Val"
    ])

    # Phase 5
    h5 = 15
    _phase_box(ax, X1, Y3, W, h5, "Phase 5: Evaluation", [
        "Evaluate on Test set",
        "Export artifacts & metrics"
    ])

    # Arrows (Snake pattern)
    # 1 -> 2 (horizontal right)
    _flow_arrow(ax, (X1 + W/2, Y1), (X2 - W/2, Y1))
    
    # 2 -> 3 (vertical down)
    _flow_arrow(ax, (X2, Y1 - h2/2), (X2, Y2 + h3/2))
    
    # 3 -> 4 (horizontal left)
    _flow_arrow(ax, (X2 - W/2, Y2), (X1 + W/2, Y2))
    
    # 4 -> 5 (vertical down)
    _flow_arrow(ax, (X1, Y2 - h4/2), (X1, Y3 + h5/2))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / "report_training_pipeline.png"
    fig.savefig(path, bbox_inches="tight", facecolor=WHITE, pad_inches=0.25, dpi=220)
    plt.close(fig)
    print(f"✓ {path}")

if __name__ == "__main__":
    generate()
