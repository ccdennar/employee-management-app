from fastapi import FastAPI
from app.api import employees
from app.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management API",
    description="API for managing employee records",
    version="1.0.0"
)

app.include_router(employees.router)

@app.get("/health/live")
def health_check():
    return {"status": "healthy"}

@app.get("/health/ready")
def readiness_check():
    # Add database connectivity check here in production
    return {"status": "ready"}