from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from database.connection import get_db
from models.meeting import Meeting, Summary
from services.gpt_service import summarize_transcript

router = APIRouter()


class SummarizeRequest(BaseModel):
    meeting_id: str


@router.post("/summarize")
def summarize_meeting(body: SummarizeRequest, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == uuid.UUID(body.meeting_id)).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    if not meeting.transcript:
        raise HTTPException(status_code=400, detail="Meeting has not been transcribed yet")

    meeting.status = "summarizing"
    db.commit()

    try:
        result = summarize_transcript(
            transcript=meeting.transcript.full_text,
            meeting_title=meeting.title,
        )
    except Exception as e:
        meeting.status = "error"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")

    # Upsert summary
    if meeting.summary:
        meeting.summary.summary = result["summary"]
        meeting.summary.action_items = result["action_items"]
        meeting.summary.decisions = result["decisions"]
        meeting.summary.key_points = result["key_points"]
    else:
        summary = Summary(
            meeting_id=meeting.id,
            summary=result["summary"],
            action_items=result["action_items"],
            decisions=result["decisions"],
            key_points=result["key_points"],
        )
        db.add(summary)

    meeting.status = "done"
    db.commit()

    return {
        "meeting_id": body.meeting_id,
        "summary": result["summary"],
        "action_items": result["action_items"],
        "decisions": result["decisions"],
        "key_points": result["key_points"],
    }
