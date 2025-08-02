from fastapi import APIRouter, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from typing import List
from pathlib import Path
from utils.storage import save_to_storage, read_storage
import uuid
from utils.thumbnail import generate_thumbnail

router = APIRouter()

UPLOAD_DIRECTORY = Path("uploads")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

@router.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    uploaded_files_info = []
    existing_files = read_storage().get("uploads", [])

    for file in files:
        if any(upload["filename"] == file.filename for upload in existing_files):
            continue
        file_id = str(uuid.uuid4())
        file_path = UPLOAD_DIRECTORY / file.filename
        with file_path.open("wb") as buffer:
            buffer.write(await file.read())

        thumbnail_path = generate_thumbnail(file_path)

        file_info = {
            "id": file_id,
            "filename": file.filename,
            "content_type": file.content_type,
            "size": file_path.stat().st_size,
            "path": str(file_path),
            "thumbnail": thumbnail_path
        }
        uploaded_files_info.append(file_info)

    if len(uploaded_files_info):
        save_to_storage(uploaded_files_info)

    return {"detail": "Files uploaded successfully!" if len(uploaded_files_info) else "Files already exist"}

@router.get("/uploaded-files/")
async def list_uploaded_files():
    data = read_storage()
    uploads = data.get("uploads", [])
    files_info = [
        {
            "id": upload["id"],
            "name": upload["filename"],
            "content_type": upload["content_type"],
            "url": f"/api/files/{upload['id']}",
            "thumbnail": f"/api/thumbnails/{upload['id']}"
        }
        for upload in uploads
    ]
    return JSONResponse(content={"files": files_info})

@router.get("/files/{file_id}")
async def get_file(file_id: str):
    data = read_storage()
    uploads = data.get("uploads", [])
    file_info = next((upload for upload in uploads if upload["id"] == file_id), None)
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_info["path"])

@router.get("/thumbnails/{file_id}")
async def get_thumbnail(file_id: str):
    data = read_storage()
    uploads = data.get("uploads", [])
    file_info = next((upload for upload in uploads if upload["id"] == file_id), None)
    if not file_info or not file_info.get("thumbnail"):
        raise HTTPException(status_code=404, detail="Thumbnail not found")
    return FileResponse(file_info["thumbnail"])

@router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    data = read_storage()
    uploads = data.get("uploads", [])
    file_info = next((upload for upload in uploads if upload["id"] == file_id), None)

    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        Path(file_info["path"]).unlink(missing_ok=True)
        if file_info.get("thumbnail"):
            Path(file_info["thumbnail"]).unlink(missing_ok=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

    updated_uploads = [upload for upload in uploads if upload["id"] != file_id]
    save_to_storage(updated_uploads)

    return JSONResponse(content={"detail": "File deleted successfully"}, status_code=status.HTTP_200_OK)
