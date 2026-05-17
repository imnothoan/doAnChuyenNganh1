from __future__ import annotations

import json
from pathlib import Path

from src.utils.config import CFG, ensure_directories


def required_artifact_paths(project_root: Path | None = None) -> list[Path]:
    root = project_root or CFG.project_root
    return [
        Path("data/processed/train.csv"),
        Path("data/processed/val.csv"),
        Path("data/processed/test.csv"),
        Path("models/artifacts/baseline_best.joblib"),
        Path("models/reports/model_metadata.json"),
        Path("reports/metrics_baseline.json"),
        Path("reports/model_comparison.md"),
        Path("reports/figures/confusion_matrix_lr.png"),
        Path("reports/figures/confusion_matrix_svm.png"),
        Path("reports/figures/confusion_matrix_rf.png"),
        Path("reports/figures/confusion_matrix_nb.png"),
    ]


def evaluate_artifacts(project_root: Path | None = None) -> dict:
    root = (project_root or CFG.project_root).resolve()
    missing = [str(path) for path in required_artifact_paths(root) if not (root / path).exists()]
    status = {
        "ok": len(missing) == 0,
        "project_root": str(root),
        "missing_files": missing,
    }
    return status


def write_evaluation_report(project_root: Path | None = None) -> dict:
    ensure_directories()
    status = evaluate_artifacts(project_root)
    report_path = CFG.reports_dir / "pipeline_evaluation.json"
    report_status = {**status, "project_root": "."}
    report_path.write_text(json.dumps(report_status, indent=2, ensure_ascii=False), encoding="utf-8")
    status["report_path"] = str(report_path)
    return status
