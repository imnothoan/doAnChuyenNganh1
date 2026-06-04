"""Generate academic UML Activity Diagram with swimlane partitions."""
from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

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


def _arrow(ax, s, e):
    ax.add_patch(FancyArrowPatch(s, e, arrowstyle="-|>", mutation_scale=13,
                                  lw=1.0, color=BLACK, shrinkA=0, shrinkB=0))

def _line(ax, s, e):
    ax.plot([s[0], e[0]], [s[1], e[1]], color=BLACK, lw=1.0)

def _box(ax, cx, cy, w, h, text, fs=8):
    ax.add_patch(FancyBboxPatch((cx-w/2, cy-h/2), w, h,
                                 boxstyle="round,pad=0.12", lw=1.2, ec=BLACK, fc=WHITE))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color=BLACK, linespacing=1.25)

def _diamond(ax, cx, cy, s=6.0):
    h = s/2
    ax.add_patch(plt.Polygon([(cx,cy+h),(cx+h,cy),(cx,cy-h),(cx-h,cy)],
                              closed=True, lw=1.2, ec=BLACK, fc=WHITE))

def _initial(ax, cx, cy):
    ax.add_patch(Circle((cx,cy), 1.1, fc=BLACK, ec=BLACK))

def _final(ax, cx, cy):
    ax.add_patch(Circle((cx,cy), 1.4, fc=WHITE, ec=BLACK, lw=2.0))
    ax.add_patch(Circle((cx,cy), 0.75, fc=BLACK, ec=BLACK))

def _bar(ax, cx, cy, w=30):
    ax.add_patch(Rectangle((cx-w/2, cy-0.35), w, 0.7, fc=BLACK, ec=BLACK))

def _guard(ax, x, y, text, ha="left"):
    ax.text(x, y, text, ha=ha, va="center", fontsize=7.2, color=GRAY, style="italic")


