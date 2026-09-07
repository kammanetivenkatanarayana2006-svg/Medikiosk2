"""
Verification token repository.
"""
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from bson import ObjectId
from app.db.database import DatabaseRepository
from app.db.connection import mongo_connection
import logging

logger = logging.getLogger(__name__)

class VerificationTokenRepository(DatabaseRepository):
    """Repository for verification tokens."""
    
    def __init__(self):
        super().__init__("verification_tokens")
    
    async def create_indexes(self):
        """Create indexes for verification tokens."""
        if not mongo_connection.is_connected:
            return
        
        try:
            collection = mongo_connection.database["verification_tokens"]
            await collection.create_index("user_id")
            await collection.create_index("token_hash")
            await collection.create_index([("created_at", 1)], expireAfterSeconds=86400)  # 24h TTL
            logger.info("Verification token indexes created")
        except Exception as e:
            logger.error(f"Failed to create verification token indexes: {str(e)}")
    
    async def create_token(
        self,
        user_id: str,
        token_hash: str,
        purpose: str,
        expires_at: datetime,
    ) -> Dict[str, Any]:
        """Create verification token."""
        collection = await self.get_collection()
        if collection is None:
            raise Exception("Database not connected")
        
        token_doc = {
            "user_id": user_id,
            "token_hash": token_hash,
            "purpose": purpose,
            "expires_at": expires_at,
            "used_at": None,
            "created_at": datetime.now(timezone.utc),
        }
        
        result = await collection.insert_one(token_doc)
        token_doc["_id"] = result.inserted_id
        return token_doc
    
    async def invalidate_previous_tokens(self, user_id: str, purpose: str):
        """Invalidate previous active tokens."""
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
    
    async def verify_token(self, token_hash: str, purpose: str) -> Dict[str, Any]:
        """Verify token."""
        collection = await self.get_collection()
        if collection is None:
            return {"success": False, "error": "Database not connected"}
        
        token_record = await collection.find_one({
            "token_hash": token_hash,
            "purpose": purpose,
            "used_at": None,
        })
        
        if not token_record:
            return {"success": False, "error": "Invalid verification token."}
        
        # Check expiry
        expires_at = token_record.get("expires_at")
        if expires_at and expires_at < datetime.now(timezone.utc):
            return {"success": False, "error": "Verification link has expired."}
        
        return {"success": True, "token_record": token_record}
    
    async def mark_token_used(self, token_id: ObjectId):
        """Mark token as used."""
        collection = await self.get_collection()
        if collection is None:
            return
        
        await collection.update_one(
            {"_id": token_id},
            {"$set": {"used_at": datetime.now(timezone.utc)}}
        )

verification_token_repository = VerificationTokenRepository()