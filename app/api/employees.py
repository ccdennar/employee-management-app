from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.employee import Employee, EmploymentStatus
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse, ErrorResponse
from app.models.employee import Employee as EmployeeModel

router = APIRouter(prefix="/api/v1", tags=["employees"])

@router.post("/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    # Check for duplicate email
    db_employee = db.query(EmployeeModel).filter(EmployeeModel.email == employee.email).first()
    if db_employee:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Employee with email {employee.email} already exists"
        )
    
    db_employee = EmployeeModel(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {employee_id} not found"
        )
    return db_employee

@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {employee_id} not found"
        )
    
    update_data = employee.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_employee, key, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {employee_id} not found"
        )
    
    db.delete(db_employee)
    db.commit()
    return None

@router.get("/employees", response_model=List[EmployeeResponse])
def list_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = db.query(EmployeeModel).offset(skip).limit(limit).all()
    return employees