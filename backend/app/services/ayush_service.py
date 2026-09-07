"""
AYUSH clinical information service.
"""
from typing import Optional, Dict, Any
from app.db.repositories.ayush_repository import ayush_repository
from app.db.repositories.consultation_repository import consultation_repository
from app.db.repositories.patient_repository import patient_repository
from app.models.ayush import AYUSHUpdate
import logging

logger = logging.getLogger(__name__)

class AYUSHService:
    """Service for AYUSH clinical information."""
    
    @staticmethod
    async def get_ayush_record(
        user: Dict[str, Any],
        consultation_id: str,
    ) -> Dict[str, Any]:
        """Get AYUSH record for consultation."""
        # Verify consultation ownership
        consultation = await consultation_repository.find_by_id(consultation_id)
        if not consultation:
            return {"success": False, "error": "Consultation not found.", "status_code": 404}
        
        if str(consultation.get("user_id")) != str(user["_id"]):
            return {"success": False, "error": "Access denied.", "status_code": 403}
        
        # Get or create AYUSH record
        record = await ayush_repository.find_by_consultation_id(consultation_id)
        
        if not record:
            patient = await patient_repository.find_by_user_id(str(user["_id"]))
            if not patient:
                return {"success": False, "error": "Patient not found.", "status_code": 404}
            
            record = await ayush_repository.create_record(
                patient_id=str(patient["_id"]),
                consultation_id=consultation_id,
                user_id=str(user["_id"]),
            )
            
            if not record:
                return {"success": False, "error": "Failed to create AYUSH record.", "status_code": 500}
        
        return {"success": True, "record": record}
    
    @staticmethod
    async def update_ayush_record(
        user: Dict[str, Any],
        consultation_id: str,
        update_data: AYUSHUpdate,
    ) -> Dict[str, Any]:
        """Update AYUSH record."""
        # Verify ownership
        consultation = await consultation_repository.find_by_id(consultation_id)
        if not consultation:
            return {"success": False, "error": "Consultation not found.", "status_code": 404}
        
        if str(consultation.get("user_id")) != str(user["_id"]):
            return {"success": False, "error": "Access denied.", "status_code": 403}
        
        # Get or create record
        record = await ayush_repository.find_by_consultation_id(consultation_id)
        
        if not record:
            patient = await patient_repository.find_by_user_id(str(user["_id"]))
            if not patient:
                return {"success": False, "error": "Patient not found.", "status_code": 404}
            
            record = await ayush_repository.create_record(
                patient_id=str(patient["_id"]),
                consultation_id=consultation_id,
                user_id=str(user["_id"]),
            )
            if not record:
                return {"success": False, "error": "Failed to create AYUSH record.", "status_code": 500}
        
        # Build update dict
        update_dict = {}
        
        if update_data.prakriti is not None:
            update_dict["prakriti"] = {
                "value": update_data.prakriti,
                "source_type": update_data.source_type,
                "verified": False,
            }
        
        if update_data.vikriti is not None:
            update_dict["vikriti"] = {
                "value": update_data.vikriti,
                "source_type": update_data.source_type,
                "verified": False,
            }
        
        if update_data.agni is not None:
            update_dict["agni"] = {
                "value": update_data.agni,
                "source_type": update_data.source_type,
                "verified": False,
            }
        
        if update_data.koshtha is not None:
            update_dict["koshtha"] = {
                "value": update_data.koshtha,
                "source_type": update_data.source_type,
                "verified": False,
            }
        
        if update_data.ahara is not None:
            update_dict["ahara"] = {
                "value": update_data.ahara,
                "source_type": update_data.source_type,
                "verified": False,
            }
        
        if update_data.vihara is not None:
            update_dict["vihara"] = {
                "value": update_data.vihara,
                "source_type": update_data.source_type,
                "verified": False,
            }
        
        if update_data.nidra is not None:
            update_dict["nidra"] = {
                "value": update_data.nidra,
                "source_type": update_data.source_type,
                "verified": False,
            }
        
        if update_data.dashavidha_pariksha is not None:
            update_dict["dashavidha_pariksha"] = update_data.dashavidha_pariksha.model_dump(exclude_none=True)
        
        if update_data.additional_information is not None:
            update_dict["additional_information"] = {
                "value": update_data.additional_information,
                "source_type": update_data.source_type,
                "verified": False,
            }
        
        if not update_dict:
            return {"success": True, "message": "No changes", "record": record}
        
        success = await ayush_repository.update_record(consultation_id, update_dict)
        
        if not success:
            return {"success": False, "error": "Failed to update AYUSH record.", "status_code": 500}
        
        updated_record = await ayush_repository.find_by_consultation_id(consultation_id)
        return {"success": True, "message": "AYUSH record updated", "record": updated_record}

ayush_service = AYUSHService()