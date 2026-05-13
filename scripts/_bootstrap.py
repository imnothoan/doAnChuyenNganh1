from __future__ import annotations

import sys
from pathlib import Path


def ensure_repo_root_on_path(script_file: str | Path) -> Path:
    script_path = Path(script_file).resolve()
    for candidate in [script_path.parent, *script_path.parents]:
        if (candidate / ".git").exists() or (candidate / "src").is_dir():
            repo_root = candidate
            break
    else:
        repo_root = script_path.parent
    repo_root_str = str(repo_root)
    if repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)
    return repo_root
