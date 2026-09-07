"""
Consultation service for Phase 10.
"""
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from app.db.repositories.consultation_repository import consultation_repository
from app.db.repositories.patient_repository import patient_repository
from app.models.consultation import ConsultationCreate
import logging

logger = logging.getLogger(__name__)

class ConsultationService:
    """Service for consultation setup operations."""
    
    @staticmethod
    async def create_consultation(
        user: Dict[str, Any],
        consultation_data: ConsultationCreate,
    ) -> Dict[str, Any]:
        """
        Create consultation setup for authenticated patient.
        """
        # Get patient profile
        patient = await patient_repository.find_by_user_id(str(user["_id"]))
        
        if not patient:
            return {
                "success": False,
                "error": "Patient profile not found. Please complete your profile first.",
                "status_code": 404,
            }
        
        # Generate server-side consent timestamp
        consent_timestamp = datetime.now(timezone.utc)
        
        # Create consultation
        consultation = await consultation_repository.create_consultation(
            user_id=str(user["_id"]),
            patient_id=str(patient["_id"]),
            language=consultation_data.language,
            consultation_type=consultation_data.consultation_type,
            consent_given=consultation_data.consent_given,
            consent_timestamp=consent_timestamp,
            status="setup",
        )
        
        if not consultation:
            return {
                "success": False,
                "error": "Failed to create consultation. Please try again.",
                "status_code": 500,
            }
        
        return {
            "success": True,
            "message": "Consultation setup created",
            "consultation": {
                "id": str(consultation["_id"]),
                "patient_id": consultation["patient_id"],
                "user_id": consultation["user_id"],
                "language": consultation["language"],
                "consultation_type": consultation["consultation_type"],
                "consent_given": consultation["consent_given"],
                "consent_timestamp": consultation["consent_timestamp"].isoformat(),
                "status": consultation["status"],
                "created_at": consultation["created_at"].isoformat(),
            },
            "status_code": 201,
        }
    
    @staticmethod
    async def get_consultation(
        user: Dict[str, Any],
        consultation_id: str,
    ) -> Dict[str, Any]:
        """
        Get consultation by ID with ownership check.
        """
        consultation = await consultation_repository.find_by_id(consultation_id)
        
        if not consultation:
            return {
                "success": False,
                "error": "Consultation not found.",
                "status_code": 404,
            }
        
        # Verify ownership
        if str(consultation.get("user_id")) != str(user["_id"]):
            return {
                "success": False,
                "error": "Access denied.",
                "status_code": 403,
            }
        
        return {
            "success": True,
            "consultation": consultation,
        }
    
    @staticmethod
    async def get_patient_consultations(
        user: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Get all consultations for authenticated patient.
        """
        patient = await patient_repository.find_by_user_id(str(user["_id"]))
        
        if not patient:
            return {
                "success": False,
                "error": "Patient profile not found.",
                "status_code": 404,
            }
        
        consultations = await consultation_repository.find_by_patient_id(
            str(patient["_id"])
        )
        
        return {
            "success": True,
            "consultations": consultations,
        }

consultation_service = ConsultationService()