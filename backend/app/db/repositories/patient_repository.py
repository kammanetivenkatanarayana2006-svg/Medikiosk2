"""
Patient repository for database operations.
"""
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from bson import ObjectId
from app.db.database import DatabaseRepository
from app.db.connection import mongo_connection
import logging

logger = logging.getLogger(__name__)

class PatientRepository(DatabaseRepository):
    """Repository for patient-related database operations."""
    
    def __init__(self):
        super().__init__("patients")
    
    async def create_indexes(self):
        """Create indexes for patients collection."""
        if not mongo_connection.is_connected:
            return
        
        try:
            collection = mongo_connection.database["patients"]
            await collection.create_index("user_id", unique=True)
            await collection.create_index("email", unique=True)
            await collection.create_index("phone", unique=True)
            logger.info("Patient indexes created")
        except Exception as e:
            logger.error(f"Failed to create patient indexes: {str(e)}")
    
    async def find_by_user_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Find patient by user ID."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        try:
            return await collection.find_one({"user_id": user_id})
        except Exception:
            return None
    
    async def find_by_id(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Find patient by ID."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        try:
            obj_id = ObjectId(patient_id)
            return await collection.find_one({"_id": obj_id})
        except Exception:
            return None
    
    async def create_patient(
        self,
        user_id: str,
        full_name: str,
        email: str,
        phone: str,
        gender: str,
        age: Optional[int] = None,
        date_of_birth: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Create patient profile."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        now = datetime.now(timezone.utc)
        
        patient_doc = {
            "user_id": user_id,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "gender": gender,
            "age": age,
            "date_of_birth": date_of_birth,
            "photo_reference": None,
            "photo_consent": False,
            "created_at": now,
            "updated_at": now,
        }
        
        try:
            result = await collection.insert_one(patient_doc)
            patient_doc["_id"] = result.inserted_id
            return patient_doc
        except Exception as e:
            logger.error(f"Failed to create patient: {str(e)}")
            return None
    
    async def update_patient(
        self,
        patient_id: str,
        update_data: Dict[str, Any],
    ) -> bool:
        """Update patient profile."""
        collection = await self.get_collection()
        if collection is None:
            return False
        
        try:
            obj_id = ObjectId(patient_id)
            update_data["updated_at"] = datetime.now(timezone.utc)
            
            result = await collection.update_one(
                {"_id": obj_id},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to update patient: {str(e)}")
            return False
    
    async def update_photo_reference(
        self,
        patient_id: str,
        photo_reference: str,
        photo_consent: bool = True,
    ) -> bool:
        """Update patient photo reference."""
        return await self.update_patient(
            patient_id,
            {
                "photo_reference": photo_reference,
                "photo_consent": photo_consent,
            }
        )
    
    async def delete_photo(self, patient_id: str) -> bool:
        """Delete patient photo reference."""
        return await self.update_patient(
            patient_id,
            {
                "photo_reference": None,
                "photo_consent": False,
            }
        )

patient_repository = PatientRepository()