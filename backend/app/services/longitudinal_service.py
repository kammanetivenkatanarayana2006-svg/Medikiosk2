"""
Longitudinal patient history service.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from bson import ObjectId
from app.db.repositories.patient_repository import patient_repository
from app.db.repositories.consultation_repository import consultation_repository
from app.db.repositories.interview_repository import interview_repository
from app.db.repositories.clinical_extraction_repository import clinical_extraction_repository
from app.db.repositories.medical_document_repository import medical_document_repository
from app.db.connection import mongo_connection
import logging

logger = logging.getLogger(__name__)

class LongitudinalHistoryService:
    """Service for longitudinal patient history."""
    
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 50
    
    async def get_patient_history(
        self,
        user: Dict[str, Any],
        page: int = 1,
        page_size: int = 10,
        sort_order: str = "newest_first",
    ) -> Dict[str, Any]:
        """
        Get longitudinal history for authenticated patient.
        """
        # Validate pagination
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = self.DEFAULT_PAGE_SIZE
        if page_size > self.MAX_PAGE_SIZE:
            page_size = self.MAX_PAGE_SIZE
        
        # Get patient
        patient = await patient_repository.find_by_user_id(str(user["_id"]))
        if not patient:
            return {"success": False, "error": "Patient profile not found.", "status_code": 404}
        
        patient_id = str(patient["_id"])
        
        # Get all consultations for patient
        consultations = await self._get_patient_consultations(patient_id)
        
        if not consultations:
            return {
                "success": True,
                "history": {
                    "patient_id": patient_id,
                    "total_consultations": 0,
                    "consultations": [],
                    "timeline": [],
                },
            }
        
        # Sort consultations
        reverse = sort_order == "newest_first"
        consultations.sort(key=lambda c: c.get("created_at", datetime.min.replace(tzinfo=timezone.utc)), reverse=reverse)
        
        # Paginate
        total = len(consultations)
        start = (page - 1) * page_size
        end = start + page_size
        paginated_consultations = consultations[start:end]
        
        # Build consultation summaries
        summaries = []
        timeline_events = []
        
        for consultation in paginated_consultations:
            summary = await self._build_consultation_summary(consultation, patient_id)
            summaries.append(summary)
            
            # Build timeline events for this consultation
            events = await self._build_consultation_events(consultation, patient_id)
            timeline_events.extend(events)
        
        # Sort timeline events chronologically
        timeline_events.sort(key=lambda e: e.get("event_date", datetime.min.replace(tzinfo=timezone.utc)), reverse=reverse)
        
        return {
            "success": True,
            "history": {
                "patient_id": patient_id,
                "total_consultations": total,
                "page": page,
                "page_size": page_size,
                "total_pages": (total + page_size - 1) // page_size,
                "consultations": summaries,
                "timeline": timeline_events,
            },
        }
    
    async def _get_patient_consultations(self, patient_id: str) -> List[Dict[str, Any]]:
        """Get all consultations for patient."""
        collection = mongo_connection.database["consultations"]
        if collection is None:
            return []
        
        try:
            cursor = collection.find({"patient_id": patient_id}).sort("created_at", -1)
            return await cursor.to_list(length=100)
        except Exception as e:
            logger.error(f"Failed to get consultations: {str(e)}")
            return []
    
    async def _build_consultation_summary(
        self,
        consultation: Dict[str, Any],
        patient_id: str,
    ) -> Dict[str, Any]:
        """Build summary for a consultation."""
        consultation_id = str(consultation["_id"])
        
        # Check for clinical history via the interview for this consultation
        interview = await interview_repository.find_by_consultation_id(consultation_id)
        has_clinical_history = False
        if interview:
            extractions = await clinical_extraction_repository.find_by_interview_id(
                str(interview["_id"])
            )
            has_clinical_history = len(extractions) > 0
        
        # Count documents
        documents = await medical_document_repository.find_by_patient_id(patient_id)
        consultation_docs = [d for d in documents if d.get("consultation_id") == consultation_id]
        document_count = len(consultation_docs)
        ocr_completed = sum(1 for d in consultation_docs if d.get("ocr_status") == "completed")
        
        return {
            "id": consultation_id,
            "consultation_type": consultation.get("consultation_type", "general"),
            "language": consultation.get("language", "english"),
            "status": consultation.get("status", "setup"),
            "created_at": consultation.get("created_at"),
            "completed_at": consultation.get("completed_at"),
            "has_clinical_history": has_clinical_history,
            "document_count": document_count,
            "ocr_completed_count": ocr_completed,
        }
    
    async def _build_consultation_events(
        self,
        consultation: Dict[str, Any],
        patient_id: str,
    ) -> List[Dict[str, Any]]:
        """Build timeline events for a consultation."""
        events = []
        consultation_id = str(consultation["_id"])
        
        # Consultation created event
        events.append({
            "event_id": f"consultation_{consultation_id}",
            "patient_id": patient_id,
            "consultation_id": consultation_id,
            "event_type": "consultation_started",
            "event_date": consultation.get("created_at"),
            "title": f"Consultation {consultation.get('consultation_type', 'general').replace('_', ' ').title()}",
            "description": "Consultation initiated",
            "source_type": "consultation",
            "source_id": consultation_id,
        })
        
        # Interview events
        interview = await interview_repository.find_by_consultation_id(consultation_id)
        if interview:
            interview_id = str(interview["_id"])
            
            if interview.get("status") == "completed":
                events.append({
                    "event_id": f"interview_completed_{interview_id}",
                    "patient_id": patient_id,
                    "consultation_id": consultation_id,
                    "event_type": "clinical_history_captured",
                    "event_date": interview.get("completed_at") or interview.get("updated_at"),
                    "title": "Clinical History Captured",
                    "description": "AI-assisted clinical interview completed",
                    "source_type": "interview",
                    "source_id": interview_id,
                })
        
        # Medical document events
        documents = await medical_document_repository.find_by_patient_id(patient_id)
        for doc in documents:
            if doc.get("consultation_id") == consultation_id:
                events.append({
                    "event_id": f"document_{str(doc['_id'])}",
                    "patient_id": patient_id,
                    "consultation_id": consultation_id,
                    "event_type": "medical_document_uploaded",
                    "event_date": doc.get("uploaded_at") or doc.get("created_at"),
                    "title": "Medical Document Uploaded",
                    "description": doc.get("original_filename", "Document"),
                    "source_type": "medical_document",
                    "source_id": str(doc["_id"]),
                })
                
                if doc.get("ocr_status") == "completed":
                    events.append({
                        "event_id": f"ocr_{str(doc['_id'])}",
                        "patient_id": patient_id,
                        "consultation_id": consultation_id,
                        "event_type": "ocr_completed",
                        "event_date": doc.get("updated_at"),
                        "title": "Document Processed",
                        "description": "Text extracted from document",
                        "source_type": "ocr_result",
                        "source_id": str(doc["_id"]),
                    })
        
        return events
    
    async def get_consultation_detail(
        self,
        user: Dict[str, Any],
        consultation_id: str,
    ) -> Dict[str, Any]:
        """
        Get detailed information for a specific consultation.
        """
        # Get consultation
        consultation = await consultation_repository.find_by_id(consultation_id)
        if not consultation:
            return {"success": False, "error": "Consultation not found.", "status_code": 404}
        
        # Verify ownership
        if str(consultation.get("user_id")) != str(user["_id"]):
            return {"success": False, "error": "Access denied.", "status_code": 403}
        
        patient = await patient_repository.find_by_user_id(str(user["_id"]))
        if not patient:
            return {"success": False, "error": "Patient not found.", "status_code": 404}
        
        patient_id = str(patient["_id"])
        
        # Get clinical history
        clinical_history = await self._get_clinical_history(consultation_id)
        
        # Get documents
        documents = await medical_document_repository.find_by_patient_id(patient_id)
        consultation_docs = [d for d in documents if d.get("consultation_id") == consultation_id]
        
        # Build sources
        sources = []
        if clinical_history:
            sources.append({
                "source_type": "clinical_extraction",
                "source_id": consultation_id,
                "recorded_at": clinical_history.get("updated_at"),
            })
        for doc in consultation_docs:
            sources.append({
                "source_type": "medical_document",
                "source_id": str(doc["_id"]),
                "recorded_at": doc.get("uploaded_at"),
            })
            if doc.get("ocr_status") == "completed":
                sources.append({
                    "source_type": "ocr_result",
                    "source_id": str(doc["_id"]),
                    "recorded_at": doc.get("updated_at"),
                })
        
        return {
            "success": True,
            "detail": {
                "id": consultation_id,
                "consultation_type": consultation.get("consultation_type"),
                "language": consultation.get("language"),
                "status": consultation.get("status"),
                "created_at": consultation.get("created_at"),
                "completed_at": consultation.get("completed_at"),
                "clinical_history": clinical_history,
                "documents": [
                    {
                        "id": str(d["_id"]),
                        "original_filename": d.get("original_filename"),
                        "document_type": d.get("document_type"),
                        "ocr_status": d.get("ocr_status"),
                        "file_size": d.get("file_size"),
                        "uploaded_at": d.get("uploaded_at"),
                    }
                    for d in consultation_docs
                ],
                "sources": sources,
                "verification_status": "not_verified",
            },
        }
    
    async def _get_clinical_history(self, consultation_id: str) -> Optional[Dict[str, Any]]:
        """Get aggregated clinical history for consultation."""
        # Find interview for consultation
        interview = await interview_repository.find_by_consultation_id(consultation_id)
        if not interview:
            return None
        
        interview_id = str(interview["_id"])
        
        # Get extractions
        extractions = await clinical_extraction_repository.find_by_interview_id(interview_id)
        
        if not extractions:
            return None
        
        # Aggregate extractions
        aggregated = {}
        for extraction in extractions:
            if extraction.get("status") != "completed":
                continue
            fields = extraction.get("extracted_fields", {})
            for field_name, field_value in fields.items():
                if field_value is not None:
                    if field_name not in aggregated:
                        aggregated[field_name] = field_value
        
        return aggregated

longitudinal_service = LongitudinalHistoryService()