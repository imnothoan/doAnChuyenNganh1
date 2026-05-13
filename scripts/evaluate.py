from __future__ import annotations

import json
import sys

try:
    from scripts._bootstrap import ensure_repo_root_on_path
except ModuleNotFoundError:
    from _bootstrap import ensure_repo_root_on_path

ensure_repo_root_on_path(__file__)

from src.evaluation.baseline_eval import write_evaluation_report


if __name__ == "__main__":
    status = write_evaluation_report()
    print(json.dumps(status, ensure_ascii=False, indent=2))
    sys.exit(0 if status["ok"] else 1)
