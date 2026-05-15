from __future__ import annotations

import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.features.text_preprocessing import basic_clean_text, combine_title_content
from src.utils.config import CFG, ensure_directories

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

UNIFIED_COLUMNS = [
    "id",
    "source_dataset",
    "source_type",
    "title",
    "content",
    "text",
    "label",
    "url",
    "published_at",
]

TITLE_CANDIDATES = ["title", "headline", "subject", "news_title"]
CONTENT_CANDIDATES = ["content", "body", "text", "maintext", "main_text", "description", "article", "news"]
LABEL_CANDIDATES = ["label", "class", "target", "verdict", "is_fake"]
URL_CANDIDATES = ["url", "link", "source_url"]
TIME_CANDIDATES = ["published_at", "date_publish", "date", "datetime", "time", "timestamp"]


LABEL_MAP = {
    "real": 0,
    "true": 0,
    "reliable": 0,
    "credible": 0,
    "trusted": 0,
    "0": 0,
    "fake": 1,
    "false": 1,
    "unreliable": 1,
    "misleading": 1,
    "rumor": 1,
    "clickbait": 1,
    "1": 1,
}


def _first_available_column(df: pd.DataFrame, candidates: list[str], default: str = "") -> pd.Series:
    lowered = {str(col).strip().lower(): col for col in df.columns}
    for candidate in candidates:
        if candidate in lowered:
            return df[lowered[candidate]].fillna("").astype(str)
    if default:
        return pd.Series([default] * len(df), index=df.index, dtype="string")
    return pd.Series([""] * len(df), index=df.index, dtype="string")


def normalize_label(value: object) -> int | None:
    if pd.isna(value):
        return None
    normalized = str(value).strip().lower()
    if normalized in LABEL_MAP:
        return LABEL_MAP[normalized]
    if normalized.isdigit():
        as_int = int(normalized)
        return 1 if as_int > 0 else 0
    return None


def dataset_name_from_path(path: Path) -> str:
    try:
        rel_parts = path.relative_to(CFG.data_raw_dir).parts
    except ValueError:
        rel_parts = path.parts
    useful_parts = [
        part
        for part in rel_parts[:-1]
        if part not in {".git", "CSV", "Dataset", "Dictionaries"} and not part.startswith(".")
    ]
    if not useful_parts:
        return path.parent.name or "unknown"
    return "_".join(useful_parts[:2]).lower()


def infer_label_from_path(path: Path) -> int | None:
    lowered_parts = {part.lower() for part in path.parts}
    if "fake" in lowered_parts or "misleading" in lowered_parts:
        return 1
    if "real" in lowered_parts:
        return 0
    lowered_name = path.name.lower()
    if "_fake_" in lowered_name or "fake" in lowered_name:
        return 1
    if "_real_" in lowered_name or "real" in lowered_name:
        return 0
    return None


def _stable_id(text: str, dataset_name: str) -> str:
    digest = hashlib.sha256(f"{dataset_name}::{text}".encode("utf-8")).hexdigest()[:16]
    return f"{dataset_name}_{digest}"


def unify_and_clean_dataframe(
    df: pd.DataFrame,
    dataset_name: str,
    min_text_length: int | None = None,
    label_hint: int | None = None,
) -> pd.DataFrame:
    min_text_length = min_text_length if min_text_length is not None else CFG.min_text_length
    title = _first_available_column(df, TITLE_CANDIDATES)
    content = _first_available_column(df, CONTENT_CANDIDATES)
    labels = _first_available_column(df, LABEL_CANDIDATES, default=str(label_hint) if label_hint is not None else "")
    urls = _first_available_column(df, URL_CANDIDATES)
    published_at = _first_available_column(df, TIME_CANDIDATES)

    clean_df = pd.DataFrame(
        {
            "title": title.map(basic_clean_text),
            "content": content.map(basic_clean_text),
            "label": labels.map(normalize_label),
            "url": urls.map(basic_clean_text),
            "published_at": published_at.map(basic_clean_text),
        }
    )

    clean_df["source_dataset"] = dataset_name
    clean_df["source_type"] = "news"
    clean_df["text"] = clean_df.apply(lambda row: combine_title_content(row["title"], row["content"]), axis=1)
    clean_df["id"] = clean_df["text"].apply(lambda text: _stable_id(text, dataset_name))

    before_total = len(clean_df)
    clean_df = clean_df[clean_df["label"].notna()].copy()
    clean_df = clean_df[clean_df["text"].str.len() >= min_text_length].copy()
    clean_df = clean_df.drop_duplicates(subset=["text"], keep="first").copy()

    clean_df["label"] = clean_df["label"].astype(int)
    clean_df = clean_df[UNIFIED_COLUMNS].reset_index(drop=True)

    logger.debug(
        "Dataset %s cleaned: before=%s, after=%s, removed=%s",
        dataset_name,
        before_total,
        len(clean_df),
        before_total - len(clean_df),
    )
    return clean_df


def _read_csv(path: Path) -> pd.DataFrame:
    for encoding in ["utf-8", "utf-8-sig", "cp1258", "latin-1"]:
        try:
            return pd.read_csv(path, encoding=encoding)
        except Exception:
            continue
    raise ValueError(f"Cannot read CSV file: {path}")


def _read_json(path: Path) -> pd.DataFrame:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            rows = [json.loads(line) for line in f if line.strip()]
        return pd.DataFrame(rows)

    if isinstance(data, list):
        return pd.DataFrame(data)
    if isinstance(data, dict):
        return pd.DataFrame([data])
    return pd.DataFrame({"content": [str(data)]})


def _read_txt(path: Path) -> pd.DataFrame:
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        lines = [line.strip() for line in f if line.strip()]
    return pd.DataFrame({"content": lines, "label": [None] * len(lines)})


