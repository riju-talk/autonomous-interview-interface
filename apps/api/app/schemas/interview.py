from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

from app.schemas.base import ORMModeMixin, IDModelMixin, TimestampMixin

class QuestionType(str, Enum):
    """Types of interview questions."""
    OBJECTIVE = "objective"
    MULTI_TURN = "multi_turn"
    ASSIGNMENT = "assignment"

class DifficultyLevel(str, Enum):
    """Difficulty levels for questions."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class InterviewSessionStatus(str, Enum):
    """Status of an interview session."""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class QuestionBase(BaseModel):
    """Base schema for interview questions."""
    text: str = Field(..., description="The question text")
    question_type: QuestionType = Field(..., description="Type of the question")
    difficulty: DifficultyLevel = Field(..., description="Difficulty level")
    category: str = Field(..., description="Question category/topic")
    options: Optional[List[Dict[str, Any]]] = Field(None, description="Multiple choice options if applicable")
    correct_answer: Optional[Dict[str, Any]] = Field(None, description="Expected answer format and data")
    explanation: Optional[str] = Field(None, description="Explanation of the correct answer")
    max_score: int = Field(100, description="Maximum score for this question")
    time_limit: Optional[int] = Field(None, description="Time limit in seconds")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class QuestionCreate(QuestionBase):
    """Schema for creating a new question."""
    pass

class QuestionUpdate(BaseModel):
    """Schema for updating a question."""
    text: Optional[str] = None
    question_type: Optional[QuestionType] = None
    difficulty: Optional[DifficultyLevel] = None
    category: Optional[str] = None
    options: Optional[List[Dict[str, Any]]] = None
    correct_answer: Optional[Dict[str, Any]] = None
    explanation: Optional[str] = None
    max_score: Optional[int] = None
    time_limit: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

class QuestionInDB(QuestionBase, IDModelMixin, TimestampMixin, ORMModeMixin):
    """Schema for question data stored in the database."""
    created_by: Optional[int] = Field(None, description="ID of the user who created the question")

class QuestionPublic(QuestionInDB):
    """Schema for public question data (returned in API responses)."""
    pass

class InterviewSessionBase(BaseModel):
    """Base schema for interview sessions."""
    title: str = Field(..., description="Title of the interview session")
    description: Optional[str] = Field(None, description="Description of the interview session")
    status: InterviewSessionStatus = Field(default=InterviewSessionStatus.DRAFT, description="Current status of the interview")
    scheduled_at: Optional[datetime] = Field(None, description="Scheduled start time")
    time_limit: Optional[int] = Field(None, description="Time limit in minutes")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class InterviewSessionCreate(InterviewSessionBase):
    """Schema for creating a new interview session."""
    candidate_id: int = Field(..., description="ID of the candidate being interviewed")
    interviewer_id: Optional[int] = Field(None, description="ID of the interviewer")
    question_ids: List[int] = Field(default_factory=list, description="List of question IDs for this interview")

class InterviewSessionUpdate(BaseModel):
    """Schema for updating an interview session."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[InterviewSessionStatus] = None
    scheduled_at: Optional[datetime] = None
    time_limit: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

class InterviewSessionInDB(InterviewSessionBase, IDModelMixin, TimestampMixin, ORMModeMixin):
    """Schema for interview session data stored in the database."""
    candidate_id: int = Field(..., description="ID of the candidate being interviewed")
    interviewer_id: Optional[int] = Field(None, description="ID of the interviewer")
    started_at: Optional[datetime] = Field(None, description="When the interview was started")
    completed_at: Optional[datetime] = Field(None, description="When the interview was completed")

class InterviewSessionPublic(InterviewSessionInDB):
    """Schema for public interview session data (returned in API responses)."""
    pass

class InterviewSessionWithDetails(InterviewSessionPublic):
    """Schema for interview session with additional details."""
    questions: List[QuestionPublic] = Field(default_factory=list, description="List of questions in this interview")
    candidate: Dict[str, Any] = Field(..., description="Candidate details")
    interviewer: Optional[Dict[str, Any]] = Field(None, description="Interviewer details")

class AnswerSubmission(BaseModel):
    """Schema for submitting an answer to an interview question."""
    question_id: int = Field(..., description="ID of the question being answered")
    answer: Dict[str, Any] = Field(..., description="The answer data")
    time_taken: Optional[int] = Field(None, description="Time taken to answer in seconds")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class EvaluationResult(BaseModel):
    """Schema for evaluation results of an answer."""
    score: float = Field(..., ge=0, le=100, description="Score out of 100")
    is_correct: bool = Field(..., description="Whether the answer is correct")
    feedback: str = Field(..., description="Detailed feedback on the answer")
    breakdown: Dict[str, float] = Field(..., description="Score breakdown by criteria")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional evaluation metadata")

class InterviewResponseBase(BaseModel):
    """Base schema for interview responses."""
    answer: Dict[str, Any] = Field(..., description="The answer data")
    time_taken: int = Field(..., description="Time taken to answer in seconds")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class InterviewResponseCreate(InterviewResponseBase):
    """Schema for creating a new interview response."""
    question_id: int = Field(..., description="ID of the question being answered")
    session_id: int = Field(..., description="ID of the interview session")

class InterviewResponseInDB(InterviewResponseBase, IDModelMixin, TimestampMixin, ORMModeMixin):
    """Schema for interview response data stored in the database."""
    question_id: int = Field(..., description="ID of the question")
    session_id: int = Field(..., description="ID of the interview session")
    evaluator_id: Optional[int] = Field(None, description="ID of the user who evaluated the response")
    evaluated_at: Optional[datetime] = Field(None, description="When the response was evaluated")
    evaluation_result: Optional[Dict[str, Any]] = Field(None, description="Evaluation results")

class InterviewResponsePublic(InterviewResponseInDB):
    """Schema for public interview response data (returned in API responses)."""
    question: Optional[QuestionPublic] = Field(None, description="The question that was answered")

class InterviewSessionSummary(BaseModel):
    """Schema for interview session summary."""
    session_id: int = Field(..., description="ID of the interview session")
    title: str = Field(..., description="Title of the interview session")
    status: InterviewSessionStatus = Field(..., description="Current status")
    total_questions: int = Field(..., description="Total number of questions")
    questions_answered: int = Field(..., description="Number of questions answered")
    average_score: Optional[float] = Field(None, description="Average score across all questions")
    time_spent: Optional[int] = Field(None, description="Total time spent in seconds")
    started_at: Optional[datetime] = Field(None, description="When the interview was started")
    completed_at: Optional[datetime] = Field(None, description="When the interview was completed")
