from __future__ import annotations

from pathlib import Path

from scripts._bootstrap import ensure_repo_root_on_path
from scripts.run_pipeline import run_pipeline
from src.evaluation.baseline_eval import evaluate_artifacts, required_artifact_paths


def test_ensure_repo_root_on_path_includes_repo_root():
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "download_data.py"
    repo_root = ensure_repo_root_on_path(script_path)
    assert repo_root == Path(__file__).resolve().parents[1]


def test_evaluate_artifacts_reports_missing_files(tmp_path: Path):
    status = evaluate_artifacts(tmp_path)
    assert status["ok"] is False
    assert len(status["missing_files"]) == len(required_artifact_paths(tmp_path))


def test_evaluate_artifacts_passes_when_required_files_exist(tmp_path: Path):
    for rel_path in required_artifact_paths(tmp_path):
        target = tmp_path / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("ok", encoding="utf-8")

    status = evaluate_artifacts(tmp_path)
    assert status["ok"] is True
    assert status["missing_files"] == []


def test_run_pipeline_executes_steps_in_order():
    calls: list[str] = []

    def _fake_runner(step_name: str) -> None:
        calls.append(step_name)

    run_pipeline(step_runner=_fake_runner)

    assert calls == ["download_data.py", "prepare_data.py", "train_baseline.py", "evaluate.py"]
