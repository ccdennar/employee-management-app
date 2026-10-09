from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from app.models.employee import EmploymentStatus

class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100, description="Employee first name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Employee last name")
    email: EmailStr = Field(..., description="Employee email address")
    department: str = Field(..., min_length=1, max_length=100, description="Department name")
    job_title: str = Field(..., min_length=1, max_length=200, description="Job title")
    salary: float = Field(..., gt=0, description="Annual salary must be positive")
    employment_status: EmploymentStatus = Field(default=EmploymentStatus.ACTIVE)

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    department: Optional[str] = Field(None, min_length=1, max_length=100)
    job_title: Optional[str] = Field(None, min_length=1, max_length=200)
    salary: Optional[float] = Field(None, gt=0)
    employment_status: Optional[EmploymentStatus] = None

class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    detail: str
    status_code: int