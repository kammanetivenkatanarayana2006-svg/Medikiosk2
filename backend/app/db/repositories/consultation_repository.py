"""
Consultation repository for database operations.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from bson import ObjectId
from app.db.database import DatabaseRepository
from app.db.connection import mongo_connection
import logging

logger = logging.getLogger(__name__)

class ConsultationRepository(DatabaseRepository):
    """Repository for consultation-related database operations."""
    
    def __init__(self):
        super().__init__("consultations")
    
    async def create_indexes(self):
        """Create indexes for consultations collection."""
        if not mongo_connection.is_connected:
            return
        
        try:
            collection = mongo_connection.database["consultations"]
            await collection.create_index("patient_id")
            await collection.create_index("user_id")
            await collection.create_index("status")
            await collection.create_index([("created_at", -1)])
            logger.info("Consultation indexes created")
        except Exception as e:
            logger.error(f"Failed to create consultation indexes: {str(e)}")
    
    async def create_consultation(
        self,
        user_id: str,
        patient_id: str,
        language: str,
        consultation_type: str,
        consent_given: bool,
        consent_timestamp: datetime,
        status: str = "setup",
    ) -> Optional[Dict[str, Any]]:
        """Create consultation setup record."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        now = datetime.now(timezone.utc)
        
        consultation_doc = {
            "user_id": user_id,
            "patient_id": patient_id,
            "language": language,
            "consultation_type": consultation_type,
            "consent_given": consent_given,
            "consent_timestamp": consent_timestamp,
            "status": status,
            "created_at": now,
            "updated_at": now,
        }
        
        try:
            result = await collection.insert_one(consultation_doc)
            consultation_doc["_id"] = result.inserted_id
            return consultation_doc
        except Exception as e:
            logger.error(f"Failed to create consultation: {str(e)}")
            return None
    
    async def find_by_id(self, consultation_id: str) -> Optional[Dict[str, Any]]:
        """Find consultation by ID."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        try:
            obj_id = ObjectId(consultation_id)
            return await collection.find_one({"_id": obj_id})
        except Exception:
            return None
    
    async def find_by_patient_id(self, patient_id: str) -> List[Dict[str, Any]]:
        """Find consultations by patient ID."""
        collection = await self.get_collection()
        if collection is None:
            return []
        
        try:
            cursor = collection.find({"patient_id": patient_id}).sort("created_at", -1)
            return await cursor.to_list(length=50)
        except Exception as e:
            logger.error(f"Failed to find consultations: {str(e)}")
            return []
    
    async def update_status(
        self,
        consultation_id: str,
        status: str,
    ) -> bool:
        """Update consultation status."""
        collection = await self.get_collection()
        if collection is None:
            return False
        
        try:
            obj_id = ObjectId(consultation_id)
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
        except Exception as e:
            logger.error(f"Failed to update consultation status: {str(e)}")
            return False

consultation_repository = ConsultationRepository()