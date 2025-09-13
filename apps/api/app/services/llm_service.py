import logging
from typing import Dict, Any, List, Optional
import json
import time
from pathlib import Path

import groq
from groq import Groq
from pydantic import BaseModel, Field, validator

from app.core.config import settings
from app.services.chroma_service import chroma_service

logger = logging.getLogger(__name__)

class EvaluationResult(BaseModel):
    """Schema for LLM evaluation results."""
    score: float = Field(..., ge=0, le=100, description="Overall score (0-100)")
    breakdown: Dict[str, float] = Field(
        ...,
        description="Score breakdown by evaluation criteria"
    )
    feedback: str = Field(..., description="Detailed feedback on the answer")
    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        description="Confidence score of the evaluation (0-1)"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the evaluation"
    )

class LLMService:
    """Service for interacting with the LLM (ChatGroq)."""
    
    def __init__(self):
        self.client = None
        self.model = "mixtral-8x7b-32768"  # Default model
        self.temperature = 0.1
        self.max_tokens = 1024
        self._initialize_client()
        
        # Load prompts
        self.prompts = self._load_prompts()
    
    def _initialize_client(self):
        """Initialize the Groq client."""
        if not settings.GROQ_API_KEY:
            logger.warning(
                "GROQ_API_KEY not set. LLM functionality will be limited. "
                "Using mock responses."
            )
            return
            
        try:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            logger.info("Successfully initialized Groq client")
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            raise
    
    def _load_prompts(self) -> Dict[str, str]:
        """Load prompt templates from the prompts directory."""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts = {}
        
        if not prompts_dir.exists():
            logger.warning(f"Prompts directory not found: {prompts_dir}")
            return prompts
            
        for prompt_file in prompts_dir.glob("*.txt"):
            with open(prompt_file, "r", encoding="utf-8") as f:
                prompts[prompt_file.stem] = f.read()
                
        return prompts
    
    async def evaluate_response(
        self,
        question: Any,
        answer: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> EvaluationResult:
        """
        Evaluate a candidate's response to an interview question.
        
        Args:
            question: The question being answered
            answer: The candidate's answer
            context: Additional context about the interview
            
        Returns:
            EvaluationResult with score and feedback
        """
        if not self.client:
            return self._mock_evaluation(question, answer, context)
        
        try:
            # Get the appropriate prompt template based on question type
            prompt_template = self.prompts.get(
                f"evaluation_{question.question_type}",
                self.prompts.get("evaluation_default")
            )
            
            if not prompt_template:
                raise ValueError(
                    f"No prompt template found for question type: {question.question_type}"
                )
            
            # Format the prompt with question and answer
            prompt = prompt_template.format(
                question=question.text,
                answer=json.dumps(answer, indent=2),
                context=json.dumps(context or {}, indent=2),
                **question.dict()
            )
            
            # Call the LLM
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert technical interviewer evaluating candidate responses. "
                                  "Provide a detailed evaluation with a numerical score and feedback."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            try:
                result_data = json.loads(response.choices[0].message.content)
                return EvaluationResult(**result_data)
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Failed to parse LLM response: {e}")
                raise ValueError("Invalid response format from LLM") from e
                
        except Exception as e:
            logger.error(f"Error evaluating response: {e}")
            # Fall back to mock evaluation on error
            return self._mock_evaluation(question, answer, context)
    
    def _mock_evaluation(
        self,
        question: Any,
        answer: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> EvaluationResult:
        """Generate a mock evaluation for testing or when LLM is not available."""
        logger.warning("Using mock evaluation (LLM not available)")
        
        # Simple mock logic - in a real app, this would be more sophisticated
        score = 75.0  # Base score
        feedback = "This is a mock evaluation. Enable the LLM service for real feedback."
        
        return EvaluationResult(
            score=score,
            breakdown={
                "relevance": score * 0.9,
                "accuracy": score * 0.8,
                "clarity": score * 0.95,
                "completeness": score * 0.85
            },
            feedback=feedback,
            confidence=0.7,
            metadata={
                "is_mock": True,
                "question_type": getattr(question, 'question_type', 'unknown'),
                "context": context or {}
            }
        )
    
    async def generate_follow_up_question(
        self,
        question: Any,
        answer: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a follow-up question based on the candidate's answer.
        
        Args:
            question: The original question
            answer: The candidate's answer
            context: Additional context about the interview
            
        Returns:
            Dictionary with the follow-up question and metadata
        """
        if not self.client:
            return self._mock_follow_up_question(question, answer, context)
            
        try:
            # Get the follow-up prompt template
            prompt_template = self.prompts.get("follow_up_question")
            
            if not prompt_template:
                raise ValueError("No follow-up prompt template found")
            
            # Format the prompt with question and answer
            prompt = prompt_template.format(
                question=question.text,
                answer=json.dumps(answer, indent=2),
                context=json.dumps(context or {}, indent=2),
                **question.dict()
            )
            
            # Call the LLM
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert technical interviewer. "
                                  "Generate a relevant follow-up question based on the candidate's answer."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.7,  # Slightly more creative for follow-ups
                max_tokens=500
            )
            
            # Parse the response
            follow_up = response.choices[0].message.content.strip()
            
            return {
                "text": follow_up,
                "context": {
                    "original_question_id": getattr(question, 'id', None),
                    "original_answer": answer,
                    "generated_at": time.time()
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating follow-up question: {e}")
            return self._mock_follow_up_question(question, answer, context)
    
    def _mock_follow_up_question(
        self,
        question: Any,
        answer: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a mock follow-up question for testing."""
        logger.warning("Using mock follow-up question (LLM not available)")
        
        return {
            "text": f"Can you elaborate more on {list(answer.keys())[0] if answer else 'your answer'}?",
            "context": {
                "original_question_id": getattr(question, 'id', None),
                "is_mock": True,
                "generated_at": time.time()
            }
        }

# Global LLM service instance
llm_service = LLMService()
