"""
Database access layer with dependency injection and context managers.
"""
from typing import Optional, AsyncGenerator
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from app.db.connection import mongo_connection
import logging

logger = logging.getLogger(__name__)

async def get_db() -> Optional[AsyncIOMotorDatabase]:
    """
    FastAPI dependency to get database instance.
    Returns None if database is not connected.
    """
    return mongo_connection.database

async def get_collection(name: str) -> Optional[AsyncIOMotorCollection]:
    """
    Get a collection from the database.
    Returns None if database is not connected.
    """
    return await mongo_connection.get_collection(name)

@asynccontextmanager
async def db_session():
    """
    Context manager for database operations.
    Ensures proper connection state.
    """
    if not mongo_connection.is_connected:
        logger.warning("Database session requested but database is not connected")
        yield None
    else:
        try:
            yield mongo_connection.database
        finally:
            # Connection pooling handles cleanup
            pass

class DatabaseRepository:
    """
    Base repository class for database operations.
    Future repositories will inherit from this class.
    """
    
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
    
    async def get_collection(self) -> Optional[AsyncIOMotorCollection]:
        """Get collection instance."""
        return await get_collection(self.collection_name)
    
    async def find_one(self, query: dict):
        """Find a single document."""
        collection = await self.get_collection()
        if collection is None:
            return None
        return await collection.find_one(query)
    
    async def find_many(self, query: dict, limit: int = 100, skip: int = 0):
        """Find multiple documents."""
        collection = await self.get_collection()
        if collection is None:
            return []
        cursor = collection.find(query).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
    
    async def insert_one(self, document: dict):
        """Insert a single document."""
        collection = await self.get_collection()
        if collection is None:
            raise DatabaseUnavailableError(f"Cannot insert into {self.collection_name}")
        result = await collection.insert_one(document)
        return result.inserted_id
    
    async def update_one(self, query: dict, update: dict, upsert: bool = False):
        """Update a single document."""
        collection = await self.get_collection()
        if collection is None:
            raise DatabaseUnavailableError(f"Cannot update {self.collection_name}")
        result = await collection.update_one(query, update, upsert=upsert)
        return result.modified_count
    
    async def delete_one(self, query: dict):
        """Delete a single document."""
        collection = await self.get_collection()
        if collection is None:
            raise DatabaseUnavailableError(f"Cannot delete from {self.collection_name}")
        result = await collection.delete_one(query)
        return result.deleted_count

class DatabaseUnavailableError(Exception):
    """Raised when database operations are attempted without connection."""
    pass