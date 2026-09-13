from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_size=20,
    max_overflow=0,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Database session dependency for FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
