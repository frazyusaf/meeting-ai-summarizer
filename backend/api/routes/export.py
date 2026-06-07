from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
import uuid

from database.connection import get_db
from models.meeting import Meeting
from services.export_service import generate_pdf, generate_docx, generate_txt

router = APIRouter()

EXPORT_FORMATS = {"pdf", "docx", "txt"}


@router.get("/export/{meeting_id}")
def export_meeting(
    meeting_id: str,
    format: str = "pdf",
    db: Session = Depends(get_db),
):
    if format not in EXPORT_FORMATS:
        raise HTTPException(status_code=400, detail=f"Invalid format. Choose: {', '.join(EXPORT_FORMATS)}")

    meeting = db.query(Meeting).filter(Meeting.id == uuid.UUID(meeting_id)).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    if not meeting.summary:
        raise HTTPException(status_code=400, detail="Meeting has not been summarized yet")

    meeting_data = {
        "summary": meeting.summary.summary,
        "action_items": meeting.summary.action_items or [],
        "decisions": meeting.summary.decisions or [],
        "key_points": meeting.summary.key_points or [],
    }
    title = meeting.title or "Meeting Summary"

    if format == "pdf":
        content = generate_pdf(meeting_data, title)
        media_type = "application/pdf"
        filename = f"{title.replace(' ', '_')}.pdf"

    elif format == "docx":
        content = generate_docx(meeting_data, title)
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        filename = f"{title.replace(' ', '_')}.docx"

    else:  # txt
        content = generate_txt(meeting_data, title)
        media_type = "text/plain"
        filename = f"{title.replace(' ', '_')}.txt"

    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
