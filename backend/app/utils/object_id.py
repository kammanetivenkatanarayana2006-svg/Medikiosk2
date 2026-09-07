"""
ObjectId handling utilities for MongoDB.
"""
from bson import ObjectId
from bson.errors import InvalidId
from typing import Optional, Union, Any
import logging

logger = logging.getLogger(__name__)

class ObjectIdHandler:
    """
    Handles MongoDB ObjectId operations safely.
    """
    
    @staticmethod
    def create() -> ObjectId:
        """Create a new ObjectId."""
        return ObjectId()
    
    @staticmethod
    def parse(value: Union[str, ObjectId]) -> Optional[ObjectId]:
        """
        Safely parse a value to ObjectId.
        Returns None if invalid.
        """
        if isinstance(value, ObjectId):
            return value
        
        if isinstance(value, str):
            try:
                return ObjectId(value)
            except InvalidId:
                logger.warning(f"Invalid ObjectId format: {value}")
                return None
        
        return None
    
    @staticmethod
    def to_str(value: Union[str, ObjectId]) -> str:
        """
        Convert ObjectId to string representation.
        """
        if isinstance(value, ObjectId):
            return str(value)
        return str(value)
    
    @staticmethod
    def validate(value: Any) -> bool:
        """
        Check if a value is a valid ObjectId.
        """
        if isinstance(value, ObjectId):
            return True
        if isinstance(value, str):
            try:
                ObjectId(value)
                return True
            except InvalidId:
                return False
        return False

# Global instance
object_id_handler = ObjectIdHandler()

def parse_object_id(value: Any) -> Optional[ObjectId]:
    """Utility function to parse ObjectId."""
    return object_id_handler.parse(value)