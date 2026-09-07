"""
User repository for database operations.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from app.db.database import DatabaseRepository, DatabaseUnavailableError
from app.db.connection import mongo_connection
from app.utils.security import security_utils
import logging

logger = logging.getLogger(__name__)

class UserRepository(DatabaseRepository):
    """Repository for user-related database operations."""
    
    def __init__(self):
        super().__init__("users")
    
    async def create_indexes(self):
        """Create unique indexes for email and phone."""
        if not mongo_connection.is_connected:
            logger.warning("Cannot create indexes: database not connected")
            return
        
        try:
            collection = mongo_connection.database["users"]
            await collection.create_index("email", unique=True)
            await collection.create_index("phone", unique=True)
            logger.info("User indexes created successfully")
        except Exception as e:
            logger.error(f"Failed to create user indexes: {str(e)}")
    
    async def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Find user by normalized email."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        normalized_email = email.strip().lower()
        user = await collection.find_one({"email": normalized_email})
        return user
    
    async def find_by_phone(self, phone: str) -> Optional[Dict[str, Any]]:
        """Find user by normalized phone."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        normalized_phone = ''.join(filter(str.isdigit, phone))
        user = await collection.find_one({"phone": normalized_phone})
        return user
    
    async def find_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Find user by ID."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        try:
            obj_id = ObjectId(user_id)
            user = await collection.find_one({"_id": obj_id})
            return user
        except Exception:
            return None
    
    async def create_user(
        self,
        full_name: str,
        email: str,
        phone: str,
        password: str,
        role: str = "PATIENT",
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new user with hashed password.
        Returns created user or None if duplicate.
        """
        collection = await self.get_collection()
        if collection is None:
            raise DatabaseUnavailableError("Database not connected")
        
        # Normalize inputs
        normalized_email = email.strip().lower()
        normalized_phone = ''.join(filter(str.isdigit, phone))
        password_hash = security_utils.hash_password(password)
        
        now = datetime.now(timezone.utc)
        
        user_doc = {
            "full_name": full_name.strip(),
            "email": normalized_email,
            "phone": normalized_phone,
            "password_hash": password_hash,
            "role": role.upper(),
            "email_verified": False,
            "phone_verified": False,
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        }
        
        try:
            result = await collection.insert_one(user_doc)
            user_doc["_id"] = result.inserted_id
            return user_doc
        except DuplicateKeyError as e:
            logger.warning(f"Duplicate user registration attempt: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Failed to create user: {str(e)}")
            raise
    async def update_user(self, user_id: str, update_data: Dict[str, Any]) -> bool:
        """Update user fields."""
        collection = await self.get_collection()
        if collection is None:
            return False
        
        try:
            obj_id = ObjectId(user_id)
            update_data["updated_at"] = datetime.now(timezone.utc)
            
            result = await collection.update_one(
                {"_id": obj_id},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to update user: {str(e)}")
            return False
    
    async def verify_credentials(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Verify user credentials.
        Returns user document if valid, None otherwise.
        """
        user = await self.find_by_email(email)
        if not user:
            return None
        
        if not user.get("is_active", True):
            return None
        
        password_hash = user.get("password_hash", "")
        if not security_utils.verify_password(password, password_hash):
            return None
        
        return user
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        return await self.find_by_id(user_id)
    

user_repository = UserRepository()