"""
Smart follow-up questioning service.
"""
from typing import Optional, Dict, Any, List
from app.ai.ollama_provider import ollama_provider
from app.ai.follow_up_prompt import FOLLOW_UP_SYSTEM_PROMPT, build_follow_up_prompt
from app.db.repositories.follow_up_repository import follow_up_repository
from app.db.repositories.interview_repository import interview_repository
from app.db.repositories.clinical_extraction_repository import clinical_extraction_repository
from app.models.follow_up import FollowUpDecision, CLINICAL_FIELDS
from app.data.interview_questions import get_question_by_id, get_question_text
from app.core.config import settings
import json
import logging

logger = logging.getLogger(__name__)

# Deterministic fallback questions
DETERMINISTIC_FALLBACKS = {
    "duration": "How long have you been experiencing this?",
    "onset": "When did this problem first begin?",
    "severity": "How would you describe the severity of this symptom?",
    "aggravating_factors": "Is there anything that makes this symptom worse?",
    "relieving_factors": "Is there anything that makes this symptom better?",
    "symptoms": "Could you describe any other symptoms you are experiencing?",
    "medical_history": "Do you have any existing medical conditions?",
    "medications": "Are you currently taking any medications?",
    "allergies": "Do you have any known allergies?",
    "family_history": "Is there any family history of medical conditions?",
}

