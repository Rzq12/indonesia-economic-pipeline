import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.load.models import Base


@pytest.fixture(scope="session")
def engine():
    db_url = os.environ.get("TEST_DATABASE_URL", "sqlite:///test.db")
    eng = create_engine(db_url)
    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)


@pytest.fixture
def session(engine):
    Session = sessionmaker(bind=engine)
    sess = Session()
    yield sess
    sess.rollback()
    sess.close()