"""CRUD operations for interview-related models."""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.interview import InterviewSession, Question, InterviewResponse
from app.schemas.interview import (
    InterviewSessionCreate, InterviewSessionUpdate,
    QuestionCreate, QuestionUpdate
)


class CRUDInterviewSession(CRUDBase[InterviewSession, InterviewSessionCreate, InterviewSessionUpdate]):
    """CRUD operations for InterviewSession."""
    
    async def get_with_details(self, db: AsyncSession, *, id: int) -> Optional[InterviewSession]:
        """Get interview session with all related data."""
        result = await db.execute(
            select(InterviewSession)
            .options(
                selectinload(InterviewSession.candidate),
                selectinload(InterviewSession.interviewer),
                selectinload(InterviewSession.responses),
                selectinload(InterviewSession.questions)
            )
            .filter(InterviewSession.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_with_questions(self, db: AsyncSession, *, id: int) -> Optional[InterviewSession]:
        """Get interview session with questions."""
        result = await db.execute(
            select(InterviewSession)
            .options(
                selectinload(InterviewSession.questions),
                selectinload(InterviewSession.responses)
            )
            .filter(InterviewSession.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_multi_filtered(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        candidate_id: Optional[int] = None,
        interviewer_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[InterviewSession]:
        """Get multiple sessions with filtering."""
        query = select(InterviewSession)
        
        if candidate_id:
            query = query.filter(InterviewSession.candidate_id == candidate_id)
        if interviewer_id:
            query = query.filter(InterviewSession.interviewer_id == interviewer_id)
        if status:
            query = query.filter(InterviewSession.status == status)
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()


class CRUDQuestion(CRUDBase[Question, QuestionCreate, QuestionUpdate]):
    """CRUD operations for Question."""
    
    async def get_by_category(
        self, 
        db: AsyncSession, 
        *, 
        category: str, 
        difficulty: Optional[str] = None
    ) -> List[Question]:
        """Get questions by category and optional difficulty."""
        query = select(Question).filter(Question.category == category)
        if difficulty:
            query = query.filter(Question.difficulty == difficulty)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_multi_by_ids(self, db: AsyncSession, *, ids: List[int]) -> List[Question]:
        """Get multiple questions by list of IDs."""
        result = await db.execute(select(Question).filter(Question.id.in_(ids)))
        return result.scalars().all()


class CRUDInterviewResponse(CRUDBase[InterviewResponse, Dict[str, Any], Dict[str, Any]]):
    """CRUD operations for InterviewResponse."""
    
    async def get_by_session(
        self, 
        db: AsyncSession, 
        *, 
        session_id: int,
        evaluated_only: bool = False
    ) -> List[InterviewResponse]:
        """Get all responses for a session."""
        query = select(InterviewResponse).filter(InterviewResponse.session_id == session_id)
        if evaluated_only:
            query = query.filter(InterviewResponse.score.isnot(None))
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_session_and_question(
        self, 
        db: AsyncSession, 
        *, 
        session_id: int,
        question_id: int
    ) -> Optional[InterviewResponse]:
        """Get response for specific session and question."""
        result = await db.execute(
            select(InterviewResponse)
            .filter(
                InterviewResponse.session_id == session_id,
                InterviewResponse.question_id == question_id
            )
        )
        return result.scalar_one_or_none()


# Create instances
interview_session = CRUDInterviewSession(InterviewSession)
question = CRUDQuestion(Question)
interview_response = CRUDInterviewResponse(InterviewResponse)