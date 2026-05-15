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

    def _append_local(self, table: str, payload: dict[str, Any]) -> dict[str, Any]:
        self.local_store.parent.mkdir(parents=True, exist_ok=True)
        with self.local_store.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"table": table, "data": payload}, ensure_ascii=False) + "\n")
        return payload

    def _insert(self, table: str, payload: dict[str, Any]) -> dict[str, Any]:
        payload = {**payload, "created_at": datetime.now(timezone.utc).isoformat()}
        if self.enabled and self._client is not None:
            try:
                data = self._client.table(table).insert(payload).execute().data
                if isinstance(data, list) and data:
                    return data[0]
                return payload
            except Exception:
                self.enabled = False
        return self._append_local(table, payload)

    def insert_prediction(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._insert("predictions", payload)

    def insert_feedback(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._insert("feedback", payload)

    def list_predictions(self, limit: int = 50) -> list[dict[str, Any]]:
        if self.enabled and self._client is not None:
            try:
                return (
                    self._client.table("predictions")
                    .select("*")
                    .order("created_at", desc=True)
                    .limit(limit)
                    .execute()
                    .data
                )
            except Exception:
                self.enabled = False
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
