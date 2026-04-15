from __future__ import annotations

import subprocess
import sys
from pathlib import Path

try:
    from scripts._bootstrap import ensure_repo_root_on_path
except ModuleNotFoundError:
    from _bootstrap import ensure_repo_root_on_path

REPO_ROOT = ensure_repo_root_on_path(__file__)
PIPELINE_STEPS = ["download_data.py", "prepare_data.py", "train_baseline.py", "evaluate.py"]


def _run_step(script_name: str) -> None:
    script_path = Path(REPO_ROOT) / "scripts" / script_name
    try:
        subprocess.run([sys.executable, str(script_path)], cwd=str(REPO_ROOT), check=True)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Step failed: {script_name}") from exc


def run_pipeline(step_runner=_run_step) -> None:
    for step in PIPELINE_STEPS:
        print(f"==> Running {step}")
        step_runner(step)
    print("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
