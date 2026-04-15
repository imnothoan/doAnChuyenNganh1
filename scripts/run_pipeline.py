from __future__ import annotations

import subprocess
import sys
from pathlib import Path

try:
    from scripts._bootstrap import ensure_repo_root_on_path
except ModuleNotFoundError:
    from _bootstrap import ensure_repo_root_on_path

REPO_ROOT = ensure_repo_root_on_path(__file__)


def _run_step(script_name: str) -> None:
    script_path = Path(REPO_ROOT) / "scripts" / script_name
    result = subprocess.run([sys.executable, str(script_path)], cwd=str(REPO_ROOT))
    if result.returncode != 0:
        raise RuntimeError(f"Step failed: {script_name}")


if __name__ == "__main__":
    for step in ["download_data.py", "prepare_data.py", "train_baseline.py", "evaluate.py"]:
        print(f"==> Running {step}")
        _run_step(step)
    print("Pipeline completed successfully.")
