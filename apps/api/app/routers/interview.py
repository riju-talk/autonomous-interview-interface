from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from ..services.evaluator_agent import evaluator_agent
from ..core.config import settings

router = APIRouter(prefix="/interviews", tags=["interviews"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Question(BaseModel):
    id: str
    text: str
    type: str = Field(..., description="Type of question: 'text', 'code', or 'multiple_choice'")
    options: Optional[List[str]] = None
    time_limit: int = Field(..., description="Time limit in seconds")
    category: Optional[str] = Field(None, description="Category of the question, e.g., 'behavioral', 'technical'")

class InterviewSession(BaseModel):
    id: str
    title: str = "Technical Interview"
    description: str = "A comprehensive technical interview with behavioral and technical questions"
    questions: List[Question]
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    candidate_level: str = "intermediate"
    current_question_index: int = 0
    is_completed: bool = False

class InterviewResponse(BaseModel):
    question_id: str
    response: str
    time_taken: int  # in seconds

@router.post("/sessions", response_model=InterviewSession)
async def create_interview_session(
    candidate_level: str = Query("intermediate", description="Candidate's experience level: junior, intermediate, or senior"),
    token: str = Depends(oauth2_scheme)
):
    """
    Create a new interview session with dynamically generated questions
    """
    questions_data = evaluator_agent.generate_interview_questions(candidate_level)
    
    # Convert question data to Question models
    questions = [
        Question(
            id=q["id"],
            text=q["text"],
            type=q["type"],
            time_limit=q["time_limit"],
            category="behavioral" if "behavioral" in q["id"] else "technical"
        )
        for q in questions_data
    ]
    
    # In a real app, save to database
    session = InterviewSession(
        id=str(datetime.utcnow().timestamp()),
        questions=questions,
        candidate_level=candidate_level
    )
    
    return session

@router.get("/sessions/{session_id}", response_model=InterviewSession)
async def get_interview_session(
    session_id: str,
    token: str = Depends(oauth2_scheme)
):
    """
    Get interview session details by ID
    In a real app, this would retrieve from a database
    """
    # For demo, generate a new session with the same ID
    return await create_interview_session("intermediate", token)

@router.post("/sessions/{session_id}/responses", response_model=Dict[str, Any])
async def submit_interview_response(
    session_id: str,
    response: InterviewResponse,
    token: str = Depends(oauth2_scheme)
):
    """
    Submit a response to an interview question and get immediate feedback
    """
    # In a real app, save the response to the database
    # For now, we'll just evaluate it and return feedback
    
    evaluation = evaluator_agent.evaluate_response(
        question_id=response.question_id,
        response=response.response
    )
    
    return {
        "status": "success",
        "evaluation": evaluation,
        "next_steps": "Proceed to the next question or complete the interview"
    }

@router.get("/sessions/{session_id}/evaluation", response_model=Dict[str, Any])
async def get_interview_evaluation(
    session_id: str,
    token: str = Depends(oauth2_scheme)
):
    """
    Get final evaluation for a completed interview
    """
    # In a real app, this would aggregate all responses and provide a comprehensive evaluation
    return {
        "session_id": session_id,
        "overall_score": 78,
        "strengths": [
            "Strong problem-solving skills",
            "Good communication of technical concepts"
        ],
        "areas_for_improvement": [
            "Could provide more detailed examples in behavioral questions",
            "Consider diving deeper into system design concepts"
        ],
        "recommendations": [
            "Practice explaining your thought process more clearly",
            "Review data structures and algorithms",
            "Work on time management during technical questions"
        ]
    }
