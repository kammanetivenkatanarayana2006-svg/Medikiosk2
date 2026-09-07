from fastapi import APIRouter, Depends
from typing import Dict, Any
from datetime import datetime, timezone
from app.core.config import settings
from app.db.connection import mongo_connection
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Comprehensive health check endpoint.
    Reports application and database status separately.
    """
    # Get database health
    db_health = await mongo_connection.health_check()
    
    # Build response
    response = {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": settings.APP_ENV,
        "database": db_health
    }
    
    # Log health check
    logger.debug(f"Health check: app=ok, database={db_health['status']}")
    
    return response

@router.get("/")
async def api_info() -> Dict[str, Any]:
    """
    API information endpoint.
    """
    db_health = await mongo_connection.health_check()
    
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "AI-Powered Clinical Intake & Clinical History Software Platform",
        "phase": "Phase 3 - Database Foundation",
        "environment": settings.APP_ENV,
        "endpoints": {
            "health": "/api/health",
            "documentation": "/api/docs" if settings.is_development else None,
            "versioned_api": "/api/v1"
        },
        "database": db_health
    }