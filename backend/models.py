from datetime import date
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import EmailStr, conint, conlist

from enum import Enum

class PatientStatus(str, Enum):
    ACTIVE = "Active"
    DISCHARGED = "Discharged"

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class PatientBase(SQLModel):

    name: str = Field(index=True, min_length=2, max_length=100)

    dob: date = Field(description="Patient's Date of Birth") 

    gender: Gender = Field() 
    
    phone: str = Field(min_length=11, max_length=15) 
    
    email: Optional[EmailStr] = None
    
    status: PatientStatus = Field(default=PatientStatus.ACTIVE)
    

class Patient(PatientBase, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)


class PatientUpdate(SQLModel):
    name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[Gender] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[PatientStatus] = None