from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import uuid

from database.connection import get_db
from models.meeting import Meeting, Transcript
from services.whisper_service import process_meeting_file

router = APIRouter()


class TranscribeRequest(BaseModel):
    meeting_id: str


def get_meeting_for_session(meeting_id: str, session_id: Optional[str], db: Session):
    """Get meeting only if it belongs to this session."""
    meeting = db.query(Meeting).filter(Meeting.id == uuid.UUID(meeting_id)).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    # If meeting has a session_id, verify it matches
    if meeting.session_id and session_id != meeting.session_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return meeting


@router.post("/transcribe")
def transcribe_meeting(
    body: TranscribeRequest,
    db: Session = Depends(get_db),
    x_session_id: Optional[str] = Header(None),
):
    meeting = get_meeting_for_session(body.meeting_id, x_session_id, db)

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
def list_meetings(
    db: Session = Depends(get_db),
    x_session_id: Optional[str] = Header(None),
):
    # Only return meetings belonging to this session
    query = db.query(Meeting).order_by(Meeting.created_at.desc())
    if x_session_id:
        query = query.filter(Meeting.session_id == x_session_id)
    else:
        return []

    meetings = query.all()
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
def get_meeting(
    meeting_id: str,
    db: Session = Depends(get_db),
    x_session_id: Optional[str] = Header(None),
):
    meeting = get_meeting_for_session(meeting_id, x_session_id, db)

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