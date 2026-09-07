"""
Follow-up question repository.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from bson import ObjectId
from app.db.database import DatabaseRepository
from app.db.connection import mongo_connection
import logging

logger = logging.getLogger(__name__)

class FollowUpRepository(DatabaseRepository):
    """Repository for follow-up questions."""
    
    def __init__(self):
        super().__init__("interview_followups")
    
    async def create_indexes(self):
        """Create indexes."""
        if not mongo_connection.is_connected:
            return
        
        try:
            collection = mongo_connection.database["interview_followups"]
            await collection.create_index("interview_id")
            await collection.create_index("consultation_id")
            await collection.create_index("patient_id")
            await collection.create_index("response_id")
            await collection.create_index([("interview_id", 1), ("target_field", 1)], unique=True)
            await collection.create_index([("created_at", -1)])
            logger.info("Follow-up indexes created")
        except Exception as e:
            logger.error(f"Failed to create follow-up indexes: {str(e)}")
    
    async def create_followup(
        self,
        interview_id: str,
        consultation_id: str,
        patient_id: str,
        response_id: str,
        target_field: str,
        question: str,
        language: str,
        source: str,
        status: str = "asked",
    ) -> Optional[Dict[str, Any]]:
        """Create follow-up record."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        now = datetime.now(timezone.utc)
        
        followup_doc = {
            "interview_id": interview_id,
            "consultation_id": consultation_id,
            "patient_id": patient_id,
            "response_id": response_id,
            "target_field": target_field,
            "question": question,
            "language": language,
            "source": source,
            "status": status,
            "created_at": now,
            "updated_at": now,
        }
        
        try:
            result = await collection.insert_one(followup_doc)
            followup_doc["_id"] = result.inserted_id
            return followup_doc
        except Exception as e:
            logger.error(f"Failed to create follow-up: {str(e)}")
            return None
    
    async def find_by_interview_and_field(
        self,
        interview_id: str,
        target_field: str,
    ) -> Optional[Dict[str, Any]]:
        """Find existing follow-up for interview and field."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        try:
            return await collection.find_one({
                "interview_id": interview_id,
                "target_field": target_field,
            })
        except Exception:
            return None
    
    async def get_asked_fields(self, interview_id: str) -> List[str]:
        """Get list of target fields already asked."""
        collection = await self.get_collection()
        if collection is None:
            return []
        
        try:
            cursor = collection.find({"interview_id": interview_id})
            followups = await cursor.to_list(length=50)
            return [f.get("target_field", "") for f in followups if f.get("target_field")]
        except Exception:
            return []
    
    async def get_followup_count(self, interview_id: str) -> int:
        """Get total follow-ups for interview."""
        collection = await self.get_collection()
        if collection is None:
            return 0
        
        try:
            return await collection.count_documents({"interview_id": interview_id})
        except Exception:
            return 0

follow_up_repository = FollowUpRepository()