from __future__ import annotations

import json
import logging
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

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
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return True, "downloaded"
    message = (result.stderr or result.stdout or "clone_failed").strip()
    return False, message


def _write_manual_fallback(issues: list[DownloadStatus]) -> None:
    if not issues:
        return

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
                f"  - Đích mong muốn: {issue.destination}",
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
    (CFG.project_root / "docs" / "DATASET_MANUAL.md").write_text("\n".join(lines), encoding="utf-8")


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


def download_datasets() -> list[DownloadStatus]:
    ensure_directories()
    targets = [
        ("VFND", "https://github.com/VFND/VFND-vietnamese-fake-news-datasets", CFG.data_raw_dir / "vfnd"),
        ("TALLIP", "https://github.com/Arko98/TALLIP-FakeNews-Dataset", CFG.data_raw_dir / "tallip"),
        ("Zenodo", "https://zenodo.org/records/2578917/latest", CFG.data_raw_dir / "zenodo"),
    ]

    results: list[DownloadStatus] = []
    failed: list[DownloadStatus] = []

    for dataset_name, url, dest in targets:
        if dataset_name == "Zenodo":
            status = DownloadStatus(
                dataset=dataset_name,
                source=url,
                destination=str(dest),
                status="manual_required",
                message="Zenodo latest endpoint may require browser/manual download",
                timestamp_utc=datetime.now(timezone.utc).isoformat(),
            )
            failed.append(status)
            results.append(status)
            continue

        ok, message = _run_git_clone(url, dest)
        status = DownloadStatus(
            dataset=dataset_name,
            source=url,
            destination=str(dest),
            status="ok" if ok else "failed",
            message=message,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
        )
        results.append(status)
        if not ok:
            failed.append(status)
            logger.warning("Failed to download %s: %s", dataset_name, message)

    results = _ensure_local_sample_fallback(results)

    (CFG.reports_dir / "dataset_sources.json").write_text(
        json.dumps([asdict(item) for item in results], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    _write_manual_fallback(failed)
    return results
