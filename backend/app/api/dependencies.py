"""
API dependencies for FastAPI.
These will be used by future endpoints for common functionality.
"""
from typing import Optional
from fastapi import Request, HTTPException, status
from app.db.mongodb import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

async def get_db() -> Optional[AsyncIOMotorDatabase]:
    """
    Database dependency for API endpoints.
    Returns None if database is not configured.
    """
    return await get_database()

async def get_request_id(request: Request) -> str:
    """
    Get or generate request ID for tracking.
    """
    return getattr(request.state, "request_id", "unknown")

# Future dependencies:
# async def get_current_user(...)
# async def get_current_doctor(...)
# async def require_permissions(...)