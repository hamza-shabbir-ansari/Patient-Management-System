from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import date

from database import create_db_and_tables, get_session
from models import Patient, PatientBase, PatientUpdate, PatientStatus, Gender

app = FastAPI(
    title="Patient Management System API",
    description="Professional backend for managing patient records.",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():

    create_db_and_tables()


@app.post("/patients/", response_model=Patient)
def create_patient(patient: PatientBase, session: Session = Depends(get_session)):
    db_patient = Patient.model_validate(patient)
    session.add(db_patient)
    session.commit()
    session.refresh(db_patient)
    return db_patient

@app.get("/patients/", response_model=List[Patient])
def read_patients(

    status: Optional[PatientStatus] = Query(None, description="Filter by Patient Status"),

    gender: Optional[Gender] = Query(None, description="Filter by Patient Gender"),
    
    name: Optional[str] = Query(None, description="Search by Patient Name"),
    session: Session = Depends(get_session)
):
    query = select(Patient)
    
    if status:
        query = query.where(Patient.status == status)
        
    if gender:
        query = query.where(Patient.gender == gender)
        
    if name:
        query = query.where(Patient.name.ilike(f"%{name}%"))
        
    patients = session.exec(query).all()
    return patients

@app.get("/patients/{patient_id}", response_model=Patient)
def read_patient_by_id(patient_id: int, session: Session = Depends(get_session)):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.put("/patients/{patient_id}", response_model=Patient)
def update_patient(
    patient_id: int, 
    patient_data: PatientUpdate, 
    session: Session = Depends(get_session)
):
    db_patient = session.get(Patient, patient_id)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    update_data = patient_data.model_dump(exclude_unset=True)
    
    db_patient.sqlmodel_update(update_data)
    
    session.add(db_patient)
    session.commit()
    session.refresh(db_patient)
    return db_patient

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, session: Session = Depends(get_session)):
    patient = session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    session.delete(patient)
    session.commit()
    return {"ok": True}