def read_file_to_dataframe(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return _read_csv(path)
    if suffix == ".json":
        return _read_json(path)
    if suffix == ".txt":
        return _read_txt(path)
    raise ValueError(f"Unsupported format for file {path}")


def discover_data_files(root_dir: Path) -> list[Path]:
    patterns = ["**/*.csv", "**/*.json", "**/*.txt"]
    files: list[Path] = []
    for pattern in patterns:
        files.extend(root_dir.glob(pattern))
    ignored_parts = {".git", "Dictionaries", "Tools", "__MACOSX"}
    if os.getenv("INCLUDE_VIFACTCHECK", "0").strip().lower() not in {"1", "true", "yes"}:
        ignored_parts.add("vifactcheck")
    return sorted({path for path in files if not ignored_parts.intersection(path.parts)})


def split_dataset(
    full_df: pd.DataFrame,
    val_size: float,
    test_size: float,
    random_state: int,
    time_aware: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if full_df.empty:
        raise ValueError("Input dataframe is empty.")

    if time_aware and full_df["published_at"].astype(str).str.strip().ne("").any():
        time_df = full_df.copy()
        time_df["published_at"] = pd.to_datetime(time_df["published_at"], errors="coerce")
        time_df = time_df.sort_values("published_at", na_position="last").reset_index(drop=True)
        n = len(time_df)
        n_test = max(1, int(round(n * test_size)))
        n_val = max(1, int(round(n * val_size)))
        test_df = time_df.iloc[-n_test:].copy()
        val_df = time_df.iloc[-(n_test + n_val):-n_test].copy()
        train_df = time_df.iloc[: -(n_test + n_val)].copy()
        return train_df, val_df, test_df

    train_df, temp_df = train_test_split(
        full_df,
        test_size=(val_size + test_size),
        stratify=full_df["label"],
        random_state=random_state,
    )
    val_fraction_of_temp = val_size / (val_size + test_size)
    val_df, test_df = train_test_split(
        temp_df,
        test_size=(1 - val_fraction_of_temp),
        stratify=temp_df["label"],
        random_state=random_state,
    )
    return train_df, val_df, test_df


def build_dataset_profile(
    full_df: pd.DataFrame,
    train_df: pd.DataFrame,
    val_df: pd.DataFrame,
    test_df: pd.DataFrame,
    duplicate_ratio_removed: float,
) -> str:
    def _len_stats(df: pd.DataFrame) -> dict[str, float]:
        lengths = df["text"].str.len()
        return {
            "min": float(lengths.min()) if not lengths.empty else 0,
            "mean": float(lengths.mean()) if not lengths.empty else 0,
            "max": float(lengths.max()) if not lengths.empty else 0,
        }

    lines = [
        "# Dataset Profile",
        "",
        "## Split Sizes",
        f"- train: {len(train_df)}",
        f"- val: {len(val_df)}",
        f"- test: {len(test_df)}",
        "",
        "## Label Distribution (full)",
    ]
    label_counts = full_df["label"].value_counts(dropna=False).to_dict()
    for k, v in label_counts.items():
        lines.append(f"- label {k}: {v}")

    lines.extend(
        [
            "",
            "## Text Length Stats",
            f"- train: {_len_stats(train_df)}",
            f"- val: {_len_stats(val_df)}",
            f"- test: {_len_stats(test_df)}",
            "",
            "## Cleaning Notes",
            f"- duplicate ratio removed: {duplicate_ratio_removed:.4f}",
            f"- minimum text length threshold: {CFG.min_text_length}",
            "- detected issues: missing labels, short texts, duplicates were removed where possible.",
        ]
    )
    return "\n".join(lines)


def make_dataset(time_aware_split: bool = False) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ensure_directories()

    files = discover_data_files(CFG.data_raw_dir)
    if not files:
        raise FileNotFoundError(f"No raw data files found in {CFG.data_raw_dir}")

    unified_dfs: list[pd.DataFrame] = []
    before_count = 0
    for file_path in files:
        try:
            raw_df = read_file_to_dataframe(file_path)
            before_count += len(raw_df)
            dataset_name = dataset_name_from_path(file_path)
            clean_df = unify_and_clean_dataframe(
                raw_df,
                dataset_name,
                min_text_length=CFG.min_text_length,
                label_hint=infer_label_from_path(file_path),
            )
            if not clean_df.empty:
                unified_dfs.append(clean_df)
        except Exception as exc:
            logger.warning("Skipping file %s due to error: %s", file_path, exc)

    if not unified_dfs:
        raise ValueError("No usable dataset found after cleaning.")

    full_df = pd.concat(unified_dfs, ignore_index=True)
    full_df = full_df.drop_duplicates(subset=["text"]).reset_index(drop=True)

    train_df, val_df, test_df = split_dataset(
        full_df,
        val_size=CFG.val_size,
        test_size=CFG.test_size,
        random_state=CFG.random_state,
        time_aware=time_aware_split,
    )

    train_df.to_csv(CFG.data_processed_dir / "train.csv", index=False, encoding="utf-8")
    val_df.to_csv(CFG.data_processed_dir / "val.csv", index=False, encoding="utf-8")
    test_df.to_csv(CFG.data_processed_dir / "test.csv", index=False, encoding="utf-8")

    duplicate_ratio_removed = max(0.0, (before_count - len(full_df)) / before_count) if before_count else 0.0
    profile = build_dataset_profile(full_df, train_df, val_df, test_df, duplicate_ratio_removed)
    (CFG.reports_dir / "dataset_profile.md").write_text(profile, encoding="utf-8")

    logger.info("Dataset prepared: train=%s val=%s test=%s", len(train_df), len(val_df), len(test_df))
    return train_df, val_df, test_df
