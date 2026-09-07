"""
AI interview service integrating Qwen/Ollama with interview engine.
"""
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from app.ai.ai_interview_provider import LocalOllamaInterviewProvider, MockAIInterviewProvider
from app.ai.ollama_provider import ollama_provider
from app.db.repositories.interview_repository import interview_repository
from app.data.interview_questions import (
    get_question_by_id,
    get_next_question,
    get_question_text,
    INTERVIEW_QUESTIONS,
)
from app.models.ai import AIInterviewDecision
import logging

logger = logging.getLogger(__name__)

class AIInterviewService:
    """Service for AI-assisted interview."""
    
    def __init__(self):
        self.provider = self._get_provider()
    
    def _get_provider(self):
        """Get AI provider based on configuration."""
        from app.core.config import settings
        if settings.OLLAMA_ENABLED:
            return LocalOllamaInterviewProvider()
        return MockAIInterviewProvider()
    
    async def check_ai_status(self) -> Dict[str, Any]:
        """Check AI provider status."""
        health = await ollama_provider.check_health()
        return health
    
    async def get_next_question_ai(
        self,
        user: Dict[str, Any],
        interview_id: str,
        current_question_id: str,
        patient_response: str,
    ) -> Dict[str, Any]:
        """
        Get AI-generated next question with fallback.
        """
        # Get interview
        interview = await interview_repository.find_by_id(interview_id)
        
        if not interview:
            return {"success": False, "error": "Interview not found.", "status_code": 404}
        
        if str(interview.get("user_id")) != str(user["_id"]):
            return {"success": False, "error": "Access denied.", "status_code": 403}
        
        if interview.get("status") not in ["in_progress", "ready"]:
            return {"success": False, "error": "Interview is not active.", "status_code": 400}
        
        # Get current question
        current_question = get_question_by_id(current_question_id)
        if not current_question:
            return {"success": False, "error": "Question not found.", "status_code": 404}
        
        current_question_text = get_question_text(
            current_question, interview.get("language", "english")
        )
        
        # Get responses for completed sections
        responses = await interview_repository.get_responses(interview_id)
        completed_sections = list(set(r.get("section", "") for r in responses))
        
        # Build context
        context = {
            "language": interview.get("language", "english"),
            "consultation_type": interview.get("consultation_type", "general"),
            "current_section": current_question.get("section"),
            "current_question": current_question_text,
            "patient_response": patient_response,
            "completed_sections": completed_sections,
        }
        
        # Try AI provider
        ai_result = await self.provider.get_next_question(context)
        
        if ai_result.get("success"):
            decision = ai_result["decision"]
            
            return {
                "success": True,
                "data": {
                    "question": decision.next_question,
                    "section": decision.section,
                    "source": "ai",
                    "ai_available": True,
                    "answer_status": decision.answer_status,
                },
            }
        
        # Fallback to deterministic
        logger.warning(f"AI fallback: {ai_result.get('error', 'Unknown error')}")
        
        next_question = get_next_question(current_question_id)
        if not next_question:
            return {
                "success": True,
                "data": {
                    "question": None,
                    "section": "completion",
                    "source": "deterministic",
                    "ai_available": False,
                    "completed": True,
                },
            }
        
        next_question_text = get_question_text(
            next_question, interview.get("language", "english")
        )
        
        return {
            "success": True,
            "data": {
                "question": next_question_text,
                "section": next_question.get("section"),
                "source": "deterministic",
                "ai_available": False,
                "next_question_id": next_question["question_id"],
            },
        }

ai_interview_service = AIInterviewService()