from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Boolean, DateTime, JSON, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class User(Base):
    """User model for authentication and authorization."""
    __tablename__ = "users"
    
    # GitHub OAuth fields
    github_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True, index=True, nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    
    # Auth fields
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    candidate_sessions: Mapped[List["InterviewSession"]] = relationship(
        "InterviewSession", 
        foreign_keys="InterviewSession.candidate_id",
        back_populates="candidate"
    )
    interviewer_sessions: Mapped[List["InterviewSession"]] = relationship(
        "InterviewSession", 
        foreign_keys="InterviewSession.interviewer_id", 
        back_populates="interviewer"
    )
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"
    
    @property
    def is_authenticated(self) -> bool:
        return self.is_active
    
    def update_last_login(self) -> None:
        """Update the last login timestamp."""
        self.last_login = datetime.now(timezone.utc)
