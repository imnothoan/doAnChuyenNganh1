from __future__ import annotations

import json
from pathlib import Path

from src.utils.config import CFG


def train_transformer_or_report_fallback() -> dict:
    report = {
        "status": "skipped",
        "reason": "Transformer training requires GPU/Colab resources and optional dependencies.",
        "recommendation": "Use Google Colab with PhoBERT and save output metrics to reports/metrics_transformer.json.",
    }
    (CFG.reports_dir / "metrics_transformer.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


if __name__ == "__main__":
    print(train_transformer_or_report_fallback())
