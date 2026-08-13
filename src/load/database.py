import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


def _get_database_url() -> str:
    return (
        f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
        f"@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
    )


_engine = None
_SessionLocal = None


def _init_engine():
    global _engine, _SessionLocal
    if _engine is None:
        _engine = create_engine(_get_database_url(), pool_size=5, max_overflow=10)
        _SessionLocal = sessionmaker(bind=_engine)


def get_session() -> Session:
    _init_engine()
    assert _SessionLocal is not None
    return _SessionLocal()