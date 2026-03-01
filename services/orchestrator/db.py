from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from common.settings import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()


def _build_engine():
    try:
        return create_engine(settings.database_url, future=True, pool_pre_ping=True)
    except ModuleNotFoundError:
        fallback_url = "sqlite+pysqlite:///./data/agentic.db"
        return create_engine(fallback_url, future=True, pool_pre_ping=True)


engine = _build_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def init_db() -> None:
    from services.orchestrator import models  # noqa: F401

    Base.metadata.create_all(bind=engine)


@contextmanager
def session_scope() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
