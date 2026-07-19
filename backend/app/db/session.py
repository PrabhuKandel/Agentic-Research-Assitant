from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings


# Engine manages the actual connection pool to PostgreSQL.
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)


# SessionLocal creates database sessions for requests and services.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """Provide one database session and close it after use."""

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()