from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import shutil
import os
import uuid

from database.connection import get_db
from models.meeting import Meeting

router = APIRouter()

UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {".mp3", ".wav", ".mp4"}
MAX_FILE_SIZE_MB = 100


@router.post("/upload")
async def upload_meeting(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    file_id = str(uuid.uuid4())
    save_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Stream file to disk
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    file_size_mb = os.path.getsize(save_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        os.remove(save_path)
        raise HTTPException(status_code=413, detail=f"File too large. Max size: {MAX_FILE_SIZE_MB}MB")

    # Create a meeting record
    title = os.path.splitext(file.filename)[0].replace("_", " ").replace("-", " ").title()
    meeting = Meeting(title=title, file_path=save_path, status="uploaded")
    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    return {
        "meeting_id": str(meeting.id),
        "file_id": file_id,
        "filename": file.filename,
        "file_size_mb": round(file_size_mb, 2),
        "status": "uploaded",
    }
