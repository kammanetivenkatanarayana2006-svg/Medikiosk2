"""
MongoDB connection management module.
Handles client lifecycle, connection pooling, and graceful degradation.
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional, Dict, Any
import logging
import time
from contextlib import asynccontextmanager
from app.core.config import settings

logger = logging.getLogger(__name__)

class MongoConnection:
    """
    Manages MongoDB connection lifecycle.
    Implements singleton pattern for connection reuse.
    """
    
    _instance = None
    _client: Optional[AsyncIOMotorClient] = None
    _database: Optional[AsyncIOMotorDatabase] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def connect(self) -> bool:
        """
        Establish MongoDB connection if configured.
        Returns True if connected successfully.
        """
        if not settings.MONGODB_URI:
            logger.info("MongoDB URI not configured. Running without database.")
            return False
        
        try:
            logger.info(f"Attempting MongoDB connection to database: {settings.DATABASE_NAME}")
            
            self._client = AsyncIOMotorClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=10,
                minPoolSize=1,
                retryWrites=True,
                retryReads=True,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000,
            )
            
            # Test connection
            await self._client.admin.command('ping')
            
            self._database = self._client[settings.DATABASE_NAME]
            
            # Log successful connection (without credentials)
            logger.info(f"Successfully connected to MongoDB database: {settings.DATABASE_NAME}")
            return True
            
        except Exception as e:
            logger.warning(f"Failed to connect to MongoDB: {str(e)}")
            await self.disconnect()
            return False
    
    async def disconnect(self):
        """
        Safely close MongoDB connection.
        """
        if self._client:
            try:
                self._client.close()
                logger.info("MongoDB connection closed")
            except Exception as e:
                logger.error(f"Error closing MongoDB connection: {str(e)}")
            finally:
                self._client = None
                self._database = None
    
    @property
    def is_connected(self) -> bool:
        """
        Check if database is currently connected.
        """
        return self._client is not None and self._database is not None
    
    @property
    def database(self) -> Optional[AsyncIOMotorDatabase]:
        """
        Get database instance if connected.
        Returns None if not connected.
        """
        return self._database
    
    @property
    def client(self) -> Optional[AsyncIOMotorClient]:
        """
        Get MongoDB client instance.
        Returns None if not connected.
        """
        return self._client
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform database health check.
        Returns detailed status information.
        """
        if not settings.MONGODB_URI:
            return {
                "status": "not_configured",
                "message": "MongoDB URI not configured",
                "timestamp": None
            }
        
        if not self.is_connected:
            return {
                "status": "disconnected",
                "message": "Database connection not established",
                "timestamp": None
            }
        
        try:
            start_time = time.time()
            await self._client.admin.command('ping')
            latency_ms = int((time.time() - start_time) * 1000)
            
            return {
                "status": "connected",
                "message": "Database is healthy",
                "database": settings.DATABASE_NAME,
                "latency_ms": latency_ms
            }
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "message": f"Health check failed: {str(e)}",
                "database": settings.DATABASE_NAME
            }
    
    async def get_collection(self, name: str):
        """
        Get collection by name.
        Returns None if database not connected.
        """
        if not self.is_connected or self._database is None:
            logger.warning(f"Cannot access collection '{name}': database not connected")
            return None
        return self._database[name]
    
    async def list_collections(self) -> list:
        """
        List all collections in the database.
        Returns empty list if not connected.
        """
        if not self.is_connected or not self._database:
            return []
        try:
            return await self._database.list_collection_names()
        except Exception as e:
            logger.error(f"Failed to list collections: {str(e)}")
            return []

# Global connection instance
mongo_connection = MongoConnection()

# For backward compatibility with Phase 1/2
async def get_database() -> Optional[AsyncIOMotorDatabase]:
    """
    Dependency for FastAPI to get database instance.
    """
    return mongo_connection.database

async def get_database_status() -> str:
    """
    Get database connection status for health checks.
    """
    if not settings.MONGODB_URI:
        return "not_configured"
    if mongo_connection.is_connected:
        return "connected"
    return "disconnected"