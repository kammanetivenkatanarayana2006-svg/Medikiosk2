"""
OTP repository for database operations.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from bson import ObjectId
from app.db.database import DatabaseRepository
from app.db.connection import mongo_connection
import logging

logger = logging.getLogger(__name__)

class OTPRepository(DatabaseRepository):
    """Repository for OTP-related database operations."""
    
    def __init__(self):
        super().__init__("otp_verifications")
    
    async def create_indexes(self):
        """Create indexes for OTP collection."""
        if not mongo_connection.is_connected:
            return
        
        try:
            collection = mongo_connection.database["otp_verifications"]
            await collection.create_index("user_id")

            # Drop legacy non-TTL "created_at_1" index if present, so the TTL
            # index below can be created without an IndexOptionsConflict.
            for index in await collection.list_indexes().to_list(length=None):
                if index.get("name") == "created_at_1" and "expireAfterSeconds" not in index:
                    logger.info("Dropping legacy non-TTL index 'created_at_1'")
                    await collection.drop_index("created_at_1")
                    break

            await collection.create_index([("created_at", 1)], expireAfterSeconds=600)  # TTL for cleanup
            logger.info("OTP indexes created")
        except Exception as e:
            logger.error(f"Failed to create OTP indexes: {str(e)}")
    
    async def create_otp(
        self,
        user_id: str,
        otp_hash: str,
        purpose: str,
        expires_at: datetime,
        max_attempts: int = 5,
    ) -> Dict[str, Any]:
        """Create OTP record."""
        collection = await self.get_collection()
        if collection is None:
            raise Exception("Database not connected")
        
        otp_doc = {
            "user_id": user_id,
            "otp_hash": otp_hash,
            "purpose": purpose,
            "expires_at": expires_at,
            "attempts": 0,
            "max_attempts": max_attempts,
            "used_at": None,
            "created_at": datetime.now(timezone.utc),
        }
        
        result = await collection.insert_one(otp_doc)
        otp_doc["_id"] = result.inserted_id
        return otp_doc
    
    async def invalidate_previous_otps(self, user_id: str, purpose: str):
        """Invalidate all previous active OTPs."""
        collection = await self.get_collection()
        if collection is None:
            return
        
        await collection.update_many(
            {
                "user_id": user_id,
                "purpose": purpose,
                "used_at": None,
            },
            {
                "$set": {"used_at": datetime.now(timezone.utc)}
            }
        )
    
    async def verify_otp(self, user_id: str, otp_hash: str, purpose: str) -> Dict[str, Any]:
        """Verify OTP for user."""
        collection = await self.get_collection()
        if collection is None:
            return {"success": False, "error": "Database not connected"}
        
        otp_record = await collection.find_one({
            "user_id": user_id,
            "purpose": purpose,
            "used_at": None,
        })
        
        if not otp_record:
            return {"success": False, "error": "No active OTP found. Please request a new code."}
        
        # Check expiry
        expires_at = otp_record.get("expires_at")
        if expires_at and expires_at < datetime.now(timezone.utc):
            return {"success": False, "error": "OTP has expired. Please request a new code."}
        
        # Check attempts
        attempts = otp_record.get("attempts", 0)
        max_attempts = otp_record.get("max_attempts", 5)
        
        if attempts >= max_attempts:
            await self.mark_otp_used(otp_record["_id"])
            return {"success": False, "error": "Maximum attempts exceeded. Please request a new code."}
        
        # Verify OTP hash
        if otp_record.get("otp_hash") != otp_hash:
            # Increment attempts
            await collection.update_one(
                {"_id": otp_record["_id"]},
                {"$inc": {"attempts": 1}}
            )
            return {"success": False, "error": "Invalid OTP. Please try again."}
        
        return {"success": True, "otp_record": otp_record}
    
    async def mark_otp_used(self, otp_id: ObjectId):
        """Mark OTP as used."""
        collection = await self.get_collection()
        if collection is None:
            return
        
        await collection.update_one(
            {"_id": otp_id},
            {"$set": {"used_at": datetime.now(timezone.utc)}}
        )
    
    async def get_latest_otp(self, user_id: str, purpose: str) -> Optional[Dict[str, Any]]:
        """Get latest OTP for user."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        return await collection.find_one(
            {"user_id": user_id, "purpose": purpose},
            sort=[("created_at", -1)]
        )

otp_repository = OTPRepository()