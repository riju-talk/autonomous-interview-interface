from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import uuid

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.interview import InterviewSession, InterviewResponse, Question
from app.schemas.interview import (
    InterviewSessionCreate,
    InterviewSessionUpdate,
    InterviewSessionInDB,
    InterviewSessionPublic,
    InterviewSessionWithDetails,
    InterviewSessionSummary,
    InterviewResponseCreate,
    InterviewResponsePublic,
    AnswerSubmission,
    EvaluationResult,
    InterviewSessionStatus,
)
from app.services.chroma_service import chroma_service
from app.services.llm_service import llm_service

router = APIRouter()

@router.post("/", response_model=InterviewSessionPublic)
async def create_interview_session(
    session_in: InterviewSessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create a new interview session.
    """
    # Check if candidate exists
    candidate = await User.get(db, session_in.candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    # Check if interviewer exists if provided
    if session_in.interviewer_id:
        interviewer = await User.get(db, session_in.interviewer_id)
        if not interviewer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interviewer not found"
            )
    
    # Get questions
    questions = []
    if session_in.question_ids:
        questions = await Question.get_multi_by_ids(db, ids=session_in.question_ids)
        if len(questions) != len(session_in.question_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more questions not found"
            )
    
    # Create session
    session_data = session_in.dict(exclude={"question_ids"})
    db_session = InterviewSession(**session_data, created_by=current_user.id)
    db.add(db_session)
    
    # Add questions to session
    for question in questions:
        db_session.questions.append(question)
    
    await db.commit()
    await db.refresh(db_session)
    
    return db_session

@router.get("/{session_id}", response_model=InterviewSessionWithDetails)
async def get_interview_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get interview session by ID.
    """
    # Get session with relationships
    session = await InterviewSession.get_with_details(db, id=session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found"
        )
    
    # Check permissions
    if not (
        current_user.is_superuser or
        current_user.id == session.interviewer_id or
        current_user.id == session.candidate_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this interview session"
        )
    
    return session

@router.put("/{session_id}", response_model=InterviewSessionPublic)
async def update_interview_session(
    session_id: int,
    session_in: InterviewSessionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update an interview session.
    """
    # Get session
    session = await InterviewSession.get(db, id=session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found"
        )
    
    # Check permissions
    if not (
        current_user.is_superuser or
        current_user.id == session.interviewer_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this interview session"
        )
    
    # Update session
    update_data = session_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(session, field, value)
    
    session.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(session)
    
    return session

@router.get("/", response_model=List[InterviewSessionSummary])
async def list_interview_sessions(
    skip: int = 0,
    limit: int = 100,
    status: Optional[InterviewSessionStatus] = None,
    candidate_id: Optional[int] = None,
    interviewer_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    List interview sessions with optional filtering.
    """
    # Regular users can only see their own sessions
    if not current_user.is_superuser:
        if candidate_id and candidate_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view these sessions"
            )
        if interviewer_id and interviewer_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view these sessions"
            )
        
        # If no filters, show only user's sessions
        if not (candidate_id or interviewer_id):
            candidate_id = current_user.id
    
    # Get sessions
    sessions = await InterviewSession.get_multi(
        db,
        skip=skip,
        limit=limit,
        status=status,
        candidate_id=candidate_id,
        interviewer_id=interviewer_id
    )
    
    # Convert to summary format
    summaries = []
    for session in sessions:
        summary = await session.to_summary(db)
        summaries.append(summary)
    
    return summaries

