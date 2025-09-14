import logging
from typing import Dict, Any, List, Optional
import json
import time
import os
from pathlib import Path
import groq
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

from app.core.config import settings

logger = logging.getLogger(__name__)

class EvaluationResult(BaseModel):
    """Schema for LLM evaluation results."""
    score: float = Field(..., ge=0, le=100, description="Overall score (0-100)")
    is_correct: bool = Field(..., description="Whether the answer is fundamentally correct")
    feedback: str = Field(..., description="Detailed feedback on the answer")
    reasoning: str = Field(..., description="Reasoning behind the evaluation")
    follow_up_suggestions: List[str] = Field(
        default_factory=list,
        description="Suggestions for follow-up questions"
    )
    time_assessment: str = Field(
        default="unknown",
        description="Assessment of response time (too_fast, appropriate, too_slow)"
    )
    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        description="Confidence score of the evaluation (0-1)"
    )

class LLMService:
    """Service for AI-powered Excel interview evaluation using Groq."""
    
    def __init__(self):
        # Using Groq's LLaMA3 model for inference
        self.client = None
        self.model = "llama3-70b-8192"  # Groq's LLaMA3 model
        self.temperature = 0.3
        self.max_tokens = 1024
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Groq client."""
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            logger.warning(
                "GROQ_API_KEY not set. LLM functionality will be limited. "
                "Using mock responses."
            )
            return
            
        try:
            self.client = groq.Client(api_key=api_key)
            logger.info("Successfully initialized Groq client")
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            raise
    
    def _assess_response_time(self, processing_time: Optional[float], difficulty: str) -> str:
        """Assess if response time is appropriate for the question difficulty."""
        if not processing_time:
            return "unknown"
        
        # Expected time ranges by difficulty (in seconds)
        time_ranges = {
            "easy": (30, 120),
            "medium": (60, 300),
            "hard": (180, 600)
        }
        
        min_time, max_time = time_ranges.get(difficulty.lower(), (60, 300))
        
        if processing_time < min_time * 0.5:
            return "too_fast"
        elif processing_time > max_time * 1.5:
            return "too_slow"
        else:
            return "appropriate"
    
    async def evaluate_response(
        self,
        question: Any,
        answer: str,
        context: Optional[Dict[str, Any]] = None,
        processing_time: Optional[float] = None
    ) -> EvaluationResult:
        """
        Evaluate a candidate's response to an Excel interview question.
        
        Args:
            question: The question being answered
            answer: The candidate's answer (string)
            context: Additional context about the interview
            processing_time: Time taken to answer (in seconds)
            
        Returns:
            EvaluationResult with score and feedback
        """
        if not self.client:
            return self._mock_evaluation(question, answer, context, processing_time)
        
        try:
            time_assessment = self._assess_response_time(processing_time, getattr(question, 'difficulty', 'medium'))
            
            # Build Excel-specific evaluation prompt
            prompt = f"""You are an expert Excel interviewer evaluating a candidate's response to a technical Excel question.

Question: {getattr(question, 'prompt', getattr(question, 'text', str(question)))}
Category: {getattr(question, 'category', 'Excel')}
Difficulty: {getattr(question, 'difficulty', 'medium')}
Question Type: {getattr(question, 'question_type', 'objective')}
Expected Answer: {json.dumps(getattr(question, 'correct_answer', None)) if hasattr(question, 'correct_answer') else "N/A"}
Explanation: {getattr(question, 'explanation', 'N/A')}

Candidate's Answer: {answer}
Response Time: {f"{processing_time:.1f} seconds ({time_assessment})" if processing_time else "Not recorded"}

Please evaluate this response and provide:
1. A score from 0-100 based on accuracy and completeness
2. Whether the answer is fundamentally correct
3. Detailed feedback on what was good and what could be improved
4. Your reasoning for the score
5. 2-3 follow-up questions or suggestions to test deeper understanding
6. Your confidence in the evaluation (0-1)

Focus on:
- Technical accuracy of Excel formulas, functions, or concepts
- Completeness of the answer
- Understanding of underlying Excel principles
- Practical applicability

Respond in JSON format with these exact keys: score, is_correct, feedback, reasoning, follow_up_suggestions, confidence"""
            
            # Call Groq API
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Excel interviewer. Evaluate responses fairly but thoroughly, considering both technical accuracy and practical understanding."
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
                return EvaluationResult(
                    score=max(0, min(100, float(result_data.get("score", 0)))),
                    is_correct=bool(result_data.get("is_correct", False)),
                    feedback=result_data.get("feedback", "No feedback provided"),
                    reasoning=result_data.get("reasoning", "No reasoning provided"),
                    follow_up_suggestions=result_data.get("follow_up_suggestions", []),
                    time_assessment=time_assessment,
                    confidence=max(0, min(1, float(result_data.get("confidence", 0.5))))
                )
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Failed to parse LLM response: {e}")
                return self._mock_evaluation(question, answer, context, processing_time)
                
        except Exception as e:
            logger.error(f"Error evaluating response: {e}")
            # Fall back to mock evaluation on error
            return self._mock_evaluation(question, answer, context, processing_time)
    
    def _mock_evaluation(
        self,
        question: Any,
        answer: str,
        context: Optional[Dict[str, Any]] = None,
        processing_time: Optional[float] = None
    ) -> EvaluationResult:
        """Generate a mock evaluation for testing or when LLM is not available."""
        logger.warning("Using mock evaluation (LLM not available)")
        
        # Simple mock logic - in a real app, this would be more sophisticated
        score = 75.0  # Base score
        time_assessment = self._assess_response_time(processing_time, getattr(question, 'difficulty', 'medium'))
        
        return EvaluationResult(
            score=score,
            is_correct=score >= 70,
            feedback="This is a mock evaluation. Enable the LLM service for real feedback.",
            reasoning="Mock evaluation - AI service not available",
            follow_up_suggestions=["Please enable Groq API for real evaluation"],
            time_assessment=time_assessment,
            confidence=0.5
        )
    
    async def generate_follow_up_question(
        self,
        question: Any,
        answer: str,
        evaluation: EvaluationResult
    ) -> str:
        """Generate an intelligent follow-up question based on the response."""
        
        if not self.client:
            return f"Can you explain your approach to {getattr(question, 'category', 'Excel').lower()} in more detail?"
        
        prompt = f"""Based on this Excel interview exchange, generate one thoughtful follow-up question.

Original Question: {getattr(question, 'prompt', getattr(question, 'text', str(question)))}
Candidate's Answer: {answer}
Evaluation Score: {evaluation.score}/100
Areas for Improvement: {evaluation.feedback}

Generate a follow-up question that:
1. Builds on their answer (whether strong or weak)
2. Tests deeper understanding of the same concept
3. Is appropriate for their demonstrated skill level
4. Would provide valuable insight into their Excel expertise

Return only the follow-up question text, no additional formatting."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Excel interviewer. Generate insightful follow-up questions that reveal deeper understanding."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating follow-up question: {e}")
            return f"Can you explain your approach to {getattr(question, 'category', 'Excel').lower()} in more detail?"

# Global LLM service instance
llm_service = LLMService()
