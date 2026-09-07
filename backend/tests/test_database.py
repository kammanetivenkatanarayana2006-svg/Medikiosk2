"""
Tests for database foundation.
These tests verify database connection handling and health checks.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from app.main import app
from app.db.connection import mongo_connection
from app.core.config import settings

client = TestClient(app=app)

class TestDatabaseFoundation:
    """Test database foundation functionality."""
    
    def test_configuration_loading(self):
        """Test database configuration is loaded."""
        assert hasattr(settings, 'MONGODB_URI')
        assert hasattr(settings, 'DATABASE_NAME')
        assert settings.DATABASE_NAME == "medikiosk"
    
    def test_database_module_import(self):
        """Test database module imports correctly."""
        from app.db.connection import mongo_connection
        from app.db.database import DatabaseRepository, get_db
        assert mongo_connection is not None
        assert DatabaseRepository is not None
        assert get_db is not None
    
    @pytest.mark.asyncio
    async def test_database_not_configured(self):
        """Test behavior when database is not configured."""
        # Save original setting
        original_uri = settings.MONGODB_URI
        settings.MONGODB_URI = None
        
        result = await mongo_connection.connect()
        assert result is False
        assert mongo_connection.is_connected is False
        
        # Restore setting
        settings.MONGODB_URI = original_uri
    
    @pytest.mark.asyncio
    async def test_database_health_check_not_configured(self):
        """Test health check when database not configured."""
        original_uri = settings.MONGODB_URI
        settings.MONGODB_URI = None
        
        health = await mongo_connection.health_check()
        assert health["status"] == "not_configured"
        
        settings.MONGODB_URI = original_uri
    
    def test_health_endpoint(self):
        """Test health endpoint returns correct structure."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "database" in data
        assert "status" in data["database"]
    
    def test_api_info_endpoint(self):
        """Test API info endpoint."""
        response = client.get("/api/")
        assert response.status_code == 200
        data = response.json()
        assert "database" in data
    
    @pytest.mark.asyncio
    async def test_connection_lifecycle(self):
        """Test database connection lifecycle."""
        # Test disconnect when not connected
        await mongo_connection.disconnect()
        assert mongo_connection.is_connected is False

class TestObjectIdHandling:
    """Test ObjectId handling."""
    
    def test_create_object_id(self):
        """Test ObjectId creation."""
        from app.utils.object_id import object_id_handler
        obj_id = object_id_handler.create()
        assert obj_id is not None
    
    def test_parse_valid_object_id(self):
        """Test parsing valid ObjectId."""
        from app.utils.object_id import object_id_handler
        from bson import ObjectId
        
        obj_id = ObjectId()
        parsed = object_id_handler.parse(str(obj_id))
        assert parsed == obj_id
    
    def test_parse_invalid_object_id(self):
        """Test parsing invalid ObjectId."""
        from app.utils.object_id import object_id_handler
        
        result = object_id_handler.parse("invalid_id")
        assert result is None
    
    def test_validate_object_id(self):
        """Test ObjectId validation."""
        from app.utils.object_id import object_id_handler
        from bson import ObjectId
        
        assert object_id_handler.validate(ObjectId()) is True
        assert object_id_handler.validate("invalid") is False