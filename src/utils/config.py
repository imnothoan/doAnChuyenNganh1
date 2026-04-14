from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    project_root: Path = Path(__file__).resolve().parents[2]
    data_raw_dir: Path = project_root / "data" / "raw"
    data_interim_dir: Path = project_root / "data" / "interim"
    data_processed_dir: Path = project_root / "data" / "processed"
    models_artifacts_dir: Path = project_root / "models" / "artifacts"
    models_reports_dir: Path = project_root / "models" / "reports"
    reports_dir: Path = project_root / "reports"
    reports_figures_dir: Path = reports_dir / "figures"

    min_text_length: int = int(os.getenv("MIN_TEXT_LENGTH", "20"))
    random_state: int = int(os.getenv("RANDOM_STATE", "42"))
    val_size: float = float(os.getenv("VAL_SIZE", "0.15"))
    test_size: float = float(os.getenv("TEST_SIZE", "0.15"))
    allowed_news_domains: tuple[str, ...] = tuple(
        item.strip().lower()
        for item in os.getenv("ALLOWED_NEWS_DOMAINS", "").split(",")
        if item.strip()
    )


CFG = Config()


def ensure_directories() -> None:
    for path in [
        CFG.data_raw_dir,
        CFG.data_interim_dir,
        CFG.data_processed_dir,
        CFG.models_artifacts_dir,
        CFG.models_reports_dir,
        CFG.reports_dir,
        CFG.reports_figures_dir,
    ]:
        path.mkdir(parents=True, exist_ok=True)
