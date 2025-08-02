from fastapi import APIRouter, File, UploadFile
from typing import List
import os
from pathlib import Path

router = APIRouter()

UPLOAD_DIRECTORY = Path("uploads")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

@router.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        # Construct the file path
        file_path = UPLOAD_DIRECTORY / file.filename
        # Save the file to the given path
        with file_path.open("wb") as buffer:
            buffer.write(await file.read())
    return {"detail": "Files uploaded successfully"}