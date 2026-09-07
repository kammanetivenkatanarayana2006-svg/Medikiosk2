"""
Clinical extraction repository.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from bson import ObjectId
from app.db.database import DatabaseRepository
from app.db.connection import mongo_connection
import logging

logger = logging.getLogger(__name__)

class ClinicalExtractionRepository(DatabaseRepository):
    """Repository for clinical extraction records."""
    
    def __init__(self):
        super().__init__("clinical_extractions")
    
    async def create_indexes(self):
        """Create indexes."""
        if not mongo_connection.is_connected:
            return
        
        try:
            collection = mongo_connection.database["clinical_extractions"]
            await collection.create_index("response_id", unique=True)
            await collection.create_index("interview_id")
            await collection.create_index("consultation_id")
            await collection.create_index("patient_id")
            await collection.create_index("status")
            await collection.create_index([("created_at", -1)])
            logger.info("Clinical extraction indexes created")
        except Exception as e:
            logger.error(f"Failed to create clinical extraction indexes: {str(e)}")
    
    async def create_extraction(
        self,
        interview_id: str,
        consultation_id: str,
        patient_id: str,
        response_id: str,
        question_id: str,
        section: str,
        extracted_fields: Dict[str, Any],
        status: str = "completed",
        extraction_version: int = 1,
    ) -> Optional[Dict[str, Any]]:
        """Create extraction record."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        now = datetime.now(timezone.utc)
        
        extraction_doc = {
            "interview_id": interview_id,
            "consultation_id": consultation_id,
            "patient_id": patient_id,
            "response_id": response_id,
            "question_id": question_id,
            "section": section,
            "extracted_fields": extracted_fields,
            "source": "ai_extracted",
            "extraction_version": extraction_version,
            "status": status,
            "created_at": now,
            "updated_at": now,
        }
        
        try:
            result = await collection.insert_one(extraction_doc)
            extraction_doc["_id"] = result.inserted_id
            return extraction_doc
        except Exception as e:
            logger.error(f"Failed to create extraction: {str(e)}")
            return None
    
    async def find_by_response_id(self, response_id: str) -> Optional[Dict[str, Any]]:
        """Find extraction by response ID."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        try:
            return await collection.find_one({"response_id": response_id})
        except Exception:
            return None
    
    async def find_by_interview_id(self, interview_id: str) -> List[Dict[str, Any]]:
        """Find all extractions for an interview."""
        collection = await self.get_collection()
        if collection is None:
            return []
        
        try:
            cursor = collection.find({"interview_id": interview_id}).sort("created_at", 1)
            return await cursor.to_list(length=100)
        except Exception:
            return []
    
    async def update_status(
        self,
        extraction_id: str,
        status: str,
    ) -> bool:
        """Update extraction status."""
        collection = await self.get_collection()
        if collection is None:
            return False
        
        try:
            obj_id = ObjectId(extraction_id)
            result = await collection.update_one(
                {"_id": obj_id},
                {
                    "$set": {
                        "status": status,
                        "updated_at": datetime.now(timezone.utc),
                    }
                }
            )
            return result.modified_count > 0
        except Exception:
            return False

clinical_extraction_repository = ClinicalExtractionRepository()