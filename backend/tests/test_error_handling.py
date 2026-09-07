"""
Tests for database error handling.
"""
import pytest
from app.utils.database_errors import DatabaseErrorHandler
from pymongo.errors import ConnectionFailure, OperationFailure

class TestDatabaseErrorHandling:
    """Test database error handling."""
    
    def test_connection_failure_message(self):
        """Test connection failure error message."""
        error = ConnectionFailure("Connection refused")
        message = DatabaseErrorHandler.get_user_message(error)
        assert message == "Database connection failed"
    
    def test_operation_failure_message(self):
        """Test operation failure error message."""
        error = OperationFailure("Operation failed")
        message = DatabaseErrorHandler.get_user_message(error)
        assert message == "Database operation failed"
    
    def test_generic_error_message(self):
        """Test generic error message."""
        error = Exception("Some error")
        message = DatabaseErrorHandler.get_user_message(error)
        assert message == "Unexpected error occurred"
    
    def test_error_response_format(self):
        """Test error response format."""
        error = ConnectionFailure("Connection refused")
        response = DatabaseErrorHandler.handle_error(error)
        assert response["success"] is False
        assert "error" in response
        assert "code" in response["error"]
        assert "message" in response["error"]