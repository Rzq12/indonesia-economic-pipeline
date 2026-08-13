"""Apply schema SQL files to the target database. Idempotent-safe: uses IF NOT EXISTS semantics via ON CONFLICT-friendly DDL is not applied here; this mirrors docker-entrypoint-initdb.d for non-Docker hosts (Supabase)."""
import os

from sqlalchemy import text

from src.load.database import get_session

SCHEMA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sql")
FILES = ["001_create_schema.sql", "002_create_indexes.sql"]


def main() -> None:
    session = get_session()
    try:
        for fname in FILES:
            path = os.path.join(SCHEMA_DIR, fname)
            with open(path) as f:
                sql = f.read()
            session.execute(text(sql))
            session.commit()
            print(f"Applied {fname}")
    finally:
        session.close()


if __name__ == "__main__":
    main()