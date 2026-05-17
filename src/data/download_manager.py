from __future__ import annotations

import json
import logging
import os
import subprocess
from io import BytesIO
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

from src.utils.config import CFG, ensure_directories

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class DownloadStatus:
    dataset: str
    source: str
    destination: str
    status: str
    message: str
    timestamp_utc: str


def _run_git_clone(url: str, dest: Path) -> tuple[bool, str]:
    if dest.exists() and any(dest.iterdir()):
        return True, "already_present"

    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["git", "clone", "--depth", "1", url, str(dest)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode == 0:
        return True, "downloaded"
    message = (result.stderr or result.stdout or "clone_failed").strip()
    return False, message


def _write_manual_fallback(issues: list[DownloadStatus]) -> None:
    if not issues:
        return

    def _display_destination(destination: str) -> str:
        try:
            return str(Path(destination).resolve().relative_to(CFG.project_root))
        except ValueError:
            return destination

    lines = [
        "# Dataset Manual Download Guide",
        "",
        "Các nguồn không tải tự động được. Hãy tải thủ công và đặt vào `data/raw/<dataset_name>/`.",
        "",
        "## Danh sách lỗi",
    ]
    for issue in issues:
        lines.extend(
            [
                f"- Dataset: {issue.dataset}",
                f"  - URL: {issue.source}",
                f"  - Lỗi: {issue.message}",
                f"  - Đích mong muốn: {_display_destination(issue.destination)}",
            ]
        )

    lines.extend(
        [
            "",
            "## Bước thủ công",
            "1. Tải file/clone repo từ URL tương ứng.",
            "2. Giải nén nếu cần và đặt vào thư mục `data/raw/` theo tên dataset.",
            "3. Chạy lại `make prepare`.",
            "4. Kiểm tra `reports/dataset_sources.json` để xác nhận trạng thái.",
        ]
    )
    (CFG.reports_dir / "dataset_manual.md").write_text("\n".join(lines), encoding="utf-8")


def _ensure_local_sample_fallback(results: list[DownloadStatus]) -> list[DownloadStatus]:
    has_ok_source = any(item.status == "ok" for item in results)
    sample_dir = CFG.data_raw_dir / "fallback_sample"
    sample_file = sample_dir / "sample_news.csv"

    if has_ok_source and sample_file.exists():
        return results
    if has_ok_source:
        return results

    sample_dir.mkdir(parents=True, exist_ok=True)
    sample_df = pd.DataFrame(
        [
            {
                "title": "Chính phủ công bố số liệu kinh tế quý mới",
                "content": "Nguồn chính thống công bố thống kê chi tiết và minh bạch.",
                "label": "real",
                "url": "https://example.org/real-1",
                "published_at": "2025-01-01",
            },
            {
                "title": "Tin lan truyền chưa kiểm chứng về y tế",
                "content": "Bài viết thiếu nguồn xác thực và có dấu hiệu giật tít.",
                "label": "fake",
                "url": "https://example.org/fake-1",
                "published_at": "2025-01-02",
            },
            {
                "title": "Bản tin chính thức từ cơ quan chức năng",
                "content": "Thông tin được đối chiếu từ nhiều nguồn báo chí uy tín.",
                "label": "real",
                "url": "https://example.org/real-2",
                "published_at": "2025-01-03",
            },
            {
                "title": "Bài đăng ẩn danh khẳng định sai sự thật",
                "content": "Không có bằng chứng đi kèm, nội dung gây hiểu nhầm.",
                "label": "fake",
                "url": "https://example.org/fake-2",
                "published_at": "2025-01-04",
            },
            {
                "title": "Phân tích dữ liệu từ báo cáo công khai",
                "content": "Bài viết có trích dẫn tài liệu đầy đủ và kiểm chứng được.",
                "label": "real",
                "url": "https://example.org/real-3",
                "published_at": "2025-01-05",
            },
            {
                "title": "Tin đồn thất thiệt về thị trường",
                "content": "Nội dung dùng ngôn ngữ kích động, không dẫn nguồn đáng tin.",
                "label": "fake",
                "url": "https://example.org/fake-3",
                "published_at": "2025-01-06",
            },
        ]
    )
    sample_df.to_csv(sample_file, index=False, encoding="utf-8")

    results.append(
        DownloadStatus(
            dataset="LOCAL_SAMPLE",
            source="generated",
            destination=str(sample_file),
            status="ok",
            message="generated_local_fallback_sample",
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
        )
    )
    return results


def _download_vifactcheck() -> DownloadStatus:
    dataset_name = "ViFactCheck"
    dest_dir = CFG.data_raw_dir / "vifactcheck"
    dest_file = dest_dir / "vifactcheck.csv"
    source = "https://huggingface.co/datasets/tranthaihoa/vifactcheck"

    if dest_file.exists():
        return DownloadStatus(
            dataset=dataset_name,
            source=source,
            destination=str(dest_file),
            status="ok",
            message="already_present",
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
        )

    parquet_urls = [
        "https://huggingface.co/datasets/tranthaihoa/vifactcheck/resolve/main/data/train-00000-of-00001.parquet",
        "https://huggingface.co/datasets/tranthaihoa/vifactcheck/resolve/main/data/dev-00000-of-00001.parquet",
        "https://huggingface.co/datasets/tranthaihoa/vifactcheck/resolve/main/data/test-00000-of-00001.parquet",
    ]

    try:
        frames = []
        for url in parquet_urls:
            response = requests.get(url, timeout=120)
            response.raise_for_status()
            frames.append(pd.read_parquet(BytesIO(response.content)))
        raw = pd.concat(frames, ignore_index=True)
        label_map = {0: "real", 1: "fake", 2: "misleading"}
        converted = pd.DataFrame(
            {
                "title": raw.get("Statement", "").fillna("").astype(str),
                "content": (
                    raw.get("Context", "").fillna("").astype(str)
                    + " "
                    + raw.get("Evidence", "").fillna("").astype(str)
                ),
                "label": raw.get("labels", "").map(label_map),
                "url": raw.get("Url", "").fillna("").astype(str),
                "published_at": "",
            }
        )
        dest_dir.mkdir(parents=True, exist_ok=True)
        converted.to_csv(dest_file, index=False, encoding="utf-8")
        return DownloadStatus(
            dataset=dataset_name,
            source=source,
            destination=str(dest_file),
            status="ok",
            message=f"downloaded_and_converted_{len(converted)}_rows",
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
        )
    except Exception as exc:
        return DownloadStatus(
            dataset=dataset_name,
            source=source,
            destination=str(dest_file),
            status="manual_required",
            message=f"Could not download Hugging Face parquet automatically: {exc}",
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
        )


def download_datasets() -> list[DownloadStatus]:
    ensure_directories()
    targets = [
        (
            "VFND",
            [
                "https://github.com/VFND/VFND-vietnamese-fake-news-datasets",
                "https://github.com/VFND/VFND-vietnamese-fake-news-datasets.git",
            ],
            CFG.data_raw_dir / "vfnd",
        ),
        (
            "TALLIP",
            [
                "https://github.com/Arko98/TALLIP-FakeNews-Dataset",
                "https://github.com/Arko98/TALLIP-FakeNews-Dataset.git",
            ],
            CFG.data_raw_dir / "tallip",
        ),
        (
            "Zenodo",
            ["https://zenodo.org/records/2578917/latest"],
            CFG.data_raw_dir / "zenodo",
        ),
    ]

    results: list[DownloadStatus] = []
    failed: list[DownloadStatus] = []

    for dataset_name, urls, dest in targets:
        if dataset_name == "Zenodo":
            status = DownloadStatus(
                dataset=dataset_name,
                source=urls[0],
                destination=str(dest),
                status="manual_required",
                message="Zenodo latest endpoint may require browser/manual download",
                timestamp_utc=datetime.now(timezone.utc).isoformat(),
            )
            failed.append(status)
            results.append(status)
            continue

        ok = False
        message = "All download sources failed"
        successful_source = urls[0]
        for url in urls:
            logger.info("Trying source for %s: %s", dataset_name, url)
            ok, message = _run_git_clone(url, dest)
            if ok:
                successful_source = url
                break

        status_value = "ok" if ok else "failed"
        if ok and dataset_name == "TALLIP":
            has_direct_data = any(dest.rglob("*.csv")) or any(dest.rglob("*.json")) or any(dest.rglob("*.txt"))
            if not has_direct_data:
                status_value = "manual_required"
                message = "Repository cloned, but data files are distributed through the TALLIP zip link in README."

        status = DownloadStatus(
            dataset=dataset_name,
            source=successful_source,
            destination=str(dest),
            status=status_value,
            message=message,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
        )
        results.append(status)
        if status_value != "ok":
            failed.append(status)
            logger.warning("Failed to download %s: %s", dataset_name, message)

    include_vifactcheck = os.getenv("INCLUDE_VIFACTCHECK", "0").strip().lower() in {"1", "true", "yes"}
    if include_vifactcheck:
        vifactcheck_status = _download_vifactcheck()
        results.append(vifactcheck_status)
        if vifactcheck_status.status != "ok":
            failed.append(vifactcheck_status)
            logger.warning("Failed to download %s: %s", vifactcheck_status.dataset, vifactcheck_status.message)
    else:
        results.append(
            DownloadStatus(
                dataset="ViFactCheck",
                source="https://huggingface.co/datasets/tranthaihoa/vifactcheck",
                destination=str(CFG.data_raw_dir / "vifactcheck"),
                status="skipped",
                message="optional_fact_checking_dataset_set_INCLUDE_VIFACTCHECK=1_to_enable",
                timestamp_utc=datetime.now(timezone.utc).isoformat(),
            )
        )

    results = _ensure_local_sample_fallback(results)

    (CFG.reports_dir / "dataset_sources.json").write_text(
        json.dumps([asdict(item) for item in results], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    _write_manual_fallback(failed)
    return results
