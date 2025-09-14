"""Sample data module for initializing the database with test data."""

from typing import List, Dict, Any
from app.models.interview import Question, InterviewSession, InterviewResponse
from app.core.database import get_db

async def load_sample_questions() -> List[Question]:
    """Load sample questions into the database."""
    questions = [
        {
            "category": "Python",
            "difficulty": "easy",
            "question_type": "objective",
            "prompt": "What is the difference between a list and a tuple in Python?",
            "options": {
                "A": "Lists are mutable, tuples are immutable",
                "B": "Tuples are mutable, lists are immutable",
                "C": "Both are mutable",
                "D": "Both are immutable"
            },
            "correct_answer": {"answer": "A"},
            "explanation": "In Python, lists are mutable (can be changed) while tuples are immutable (cannot be changed)."
        },
        {
            "category": "Python",
            "difficulty": "medium",
            "question_type": "multi_turn",
            "prompt": "Explain how Python's garbage collection works.",
            "correct_answer": {
                "key_points": [
                    "Reference counting",
                    "Cycle detection",
                    "Generational garbage collection"
                ]
            }
        }
    ]
    
    db_questions = []
    async with get_db() as session:
        for q in questions:
            db_question = Question(**q)
            session.add(db_question)
            db_questions.append(db_question)
        await session.commit()
    
    return db_questions

async def load_sample_sessions() -> List[InterviewSession]:
    """Load sample interview sessions into the database."""
    questions = await load_sample_questions()
    
    session_data = {
        "status": "completed",
        "difficulty": "easy",
        "score": 8.5,
        "feedback": {"overall": "Good performance on basic Python concepts."}
    }
    
    async with get_db() as session:
        db_session = InterviewSession(**session_data)
        db_session.questions = questions[:1]  # Add first question to the session
        session.add(db_session)
        
        # Add a sample response
        response = InterviewResponse(
            session=db_session,
            question=questions[0],
            user_answer={"answer": "A"},
            is_correct=True,
            score=1.0,
            feedback={"comment": "Correct answer"}
        )
        session.add(response)
        
        await session.commit()
        
        return [db_session]

async def load_all_sample_data() -> Dict[str, Any]:
    """Load all sample data into the database."""
    questions = await load_sample_questions()
    sessions = await load_sample_sessions()
    
    return {
        "questions_loaded": len(questions),
        "sessions_created": len(sessions)
    }
