from pydantic import BaseModel
from typing import Optional

class PatientBase(BaseModel):
    name: str
    age: int
    medical_history: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientInDB(PatientBase):
    id: Optional[str]

class PatientResponse(PatientInDB):
    pass