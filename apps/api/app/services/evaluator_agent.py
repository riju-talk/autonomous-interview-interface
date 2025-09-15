from typing import List, Dict, Any
import random
from datetime import datetime
from ..models.interview import InterviewSession, Question, InterviewResponse
from ..core.config import settings

class EvaluatorAgent:
    def __init__(self):
        self.behavioral_questions = [
            "Tell me about a challenging project you worked on and how you handled it.",
            "Describe a time when you had to learn a new technology quickly.",
            "Give an example of how you've handled a difficult team member or stakeholder.",
            "Tell me about a time you made a mistake and how you handled it.",
            "Describe a situation where you had to meet a tight deadline."
        ]
        
        self.technical_questions = {
            'beginner': [
                "Explain the difference between a list and a tuple in Python.",
                "What is the difference between SQL and NoSQL databases?",
                "Explain what an API is and how it works."
            ],
            'intermediate': [
                "How would you optimize a slow database query?",
                "Explain the concept of dependency injection.",
                "How would you handle a memory leak in your application?"
            ],
            'advanced': [
                "Explain how you would design a distributed system for high availability.",
                "Describe how you would implement a caching strategy for a high-traffic web application.",
                "Explain the CAP theorem and its implications for distributed systems."
            ]
        }

    def generate_interview_questions(self, candidate_level: str = 'intermediate') -> List[Dict[str, Any]]:
        """Generate a structured interview with behavioral questions first, then technical questions."""
        # Start with introduction
        questions = [
            self._create_question(
                "introduction",
                "Welcome to your technical interview. Let's start with some questions about your experience and background.",
                "text",
                120
            )
        ]
        
        # Add behavioral questions
        random.shuffle(self.behavioral_questions)
        for i, question in enumerate(self.behavioral_questions[:3]):  # Select 3 random behavioral questions
            questions.append(
                self._create_question(
                    f"behavioral_{i+1}",
                    question,
                    "text",
                    180
                )
            )
        
        # Add technical questions based on candidate level
        tech_questions = random.sample(
            self.technical_questions.get(candidate_level, self.technical_questions['intermediate']),
            min(5, len(self.technical_questions[candidate_level]))
        )
        
        for i, question in enumerate(tech_questions):
            questions.append(
                self._create_question(
                    f"tech_{i+1}",
                    question,
                    "text",
                    240
                )
            )
        
        # Add conclusion
        questions.append(
            self._create_question(
                "conclusion",
                "Thank you for your time. Do you have any questions for us?",
                "text",
                180
            )
        )
        
        return questions
    
    def evaluate_response(self, question_id: str, response: str) -> Dict[str, Any]:
        """Evaluate a candidate's response to a question."""
        # This is a simplified evaluation - in a real app, you'd use NLP or more complex logic
        word_count = len(response.split())
        
        # Basic evaluation metrics
        evaluation = {
            "question_id": question_id,
            "response_length": word_count,
            "feedback": "",
            "score": 0,
            "suggested_follow_ups": []
        }
        
        if word_count < 10:
            evaluation["feedback"] = "Your response is quite brief. Try to provide more specific examples and details."
            evaluation["score"] = 3
        elif word_count < 30:
            evaluation["feedback"] = "Good start, but consider adding more context or examples to strengthen your response."
            evaluation["score"] = 6
        else:
            evaluation["feedback"] = "Detailed response. You provided good context and examples."
            evaluation["score"] = 8
        
        return evaluation
    
    def _create_question(self, q_id: str, text: str, q_type: str, time_limit: int) -> Dict[str, Any]:
        return {
            "id": q_id,
            "text": text,
            "type": q_type,
            "time_limit": time_limit
        }

# Singleton instance
evaluator_agent = EvaluatorAgent()