@router.post("/{session_id}/start", response_model=InterviewSessionPublic)
async def start_interview_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Start an interview session.
    """
    # Get session with questions
    session = await InterviewSession.get_with_questions(db, id=session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found"
        )
    
    # Check permissions
    if not (
        current_user.is_superuser or
        current_user.id == session.interviewer_id or
        current_user.id == session.candidate_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to start this interview session"
        )
    
    # Check if already started
    if session.status != InterviewSessionStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Interview session is already {session.status}"
        )
    
    # Check if there are questions
    if not session.questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot start an interview session with no questions"
        )
    
    # Update session status
    session.status = InterviewSessionStatus.IN_PROGRESS
    session.started_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(session)
    
    return session

@router.post("/{session_id}/submit-answer", response_model=InterviewResponsePublic)
async def submit_answer(
    session_id: int,
    answer_submission: AnswerSubmission,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Submit an answer to an interview question.
    """
    # Get session
    session = await InterviewSession.get_with_questions(db, id=session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found"
        )
    
    # Check permissions
    if current_user.id != session.candidate_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the candidate can submit answers"
        )
    
    # Check if session is in progress
    if session.status != InterviewSessionStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot submit answer to a session that is {session.status}"
        )
    
    # Get question
    question = await Question.get(db, id=answer_submission.question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Check if question belongs to this session
    if question.id not in [q.id for q in session.questions]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question does not belong to this session"
        )
    
    # Check if answer already exists
    existing_response = await InterviewResponse.get_by_session_and_question(
        db, session_id=session_id, question_id=question.id
    )
    
    if existing_response:
        # Update existing response
        existing_response.answer = answer_submission.answer
        existing_response.time_taken = answer_submission.time_taken
        existing_response.metadata = answer_submission.metadata
        existing_response.updated_at = datetime.utcnow()
        
        db.add(existing_response)
        await db.commit()
        await db.refresh(existing_response)
        
        return existing_response
    else:
        # Create new response
        response_data = {
            "session_id": session_id,
            "question_id": question.id,
            "answer": answer_submission.answer,
            "time_taken": answer_submission.time_taken,
            "metadata": answer_submission.metadata,
            "created_by": current_user.id
        }
        
        db_response = InterviewResponse(**response_data)
        db.add(db_response)
        
        # If this is the last question, mark session as completed
        responses = await InterviewResponse.get_by_session(db, session_id=session_id)
        if len(responses) + 1 == len(session.questions):
            session.status = InterviewSessionStatus.COMPLETED
            session.completed_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(db_response)
        
        return db_response

@router.post("/{session_id}/evaluate", response_model=EvaluationResult)
async def evaluate_answer(
    session_id: int,
    question_id: int = Body(..., embed=True),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Evaluate an answer using the LLM service.
    """
    # Get session and response
    session = await InterviewSession.get(db, id=session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found"
        )
    
    # Check permissions
    if not (
        current_user.is_superuser or
        current_user.id == session.interviewer_id or
        current_user.id == session.candidate_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to evaluate answers for this session"
        )
    
    # Get response
    response = await InterviewResponse.get_by_session_and_question(
        db, session_id=session_id, question_id=question_id
    )
    
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Response not found"
        )
    
    # Get question
    question = await Question.get(db, id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Evaluate using LLM service
    evaluation = await llm_service.evaluate_response(
        question=question,
        answer=response.answer,
        context={
            "session_id": session_id,
            "candidate_id": session.candidate_id,
            "interviewer_id": session.interviewer_id,
            "question_type": question.question_type,
            "difficulty": question.difficulty,
            "category": question.category,
        }
    )
    
    # Update response with evaluation
    response.evaluation_result = evaluation.dict()
    response.evaluated_at = datetime.utcnow()
    response.evaluator_id = current_user.id
    
    # Update session score if all questions are evaluated
    await _update_session_score(db, session)
    
    await db.commit()
    await db.refresh(response)
    
    return evaluation

async def _update_session_score(db: AsyncSession, session: InterviewSession) -> None:
    """Update the overall session score based on evaluated responses."""
    responses = await InterviewResponse.get_by_session(
        db, session_id=session.id, evaluated_only=True
    )
    
    if not responses:
        return
    
    # Calculate average score
    total_score = sum(
        response.evaluation_result.get("score", 0) 
        for response in responses 
        if response.evaluation_result
    )
    
    session.score = total_score / len(responses)
    
    # If all questions are evaluated, mark as completed
    questions = await session.awaitable_attrs.questions
    if len(responses) == len(questions):
        session.status = InterviewSessionStatus.COMPLETED
        session.completed_at = datetime.utcnow()
    
    db.add(session)
