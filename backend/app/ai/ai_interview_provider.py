"""
AI interview provider abstraction.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from app.ai.ollama_provider import ollama_provider
from app.ai.prompts import build_interview_prompt
from app.models.ai import AIInterviewDecision
import logging

logger = logging.getLogger(__name__)

class AIInterviewProvider(ABC):
    """Abstract interface for AI interview providers."""
    
    @abstractmethod
    async def get_next_question(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate next question based on context."""
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """Check if provider is available."""
        pass

class LocalOllamaInterviewProvider(AIInterviewProvider):
    """Local Ollama Qwen3 provider for interview."""
    
    def __init__(self):
        self.provider = ollama_provider
    
    async def is_available(self) -> bool:
        """Check if Ollama and model are available."""
        health = await self.provider.check_health()
        return health.get("available") and health.get("model_available")
    
    async def get_next_question(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate next question using local Qwen3.
        """
        language = context.get("language", "english")
        consultation_type = context.get("consultation_type", "general")
        current_section = context.get("current_section", "introduction")
        current_question = context.get("current_question", "")
        patient_response = context.get("patient_response", "")
        completed_sections = context.get("completed_sections", [])
        
        prompt = build_interview_prompt(
            language=language,
            consultation_type=consultation_type,
            current_section=current_section,
            current_question=current_question,
            patient_response=patient_response,
            completed_sections=completed_sections,
        )
        
        result = await self.provider.generate_structured_response(prompt)
        
        if not result.get("success"):
            return {
                "success": False,
                "error": result.get("error", "AI provider failed"),
            }
        
        # Validate against Pydantic model
        try:
            decision = AIInterviewDecision(**result["data"])
            return {
                "success": True,
                "decision": decision,
            }
        except Exception as e:
            logger.warning(f"AI output validation failed: {str(e)}")
            return {
                "success": False,
                "error": "AI output validation failed",
            }

class MockAIInterviewProvider(AIInterviewProvider):
    """Mock provider that always fails gracefully."""
    
    async def is_available(self) -> bool:
        return False
    
    async def get_next_question(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "success": False,
            "error": "AI provider not available",
        }