class SmartFollowUpService:
    """Service for smart follow-up questioning."""
    
    def __init__(self):
        self.max_followups_per_interview = getattr(settings, 'MAX_FOLLOWUPS_PER_INTERVIEW', 10)
    
    async def get_follow_up(
        self,
        user: Dict[str, Any],
        interview_id: str,
        response_id: str,
    ) -> Dict[str, Any]:
        """
        Determine if follow-up question is needed.
        """
        # Get interview
        interview = await interview_repository.find_by_id(interview_id)
        if not interview:
            return {"success": False, "error": "Interview not found.", "status_code": 404}
        
        # Verify ownership
        if str(interview.get("user_id")) != str(user["_id"]):
            return {"success": False, "error": "Access denied.", "status_code": 403}
        
        # Check follow-up limit
        followup_count = await follow_up_repository.get_followup_count(interview_id)
        if followup_count >= self.max_followups_per_interview:
            return {
                "success": True,
                "data": {
                    "should_follow_up": False,
                    "target_field": None,
                    "question": None,
                    "source": "limit_reached",
                    "ai_available": False,
                },
            }
        
        # Get response
        response = await self._get_response_by_id(response_id)
        if not response:
            return {"success": False, "error": "Response not found.", "status_code": 404}
        
        # Get current question
        question = get_question_by_id(response.get("question_id", ""))
        question_text = ""
        if question:
            question_text = get_question_text(question, interview.get("language", "english"))
        
        # Get extracted fields from Phase 14
        extracted_fields = await self._get_extracted_fields(interview_id)
        
        # Get asked follow-ups
        asked_fields = await follow_up_repository.get_asked_fields(interview_id)
        
        # Try AI provider
        language = interview.get("language", "english")
        
        prompt = build_follow_up_prompt(
            language=language,
            current_section=response.get("section", ""),
            current_question=question_text,
            patient_response=response.get("response_text", ""),
            extracted_fields=extracted_fields,
            asked_followups=asked_fields,
        )
        
        ai_result = await ollama_provider.generate_structured_response(prompt)
        
        if ai_result.get("success"):
            try:
                decision = FollowUpDecision(**ai_result["data"])
                
                # Check if field already asked
                if decision.target_field in asked_fields:
                    # Find alternative field
                    alternative = await self._find_alternative_field(extracted_fields, asked_fields)
                    if alternative:
                        decision = FollowUpDecision(
                            should_follow_up=True,
                            target_field=alternative,
                            question=DETERMINISTIC_FALLBACKS.get(alternative, f"Could you tell me more about {alternative}?"),
                            reason=f"Alternative field: {alternative}",
                            language=language,
                        )
                    else:
                        decision = FollowUpDecision(
                            should_follow_up=False,
                            target_field=None,
                            question=None,
                            reason="Required information sufficiently captured",
                            language=language,
                        )
                
                if decision.should_follow_up and decision.question and decision.target_field:
                    # Save follow-up record
                    await follow_up_repository.create_followup(
                        interview_id=interview_id,
                        consultation_id=interview.get("consultation_id", ""),
                        patient_id=interview.get("patient_id", ""),
                        response_id=response_id,
                        target_field=decision.target_field,
                        question=decision.question,
                        language=language,
                        source="ai",
                    )
                
                return {
                    "success": True,
                    "data": {
                        "should_follow_up": decision.should_follow_up,
                        "target_field": decision.target_field,
                        "question": decision.question,
                        "source": "ai" if decision.should_follow_up else "none",
                        "ai_available": True,
                    },
                }
            
            except Exception as e:
                logger.warning(f"AI follow-up validation failed: {str(e)}")
        
        # Deterministic fallback
        return await self._deterministic_fallback(
            interview_id,
            interview,
            response_id,
            response,
            extracted_fields,
            asked_fields,
            language,
        )
    
    async def _get_response_by_id(self, response_id: str) -> Optional[Dict[str, Any]]:
        """Get response from database."""
        try:
            from bson import ObjectId
            from app.db.connection import mongo_connection
            collection = mongo_connection.database["interview_responses"]
            obj_id = ObjectId(response_id)
            return await collection.find_one({"_id": obj_id})
        except Exception:
            return None
    
    async def _get_extracted_fields(self, interview_id: str) -> Dict[str, Any]:
        """Get aggregated extracted fields."""
        extractions = await clinical_extraction_repository.find_by_interview_id(interview_id)
        
        aggregated = {}
        for extraction in extractions:
            if extraction.get("status") != "completed":
                continue
            fields = extraction.get("extracted_fields", {})
            for field_name, field_value in fields.items():
                if field_value is not None and field_name not in aggregated:
                    aggregated[field_name] = field_value
        
        return aggregated
    
    async def _find_alternative_field(
        self,
        extracted_fields: Dict[str, Any],
        asked_fields: List[str],
    ) -> Optional[str]:
        """Find a field that hasn't been asked about."""
        priority_order = [
            "duration", "onset", "severity", "symptoms",
            "aggravating_factors", "relieving_factors",
            "medical_history", "medications", "allergies",
        ]
        
        for field in priority_order:
            if field not in extracted_fields and field not in asked_fields:
                return field
        
        return None
    
    async def _deterministic_fallback(
        self,
        interview_id: str,
        interview: Dict[str, Any],
        response_id: str,
        response: Dict[str, Any],
        extracted_fields: Dict[str, Any],
        asked_fields: List[str],
        language: str,
    ) -> Dict[str, Any]:
        """Deterministic fallback for follow-up detection."""
        
        # Check for missing important fields
        for field in DETERMINISTIC_FALLBACKS:
            if field not in extracted_fields and field not in asked_fields:
                question_text = DETERMINISTIC_FALLBACKS[field]
                
                # Save follow-up
                await follow_up_repository.create_followup(
                    interview_id=interview_id,
                    consultation_id=interview.get("consultation_id", ""),
                    patient_id=interview.get("patient_id", ""),
                    response_id=response_id,
                    target_field=field,
                    question=question_text,
                    language=language,
                    source="deterministic",
                )
                
                return {
                    "success": True,
                    "data": {
                        "should_follow_up": True,
                        "target_field": field,
                        "question": question_text,
                        "source": "deterministic",
                        "ai_available": False,
                    },
                }
        
        # No follow-up needed
        return {
            "success": True,
            "data": {
                "should_follow_up": False,
                "target_field": None,
                "question": None,
                "source": "none",
                "ai_available": False,
            },
        }

smart_follow_up_service = SmartFollowUpService()