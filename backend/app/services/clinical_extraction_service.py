"""
Clinical extraction service.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from app.ai.ollama_provider import ollama_provider
from app.ai.clinical_extraction_prompt import (
    CLINICAL_EXTRACTION_SYSTEM_PROMPT,
    build_extraction_prompt,
)
from app.db.repositories.clinical_extraction_repository import clinical_extraction_repository
from app.db.repositories.interview_repository import interview_repository
from app.db.connection import mongo_connection
from app.models.clinical_history import (
    ClinicalHistoryExtraction,
    ExtractedField,
    EXTRACTION_STATUS,
)
import json
import re
import logging

logger = logging.getLogger(__name__)

class ClinicalExtractionService:
    """Service for clinical information extraction."""
    
    def __init__(self):
        self.provider = ollama_provider
    
    async def extract_from_response(
        self,
        user: Dict[str, Any],
        response_id: str,
    ) -> Dict[str, Any]:
        """
        Extract structured clinical information from a patient response.
        """
        # Check if extraction already exists
        existing = await clinical_extraction_repository.find_by_response_id(response_id)
        if existing:
            return {
                "success": True,
                "message": "Extraction already exists",
                "extraction": existing,
                "status_code": 200,
            }
        
        # Get response from interview_responses collection
        response = await self._get_response_by_id(response_id)
        if not response:
            return {"success": False, "error": "Response not found.", "status_code": 404}
        
        # Get interview
        interview = await interview_repository.find_by_id(response.get("interview_id", ""))
        if not interview:
            return {"success": False, "error": "Interview not found.", "status_code": 404}
        
        # Verify ownership
        if str(interview.get("user_id")) != str(user["_id"]):
            return {"success": False, "error": "Access denied.", "status_code": 403}
        
        # Build extraction prompt
        from app.data.interview_questions import get_question_by_id, get_question_text
        
        question = get_question_by_id(response.get("question_id", ""))
        question_text = ""
        if question:
            question_text = get_question_text(question, interview.get("language", "english"))
        
        prompt = build_extraction_prompt(
            section=response.get("section", ""),
            question_text=question_text,
            patient_response=response.get("response_text", ""),
            language=interview.get("language", "english"),
        )
        
        # Call Ollama
        ollama_result = await self.provider.generate_structured_response(prompt)
        
        if not ollama_result.get("success"):
            # Store failed extraction
            failed_extraction = await clinical_extraction_repository.create_extraction(
                interview_id=interview["_id"],
                consultation_id=interview.get("consultation_id", ""),
                patient_id=interview.get("patient_id", ""),
                response_id=response_id,
                question_id=response.get("question_id", ""),
                section=response.get("section", ""),
                extracted_fields={},
                status="failed",
            )
            
            return {
                "success": False,
                "error": ollama_result.get("error", "Extraction failed"),
                "status": "failed",
                "status_code": 502,
            }
        
        # Parse and validate output
        extracted_data = ollama_result.get("data", {})
        fields = extracted_data.get("fields", {})
        
        # Convert to ExtractedField objects
        structured_fields = self._convert_to_extracted_fields(
            fields,
            response.get("question_id", ""),
            response_id,
        )
        
        # Save extraction
        extraction = await clinical_extraction_repository.create_extraction(
            interview_id=str(interview["_id"]),
            consultation_id=interview.get("consultation_id", ""),
            patient_id=interview.get("patient_id", ""),
            response_id=response_id,
            question_id=response.get("question_id", ""),
            section=response.get("section", ""),
            extracted_fields=structured_fields,
            status="completed",
        )
        
        if not extraction:
            return {"success": False, "error": "Failed to save extraction.", "status_code": 500}
        
        return {
            "success": True,
            "message": "Extraction completed",
            "extraction": extraction,
            "status_code": 201,
        }
    
    async def _get_response_by_id(self, response_id: str) -> Optional[Dict[str, Any]]:
        """Get response from interview_responses collection."""
        try:
            from bson import ObjectId
            collection = mongo_connection.database["interview_responses"]
            obj_id = ObjectId(response_id)
            return await collection.find_one({"_id": obj_id})
        except Exception:
            return None
    
    def _convert_to_extracted_fields(
        self,
        fields: Dict[str, Any],
        question_id: str,
        response_id: str,
    ) -> Dict[str, Any]:
        """Convert raw fields to structured extracted fields."""
        structured = {}
        
        for field_name, field_data in fields.items():
            if field_data is None:
                structured[field_name] = None
            elif isinstance(field_data, list):
                structured[field_name] = []
                for item in field_data:
                    if isinstance(item, dict) and item.get("value"):
                        structured[field_name].append({
                            "value": item["value"],
                            "source": "patient_response",
                            "question_id": question_id,
                            "response_id": response_id,
                            "confidence": None,
                        })
            elif isinstance(field_data, dict) and field_data.get("value"):
                structured[field_name] = {
                    "value": field_data["value"],
                    "source": "patient_response",
                    "question_id": question_id,
                    "response_id": response_id,
                    "confidence": None,
                }
            else:
                structured[field_name] = None
        
        return structured
    
    async def get_structured_history(
        self,
        user: Dict[str, Any],
        interview_id: str,
    ) -> Dict[str, Any]:
        """
        Aggregate all extractions into a structured clinical history draft.
        """
        interview = await interview_repository.find_by_id(interview_id)
        
        if not interview:
            return {"success": False, "error": "Interview not found.", "status_code": 404}
        
        if str(interview.get("user_id")) != str(user["_id"]):
            return {"success": False, "error": "Access denied.", "status_code": 403}
        
        extractions = await clinical_extraction_repository.find_by_interview_id(interview_id)
        
        # Aggregate fields
        aggregated = self._aggregate_extractions(extractions)
        
        return {
            "success": True,
            "structured_history": aggregated,
            "extraction_count": len(extractions),
            "status": "draft",
        }
    
    def _aggregate_extractions(self, extractions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate extraction records into structured history."""
        aggregated = {
            "chief_complaint": None,
            "duration": None,
            "onset": None,
            "symptoms": [],
            "severity": None,
            "aggravating_factors": [],
            "relieving_factors": [],
            "medical_history": [],
            "medications": [],
            "allergies": [],
            "family_history": [],
            "appetite": None,
            "bowel_habits": None,
            "sleep": None,
            "lifestyle": None,
            "additional_information": [],
        }
        
        for extraction in extractions:
            if extraction.get("status") != "completed":
                continue
            
            fields = extraction.get("extracted_fields", {})
            
            for field_name, field_value in fields.items():
                if field_name not in aggregated:
                    continue
                
                if field_value is None:
                    continue
                
                if isinstance(aggregated[field_name], list):
                    if isinstance(field_value, list):
                        aggregated[field_name].extend(field_value)
                    else:
                        aggregated[field_name].append(field_value)
                else:
                    if aggregated[field_name] is None:
                        aggregated[field_name] = field_value
                    elif isinstance(field_value, dict) and field_value.get("value"):
                        # Conflict detection
                        if aggregated[field_name].get("value") != field_value.get("value"):
                            aggregated[f"{field_name}_conflict"] = True
                            aggregated[f"{field_name}_needs_review"] = True
        
        return aggregated

clinical_extraction_service = ClinicalExtractionService()