def generate() -> None:
    fig, ax = plt.subplots(figsize=(11, 23), dpi=220)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 205)
    ax.set_aspect("equal")
    ax.axis("off")

    # Title
    ax.text(50, 202, "Figure 3.  Activity diagram for text analysis",
            ha="center", fontsize=12, style="italic", color=BLACK)

    # ── Frame & Partitions ──
    FRAME_L, FRAME_R = 3, 97
    FRAME_T, FRAME_B = 198, 48
    LABEL_W = 12  # left label column width
    MAIN_L = FRAME_L + LABEL_W  # x=15

    # Partition boundaries (horizontal)
    P12 = 149  # between Input & Processing
    P23 = 93   # between Processing & Output

    # Outer frame
    ax.add_patch(Rectangle((FRAME_L, FRAME_B), FRAME_R-FRAME_L, FRAME_T-FRAME_B,
                            lw=1.5, ec=BLACK, fc="none"))
    # Label column divider
    _line(ax, (MAIN_L, FRAME_T), (MAIN_L, FRAME_B))
    # Partition dividers
    _line(ax, (FRAME_L, P12), (FRAME_R, P12))
    _line(ax, (FRAME_L, P23), (FRAME_R, P23))

    # Partition labels (rotated)
    ax.text((FRAME_L+MAIN_L)/2, (FRAME_T+P12)/2, "Input &\nValidation",
            ha="center", va="center", fontsize=8.5, rotation=90, color=BLACK, linespacing=1.3)
    ax.text((FRAME_L+MAIN_L)/2, (P12+P23)/2, "NLP & ML\nProcessing",
            ha="center", va="center", fontsize=8.5, rotation=90, color=BLACK, linespacing=1.3)
    ax.text((FRAME_L+MAIN_L)/2, (P23+FRAME_B)/2, "Result &\nStorage",
            ha="center", va="center", fontsize=8.5, rotation=90, color=BLACK, linespacing=1.3)

    # ── Layout constants ──
    CX = 55
    BW, BH = 24, 5.5
    DS = 6.5

    # ================================================================
    # PARTITION 1: INPUT & VALIDATION
    # ================================================================

    # (1) Initial node
    iy = 193
    _initial(ax, CX, iy)

    # (2) User enters text or URL
    y2 = 185
    _box(ax, CX, y2, BW, BH, "User enters\ntext or URL")
    _arrow(ax, (CX, iy-1.1), (CX, y2+BH/2))

    # (3) Decision: input type?
    y3 = 175
    _diamond(ax, CX, y3, DS)
    ax.text(CX, y3, "Input\ntype?", ha="center", va="center", fontsize=6.8, linespacing=1.1)
    _arrow(ax, (CX, y2-BH/2), (CX, y3+DS/2))

    # [URL] → left
    ux = 30
    _box(ax, ux, y3, 16, BH, "Extract text\nfrom URL")
    _arrow(ax, (CX-DS/2, y3), (ux+8, y3))
    _guard(ax, CX-DS/2-1, y3+4, "[URL]", ha="center")
    _guard(ax, CX+DS/2+1.5, y3+3.5, "[Text]")

    # (4) Validate input
    y4 = 164
    _box(ax, CX, y4, BW, BH, "Validate input")
    _arrow(ax, (CX, y3-DS/2), (CX, y4+BH/2))
    # URL merge
    _line(ax, (ux, y3-BH/2), (ux, y4))
    _arrow(ax, (ux, y4), (CX-BW/2, y4))

    # (5) Decision: valid?
    y5 = 155
    _diamond(ax, CX, y5, DS)
    ax.text(CX, y5, "Valid?", ha="center", va="center", fontsize=7)
    _arrow(ax, (CX, y4-BH/2), (CX, y5+DS/2))

    # [No] → right: Show warning → loop back
    wx = 84
    _box(ax, wx, y5, 13, BH, "Show\nwarning")
    _arrow(ax, (CX+DS/2, y5), (wx-6.5, y5))
    _guard(ax, CX+DS/2+1, y5+3.5, "[No]")
    _guard(ax, CX-DS/2-1, y5+3.5, "[Yes]", ha="center")
    # Loop back: up then left
    _line(ax, (wx, y5+BH/2), (wx, y2))
    _arrow(ax, (wx, y2), (CX+BW/2, y2))

    # ================================================================
    # PARTITION 2: NLP & ML PROCESSING
    # ================================================================

    # (6) Preprocess content
    y6 = 143
    _box(ax, CX, y6, BW, BH, "Preprocess content")
    _arrow(ax, (CX, y5-DS/2), (CX, y6+BH/2))

    # (7) Load cached model
    y7 = 134
    _box(ax, CX, y7, BW, BH, "Load cached model")
    _arrow(ax, (CX, y6-BH/2), (CX, y7+BH/2))

    # (8) Fork bar
    y8 = 127
    _bar(ax, CX, y8, w=32)
    _arrow(ax, (CX, y7-BH/2), (CX, y8+0.35))

    # Parallel left: ML inference
    ml_x, ml_y = 40, 119
    _box(ax, ml_x, ml_y, 21, BH, "Perform ML\ninference")
    _arrow(ax, (ml_x, y8-0.35), (ml_x, ml_y+BH/2))

    # Parallel right: Detect suspicious terms
    lx_x, lx_y = 70, 119
    _box(ax, lx_x, lx_y, 21, BH, "Detect suspicious\nterms")
    _arrow(ax, (lx_x, y8-0.35), (lx_x, lx_y+BH/2))

    # (9) Join bar
    y9 = 112
    _bar(ax, CX, y9, w=32)
    _arrow(ax, (ml_x, ml_y-BH/2), (ml_x, y9+0.35))
    _arrow(ax, (lx_x, lx_y-BH/2), (lx_x, y9+0.35))

    # (10) Compute final risk score
    y10 = 105
    _box(ax, CX, y10, BW, BH, "Compute final\nrisk score")
    _arrow(ax, (CX, y9-0.35), (CX, y10+BH/2))

    # (11) Generate token explanation
    y11 = 97
    _box(ax, CX, y11, BW, BH, "Generate token\nexplanation")
    _arrow(ax, (CX, y10-BH/2), (CX, y11+BH/2))

    # ================================================================
    # PARTITION 3: RESULT & STORAGE
    # ================================================================

    # (12) Render result dashboard
    y12 = 88
    _box(ax, CX, y12, BW, BH, "Render result\ndashboard")
    _arrow(ax, (CX, y11-BH/2), (CX, y12+BH/2))

    # (13) Save prediction to database
    y13 = 80
    _box(ax, CX, y13, BW, BH, "Save prediction\nto database")
    _arrow(ax, (CX, y12-BH/2), (CX, y13+BH/2))

    # (14) Decision: user feedback?
    y14 = 70
    _diamond(ax, CX, y14, DS)
    ax.text(CX, y14, "User\nfeedback?", ha="center", va="center",
            fontsize=6.8, linespacing=1.1)
    _arrow(ax, (CX, y13-BH/2), (CX, y14+DS/2))

    # [Yes] → left
    fb_x, fb_y = 30, 61
    _box(ax, fb_x, fb_y, 16, BH, "Store feedback")
    _line(ax, (CX-DS/2, y14), (fb_x, y14))
    _arrow(ax, (fb_x, y14), (fb_x, fb_y+BH/2))
    _guard(ax, CX-DS/2-1, y14+4, "[Yes]", ha="center")
    _guard(ax, CX+DS/2+1.5, y14+3.5, "[No]")

    # (15) Final node
    fy = 53
    _final(ax, CX, fy)
    _arrow(ax, (CX, y14-DS/2), (CX, fy+1.4))
    # Feedback merge
    _line(ax, (fb_x, fb_y-BH/2), (fb_x, fy))
    _arrow(ax, (fb_x, fy), (CX-1.4, fy))

    # ── Legend (below frame) ──
    ly = 43
    ax.text(6, ly, "Legend:", fontsize=8.5, fontweight="bold")
    lx_pos = [8, 22, 38, 57, 76]
    _initial(ax, lx_pos[0], ly-5); ax.text(lx_pos[0]+2.5, ly-5, "Initial node", fontsize=6.5, va="center", color=GRAY)
    _final(ax, lx_pos[1]+1, ly-5); ax.text(lx_pos[1]+4, ly-5, "Final node", fontsize=6.5, va="center", color=GRAY)
    _box(ax, lx_pos[2]+3.5, ly-5, 7, 2.5, "Action", fs=6); ax.text(lx_pos[2]+8.5, ly-5, "Action state", fontsize=6.5, va="center", color=GRAY)
    _diamond(ax, lx_pos[3]+1, ly-5, s=2.2); ax.text(lx_pos[3]+3.5, ly-5, "Decision", fontsize=6.5, va="center", color=GRAY)
    _bar(ax, lx_pos[4]+2, ly-5, w=4); ax.text(lx_pos[4]+5.5, ly-5, "Fork / Join", fontsize=6.5, va="center", color=GRAY)

    # Save
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / "report_activity_analysis.png"
    fig.savefig(path, bbox_inches="tight", facecolor=WHITE, pad_inches=0.25, dpi=220)
    plt.close(fig)
    print(f"✓ {path}")


if __name__ == "__main__":
    generate()
