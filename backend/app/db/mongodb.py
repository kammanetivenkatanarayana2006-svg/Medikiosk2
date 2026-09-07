from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional, Dict, Any
import logging
from contextlib import asynccontextmanager
from app.core.config import settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Manages MongoDB connection lifecycle and provides database access.
    Implements connection pooling and graceful degradation.
    """
    
    def __init__(self):
        self._client: Optional[AsyncIOMotorClient] = None
        self._database: Optional[AsyncIOMotorDatabase] = None
        self._connected: bool = False
    
    async def connect(self) -> bool:
        """
        Establish database connection if configured.
        Returns True if connected successfully, False otherwise.
        """
        if not settings.database_enabled:
            logger.info("MongoDB not configured. Application will run without database.")
            return False
        
        try:
            self._client = AsyncIOMotorClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=10,
                minPoolSize=1,
                retryWrites=True,
            )
            # Test connection
            await self._client.admin.command('ping')
            self._database = self._client[settings.DATABASE_NAME]
            self._connected = True
            logger.info(f"Connected to MongoDB database: {settings.DATABASE_NAME}")
            return True
        except Exception as e:
            logger.warning(f"Failed to connect to MongoDB: {e}")
            self._connected = False
            return False
    
    async def disconnect(self):
        """Close database connection gracefully."""
        if self._client:
            self._client.close()
            self._client = None
            self._database = None
            self._connected = False
            logger.info("MongoDB connection closed")
    
    @property
    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self._connected
    
    @property
    def database(self) -> Optional[AsyncIOMotorDatabase]:
        """Get database instance if connected."""
        return self._database
    
    async def get_collection(self, name: str):
        """
        Get a collection by name.
        Returns None if database is not connected.
        """
        if not self._connected or not self._database:
            logger.warning(f"Cannot get collection '{name}': database not connected")
            return None
        return self._database[name]
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Comprehensive database health check.
        """
        if not settings.database_enabled:
            return {
                "status": "not_configured",
                "message": "MongoDB URI not configured"
            }
        
        if not self._connected:
            return {
                "status": "disconnected",
                "message": "Database connection failed or not established"
            }
        
        try:
            await self._client.admin.command('ping')
            return {
                "status": "connected",
                "database": settings.DATABASE_NAME,
                "message": "Database is healthy"
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "message": f"Database health check failed: {str(e)}"
            }

# Global database manager instance
db_manager = DatabaseManager()

async def get_database() -> Optional[AsyncIOMotorDatabase]:
    """Dependency for FastAPI to get database instance."""
    return db_manager.database

async def get_database_status() -> str:
    """Get database connection status for health checks."""
    if not settings.database_enabled:
        return "not_configured"
    if db_manager.is_connected:
        return "connected"
    return "disconnected"

@asynccontextmanager
async def get_db_session():
    """
    Context manager for database sessions.
    Ensures proper connection lifecycle.
    """
    if not db_manager.is_connected:
        await db_manager.connect()
    try:
        yield db_manager.database
    finally:
        # Connection pooling handles cleanup automatically
        pass