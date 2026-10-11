from fastapi import FastAPI
from sqlalchemy import text
from app.api import employees
from app.database import engine, Base

# ✅ REMOVED: Base.metadata.create_all(bind=engine) 
# This was causing immediate crash loops in K8s when DB wasn't ready at import time.

app = FastAPI(
    title="Employee Management API",
    description="API for managing employee records",
    version="1.0.0"
)

app.include_router(employees.router)

@app.on_event("startup")
async def startup_event():
    """Retry DB connection and schema creation on startup.
    
    Critical for K8s: Pods often start before PostgreSQL is fully ready.
    This prevents CrashLoopBackOff by waiting up to 60 seconds.
    """
    import time
    
    print("⏳ Waiting for database to be ready...")
    for i in range(30):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            # Only create tables AFTER we know DB is reachable
            Base.metadata.create_all(engine)
            print(f"✅ Database connected and schema created after {i+1} attempts")
            return
            
        except Exception as e:
            print(f"⏳ Waiting for database... ({i+1}/30): {e}")
            time.sleep(2)
    
    raise RuntimeError("Could not connect to database after 30 retries (60s)")

@app.get("/health/live")
def health_check():
    return {"status": "healthy"}

@app.get("/health/ready")
def readiness_check():
    # Add database connectivity check here in production
    return {"status": "ready"}