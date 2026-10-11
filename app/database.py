import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# ✅ CRITICAL: Read DATABASE_URL directly from env, NO fallback to localhost
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL environment variable is not set. "
        "This must be configured in K8s/Docker, NOT defaulted to localhost."
    )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ REQUIRED: Dependency injection for FastAPI routes
def get_db() -> Session:
    """Yield a DB session for each request and ensure cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()