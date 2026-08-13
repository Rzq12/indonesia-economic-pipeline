import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


def _get_database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if url:
        return url
    return (
        f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
        f"@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
    )


_engine = None
_SessionLocal = None


def _init_engine():
    global _engine, _SessionLocal
    if _engine is None:
        url = _get_database_url()
        connect_args = {}
        if "DATABASE_URL" in os.environ:
            # Managed Postgres (Supabase/Neon) requires SSL
            connect_args["sslmode"] = "require"
        _engine = create_engine(url, pool_size=5, max_overflow=10, connect_args=connect_args)
        _SessionLocal = sessionmaker(bind=_engine)


def get_session() -> Session:
    _init_engine()
    assert _SessionLocal is not None
    return _SessionLocal()