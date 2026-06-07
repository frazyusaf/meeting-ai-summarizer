from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    meetings = relationship("Meeting", back_populates="user", cascade="all, delete")


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String(255))
    file_path = Column(Text)
    status = Column(String(50), default="uploaded")
    duration_seconds = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="meetings")
    transcript = relationship("Transcript", back_populates="meeting", uselist=False, cascade="all, delete")
    summary = relationship("Summary", back_populates="meeting", uselist=False, cascade="all, delete")


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id", ondelete="CASCADE"))
    full_text = Column(Text)
    language = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    meeting = relationship("Meeting", back_populates="transcript")


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id", ondelete="CASCADE"))
    summary = Column(Text)
    action_items = Column(JSONB)
    decisions = Column(JSONB)
    key_points = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    meeting = relationship("Meeting", back_populates="summary")
