"""
Database-specific error handling utilities.
"""
import logging
from typing import Dict, Any, Optional
from pymongo.errors import (
    PyMongoError,
    ConnectionFailure,
    ServerSelectionTimeoutError,
    OperationFailure,
    DuplicateKeyError,
    InvalidOperation,
    ConfigurationError,
)

logger = logging.getLogger(__name__)

class DatabaseErrorHandler:
    """
    Handles MongoDB errors and converts them to user-friendly messages.
    """
    
    ERROR_MAPPINGS = {
        ConnectionFailure: "Database connection failed",
        ServerSelectionTimeoutError: "Database server not reachable",
        OperationFailure: "Database operation failed",
        DuplicateKeyError: "Duplicate entry found",
        InvalidOperation: "Invalid database operation",
        ConfigurationError: "Database configuration error",
    }
    
    @classmethod
    def get_user_message(cls, error: Exception) -> str:
        """
        Get user-friendly error message for database errors.
        Never exposes internal details.
        """
        if isinstance(error, PyMongoError):
            for error_type, message in cls.ERROR_MAPPINGS.items():
                if isinstance(error, error_type):
                    return message
            return "Database error occurred"
        
        return "Unexpected error occurred"
    
    @classmethod
    def log_error(cls, error: Exception, context: Optional[Dict[str, Any]] = None):
        """
        Log database errors safely without exposing sensitive information.
        """
        error_info = {
            "error_type": type(error).__name__,
            "error_message": str(error),
        }
        
        if context:
            error_info["context"] = context
        
        # Log error without sensitive data
        logger.error(f"Database error: {error_info}")
    
    @classmethod
    def handle_error(cls, error: Exception) -> Dict[str, Any]:
        """
        Handle database error and return safe response.
        """
        cls.log_error(error)
        
        return {
            "success": False,
            "error": {
                "code": "DATABASE_ERROR",
                "message": cls.get_user_message(error),
            }
        }

# Global instance
db_error_handler = DatabaseErrorHandler()