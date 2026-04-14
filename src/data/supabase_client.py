from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.utils.config import CFG


class SupabaseClient:
    def __init__(self) -> None:
        self.url = os.getenv("SUPABASE_URL", "")
        self.key = os.getenv("SUPABASE_KEY", "")
        self.enabled = bool(self.url and self.key)
        self.local_store = CFG.data_processed_dir / "supabase_fallback.jsonl"

        self._client = None
        if self.enabled:
            try:
                from supabase import create_client

                self._client = create_client(self.url, self.key)
            except Exception:
                self.enabled = False

    def insert_prediction(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = {**payload, "created_at": datetime.now(timezone.utc).isoformat()}
        if self.enabled and self._client is not None:
            return self._client.table("predictions").insert(payload).execute().data
        self.local_store.parent.mkdir(parents=True, exist_ok=True)
        with self.local_store.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"table": "predictions", "data": payload}, ensure_ascii=False) + "\n")
        return payload

    def insert_feedback(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = {**payload, "created_at": datetime.now(timezone.utc).isoformat()}
        if self.enabled and self._client is not None:
            return self._client.table("feedback").insert(payload).execute().data
        self.local_store.parent.mkdir(parents=True, exist_ok=True)
        with self.local_store.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"table": "feedback", "data": payload}, ensure_ascii=False) + "\n")
        return payload

    def list_predictions(self, limit: int = 50) -> list[dict[str, Any]]:
        if self.enabled and self._client is not None:
            return self._client.table("predictions").select("*").limit(limit).execute().data
        if not self.local_store.exists():
            return []
        rows: list[dict[str, Any]] = []
        with self.local_store.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    if item.get("table") == "predictions":
                        rows.append(item.get("data", {}))
        return rows[-limit:]
