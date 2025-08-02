from fastapi import APIRouter, HTTPException
from models.practice import PracticeCreate, PracticeResponse
from connections.database import database

router = APIRouter()
practices_collection = database.get_collection("practices")

@router.post("/", response_model=PracticeResponse)
async def create_practice(practice: PracticeCreate):
    practice_dict = practice.dict()
    result = await practices_collection.insert_one(practice_dict)
    practice_dict["id"] = str(result.inserted_id)
    return practice_dict

@router.get("/{practice_id}", response_model=PracticeResponse)
async def get_practice(practice_id: str):
    practice = await practices_collection.find_one({"_id": practice_id})
    if not practice:
        raise HTTPException(status_code=404, detail="Practice not found")
    return practice