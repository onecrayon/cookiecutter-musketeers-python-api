"""Standard pytest fixtures used across all API tests"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

import api.main
# `models` is necessary to ensure that AlchemyBase is properly populated
from api import models
from api.environment import ApplicationSettings


@pytest.fixture(scope="session", autouse=True)
def session_local(monkeypatch):
    """Override the default database with our testing database, and make sure to run migrations"""
    settings = ApplicationSettings()
    test_engine = create_engine(
        (
            f"postgresql+psycopg2://{settings.postgres_user}:{settings.postgres_password}"
            f"@{settings.postgres_host}:{settings.postgres_port}/test"
        ),
        echo=False,
    )
    # Drop database and recreate to ensure tests are always run against a clean slate
    if database_exists(test_engine.url):
        drop_database(test_engine.url)
    create_database(test_engine.url)
    # Monkeypatch our test session into the main application
    TestSessionLocal = sessionmaker(bind=test_engine)
    monkeypatch.setattr(api.main, 'SessionLocal', TestSessionLocal)
    # Create all tables
    api.main.AlchemyBase.metadata.create_all(bind=test_engine)
    try:
        yield TestSessionLocal
    finally:
        drop_database(test_engine.url)


@pytest.fixture(scope="function")
def session(session_local: Session, monkeypatch) -> Session:
    """Return an SQLAlchemy session for this test"""
    session = session_local()
    session.begin_nested()
    # Overwrite commits with flushes so that we can query stuff, but it's in the same transaction
    monkeypatch.setattr(session, "commit", session.flush)
    try:
        yield session
    finally:
        session.rollback()
        session.close()
