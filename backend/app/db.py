"""Database engine, session factory and declarative base.

Production uses PostgreSQL (see config.Settings.database_url). Tests override
DATABASE_URL to SQLite so the test-suite runs without external services.
"""
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from .config import settings


class Base(DeclarativeBase):
    """Declarative base for all SQLAlchemy models."""


def _create_engine(database_url: str):
    kwargs = {"pool_pre_ping": True}
    if database_url.startswith("sqlite"):
        # SQLite requires a shared connection when used from FastAPI threads
        # and an in-memory database; pin the pool to a single connection.
        kwargs["connect_args"] = {"check_same_thread": False}
        if database_url == "sqlite:///:memory:":
            kwargs["poolclass"] = StaticPool
    return create_engine(database_url, **kwargs)


engine = _create_engine(settings.database_url)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a request-scoped database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create all tables on startup.

    A lightweight approach is enough for the prototype; switch to Alembic
    migrations once the schema stabilizes and before any deployment.
    """
    # Import models so SQLAlchemy registers all tables in the metadata.
    from . import models  # noqa: F401

    Base.metadata.create_all(bind=engine)