from __future__ import annotations

import os
from pathlib import Path

try:
    from scripts._bootstrap import ensure_repo_root_on_path
except ModuleNotFoundError:
    from _bootstrap import ensure_repo_root_on_path

REPO_ROOT = ensure_repo_root_on_path(__file__)


def setup_supabase_db() -> None:
    database_url = os.getenv("SUPABASE_DB_URL")
    if not database_url:
        raise RuntimeError(
            "Missing SUPABASE_DB_URL. Use a PostgreSQL connection string from Supabase Database Settings."
        )

    try:
        import psycopg2
    except ImportError as exc:
        raise RuntimeError("Missing psycopg2-binary. Run: python3 -m pip install -r requirements.txt") from exc

    sql_path = Path(REPO_ROOT) / "scripts" / "init_supabase.sql"
    sql = sql_path.read_text(encoding="utf-8")

    conn = psycopg2.connect(database_url)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                cur.execute(
                    """
                    select table_name
                    from information_schema.tables
                    where table_schema = 'public'
                      and table_name in ('predictions', 'feedback')
                    order by table_name
                    """
                )
                tables = [row[0] for row in cur.fetchall()]
                print(f"Supabase schema ready: {', '.join(tables)}")
    finally:
        conn.close()


if __name__ == "__main__":
    setup_supabase_db()
