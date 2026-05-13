from __future__ import annotations

import logging

try:
    from scripts._bootstrap import ensure_repo_root_on_path
except ModuleNotFoundError:
    from _bootstrap import ensure_repo_root_on_path

ensure_repo_root_on_path(__file__)

from src.data.download_manager import download_datasets

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    statuses = download_datasets()
    for status in statuses:
        print(f"[{status.status}] {status.dataset}: {status.message}")
    logger.info("Saved source status report to reports/dataset_sources.json")
