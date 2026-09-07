"""
AYUSH clinical record repository.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from bson import ObjectId
from app.db.database import DatabaseRepository
from app.db.connection import mongo_connection
import logging

logger = logging.getLogger(__name__)

class AYUSHRepository(DatabaseRepository):
    """Repository for AYUSH clinical records."""
    
    def __init__(self):
        super().__init__("ayush_clinical_records")
    
    async def create_indexes(self):
        """Create indexes."""
        if not mongo_connection.is_connected:
            return
        
        try:
            collection = mongo_connection.database["ayush_clinical_records"]
            await collection.create_index("consultation_id", unique=True)
            await collection.create_index("patient_id")
            await collection.create_index("user_id")
            await collection.create_index([("created_at", -1)])
            logger.info("AYUSH indexes created")
        except Exception as e:
            logger.error(f"Failed to create AYUSH indexes: {str(e)}")
    
    async def find_by_consultation_id(self, consultation_id: str) -> Optional[Dict[str, Any]]:
        """Find AYUSH record by consultation ID."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        try:
            return await collection.find_one({"consultation_id": consultation_id})
        except Exception:
            return None
    
    async def find_by_patient_id(self, patient_id: str) -> List[Dict[str, Any]]:
        """Find AYUSH records by patient ID."""
        collection = await self.get_collection()
        if collection is None:
            return []
        
        try:
            cursor = collection.find({"patient_id": patient_id}).sort("created_at", -1)
            return await cursor.to_list(length=50)
        except Exception:
            return []
    
    async def create_record(
        self,
        patient_id: str,
        consultation_id: str,
        user_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Create AYUSH record."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        now = datetime.now(timezone.utc)
        
        record = {
            "patient_id": patient_id,
            "consultation_id": consultation_id,
            "user_id": user_id,
            "prakriti": None,
            "vikriti": None,
            "agni": None,
            "koshtha": None,
            "ahara": None,
            "vihara": None,
            "nidra": None,
            "dashavidha_pariksha": None,
            "additional_information": None,
            "status": "draft",
            "created_at": now,
            "updated_at": now,
        }
        
        try:
            result = await collection.insert_one(record)
            record["_id"] = result.inserted_id
            return record
        except Exception as e:
            logger.error(f"Failed to create AYUSH record: {str(e)}")
            return None
    
    async def update_record(
        self,
        consultation_id: str,
        update_data: Dict[str, Any],
    ) -> bool:
        """Update AYUSH record."""
        collection = await self.get_collection()
        if collection is None:
            return False
        
        try:
            update_data["updated_at"] = datetime.now(timezone.utc)
            result = await collection.update_one(
                {"consultation_id": consultation_id},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to update AYUSH record: {str(e)}")
            return False

ayush_repository = AYUSHRepository()