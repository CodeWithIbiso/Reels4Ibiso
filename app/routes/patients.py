from fastapi import APIRouter, HTTPException
from models.patient import PatientCreate, PatientResponse
from connections.database import database

router = APIRouter()
patients_collection = database.get_collection("patients")

@router.post("/", response_model=PatientResponse)
async def create_patient(patient: PatientCreate):
    patient_dict = patient.dict()
    result = await patients_collection.insert_one(patient_dict)
    patient_dict["id"] = str(result.inserted_id)
    return patient_dict

@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: str):
    patient = await patients_collection.find_one({"_id": patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient