"""
Interview repository for database operations.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from bson import ObjectId
from app.db.database import DatabaseRepository
from app.db.connection import mongo_connection
import logging

logger = logging.getLogger(__name__)

class InterviewRepository(DatabaseRepository):
    """Repository for interview-related database operations."""
    
    def __init__(self):
        super().__init__("interview_sessions")
    
    async def create_indexes(self):
        """Create indexes for interview sessions."""
        if not mongo_connection.is_connected:
            return
        
        try:
            collection = mongo_connection.database["interview_sessions"]
            await collection.create_index("consultation_id", unique=True)
            await collection.create_index("patient_id")
            await collection.create_index("user_id")
            await collection.create_index("status")
            await collection.create_index([("created_at", -1)])
            
            # Response collection indexes
            responses = mongo_connection.database["interview_responses"]
            await responses.create_index("interview_id")
            await responses.create_index("question_id")
            await responses.create_index([("interview_id", 1), ("question_id", 1)], unique=True)
            
            logger.info("Interview indexes created")
        except Exception as e:
            logger.error(f"Failed to create interview indexes: {str(e)}")
    
    async def create_interview(
        self,
        consultation_id: str,
        patient_id: str,
        user_id: str,
        language: str,
        consultation_type: str,
        current_section: str = "introduction",
        current_question_id: str = "intro_01",
        status: str = "ready",
    ) -> Optional[Dict[str, Any]]:
        """Create interview session."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        now = datetime.now(timezone.utc)
        
        interview_doc = {
            "consultation_id": consultation_id,
            "patient_id": patient_id,
            "user_id": user_id,
            "language": language,
            "consultation_type": consultation_type,
            "current_section": current_section,
            "current_question_id": current_question_id,
            "status": status,
            "progress": 0.0,
            "started_at": None,
            "completed_at": None,
            "created_at": now,
            "updated_at": now,
        }
        
        try:
            result = await collection.insert_one(interview_doc)
            interview_doc["_id"] = result.inserted_id
            return interview_doc
        except Exception as e:
            logger.error(f"Failed to create interview: {str(e)}")
            return None
    
    async def find_by_id(self, interview_id: str) -> Optional[Dict[str, Any]]:
        """Find interview by ID."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        try:
            obj_id = ObjectId(interview_id)
            return await collection.find_one({"_id": obj_id})
        except Exception:
            return None
    
    async def find_by_consultation_id(self, consultation_id: str) -> Optional[Dict[str, Any]]:
        """Find interview by consultation ID."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        try:
            return await collection.find_one({"consultation_id": consultation_id})
        except Exception:
            return None
    
    async def update_interview(
        self,
        interview_id: str,
        update_data: Dict[str, Any],
    ) -> bool:
        """Update interview."""
        collection = await self.get_collection()
        if collection is None:
            return False
        
        try:
            obj_id = ObjectId(interview_id)
            update_data["updated_at"] = datetime.now(timezone.utc)
            result = await collection.update_one(
                {"_id": obj_id},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to update interview: {str(e)}")
            return False
    
    async def save_response(
        self,
        interview_id: str,
        question_id: str,
        response_text: str,
        input_method: str,
        language: str,
        section: str,
    ) -> Optional[Dict[str, Any]]:
        """Save interview response."""
        collection = mongo_connection.database["interview_responses"]
        if collection is None:
            return None
        
        now = datetime.now(timezone.utc)
        
        response_doc = {
            "interview_id": interview_id,
            "question_id": question_id,
            "response_text": response_text,
            "input_method": input_method,
            "language": language,
            "section": section,
            "answered_at": now,
        }
        
        try:
            result = await collection.insert_one(response_doc)
            response_doc["_id"] = result.inserted_id
            return response_doc
        except Exception as e:
            logger.error(f"Failed to save response: {str(e)}")
            return None
    
    async def get_responses(self, interview_id: str) -> List[Dict[str, Any]]:
        """Get all responses for interview."""
        collection = mongo_connection.database["interview_responses"]
        if collection is None:
            return []
        
        try:
            cursor = collection.find({"interview_id": interview_id}).sort("answered_at", 1)
            return await cursor.to_list(length=100)
        except Exception:
            return []
    
    async def has_response(self, interview_id: str, question_id: str) -> bool:
        """Check if response exists for question."""
        collection = mongo_connection.database["interview_responses"]
        if collection is None:
            return False
        
        try:
            count = await collection.count_documents({
                "interview_id": interview_id,
                "question_id": question_id,
            })
            return count > 0
        except Exception:
            return False

interview_repository = InterviewRepository()