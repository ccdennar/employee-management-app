import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    # ✅ Explicit stderr write + flush ensures visibility in K8s
    print("FATAL: DATABASE_URL environment variable is not set", file=sys.stderr, flush=True)
    sys.exit(1)

try:
    engine = create_engine(DATABASE_URL)
except Exception as e:
    print(f"FATAL: Invalid DATABASE_URL: {e}", file=sys.stderr, flush=True)
    sys.exit(1)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()