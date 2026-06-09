from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from database.connection import get_db
from models.meeting import Meeting, Transcript
from services.whisper_service import process_meeting_file

router = APIRouter()


class TranscribeRequest(BaseModel):
    meeting_id: str


@router.post("/transcribe")
def transcribe_meeting(body: TranscribeRequest, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == uuid.UUID(body.meeting_id)).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    if not meeting.file_path:
        raise HTTPException(status_code=400, detail="No file associated with this meeting")

    meeting.status = "transcribing"
    db.commit()

    try:
        result = process_meeting_file(meeting.file_path)
    except Exception as e:
        meeting.status = "error"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

    transcript = Transcript(
        meeting_id=meeting.id,
        full_text=result["text"],
        language=result.get("language", "unknown"),
    )
    db.add(transcript)
    meeting.status = "transcribed"
    db.commit()
    db.refresh(transcript)

    return {
        "meeting_id": body.meeting_id,
        "transcript_id": str(transcript.id),
        "text": result["text"],
        "language": result.get("language"),
    }


@router.get("/meetings")
def list_meetings(db: Session = Depends(get_db)):
    meetings = db.query(Meeting).order_by(Meeting.created_at.desc()).all()
    return [
        {
            "id": str(m.id),
            "title": m.title,
            "status": m.status,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        for m in meetings
    ]


@router.get("/meetings/{meeting_id}")
def get_meeting(meeting_id: str, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == uuid.UUID(meeting_id)).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    result = {
        "id": str(meeting.id),
        "title": meeting.title,
        "status": meeting.status,
        "created_at": meeting.created_at.isoformat() if meeting.created_at else None,
        "transcript": None,
        "summary": None,
    }

    if meeting.transcript:
        result["transcript"] = {
            "text": meeting.transcript.full_text,
            "language": meeting.transcript.language,
        }

    if meeting.summary:
        result["summary"] = {
            "summary": meeting.summary.summary,
            "action_items": meeting.summary.action_items,
            "decisions": meeting.summary.decisions,
            "key_points": meeting.summary.key_points,
        }

    return result