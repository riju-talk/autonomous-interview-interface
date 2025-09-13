from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from sqlalchemy import String, Enum as SQLEnum, Integer, ForeignKey, JSON, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class QuestionType(str, Enum):
    OBJECTIVE = "objective"
    MULTI_TURN = "multi_turn"
    ASSIGNMENT = "assignment"

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class InterviewSessionStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class InterviewSession(Base):
    """Represents an interview session for a user."""
    __tablename__ = "interview_sessions"
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    status: Mapped[InterviewSessionStatus] = mapped_column(
        SQLEnum(InterviewSessionStatus),
        default=InterviewSessionStatus.CREATED,
        nullable=False
    )
    current_question_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    difficulty: Mapped[DifficultyLevel] = mapped_column(
        SQLEnum(DifficultyLevel),
        default=DifficultyLevel.EASY,
        nullable=False
    )
    score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    feedback: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="sessions")
    responses: Mapped[List["InterviewResponse"]] = relationship(
        "InterviewResponse", 
        back_populates="session",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<InterviewSession {self.id} - {self.status}>"

class Question(Base):
    """Question bank for interview questions."""
    __tablename__ = "questions"
    
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    difficulty: Mapped[DifficultyLevel] = mapped_column(
        SQLEnum(DifficultyLevel),
        nullable=False,
        index=True
    )
    question_type: Mapped[QuestionType] = mapped_column(
        SQLEnum(QuestionType),
        nullable=False,
        index=True
    )
    prompt: Mapped[str] = mapped_column(String(2000), nullable=False)
    options: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    correct_answer: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    explanation: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    metadata_: Mapped[Optional[Dict[str, Any]]] = mapped_column("metadata", JSON, nullable=True)
    
    def __repr__(self) -> str:
        return f"<Question {self.id} - {self.category} - {self.difficulty}>"

class InterviewResponse(Base):
    """Stores user responses to interview questions."""
    __tablename__ = "interview_responses"
    
    session_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    question_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("questions.id"),
        nullable=False,
        index=True
    )
    user_answer: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    is_correct: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    feedback: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    processing_time: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # in seconds
    
    # Relationships
    session: Mapped[InterviewSession] = relationship("InterviewSession", back_populates="responses")
    question: Mapped[Question] = relationship("Question")
    
    def __repr__(self) -> str:
        return f"<InterviewResponse {self.id} - Session {self.session_id} - Q{self.question_id}>"
