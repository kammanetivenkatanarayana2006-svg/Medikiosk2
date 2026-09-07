from typing import Dict, Any
from datetime import datetime
from app.core.config import settings
from app.db.mongodb import get_database_status

class HealthService:
    """
    Service for health check operations.
    """
    
    @staticmethod
    async def get_health_status() -> Dict[str, Any]:
        """
        Get comprehensive health status of the application.
        """
        db_status = await get_database_status()
        
        return {
            "status": "ok",
            "service": settings.app_name,
            "version": settings.app_version,
            "timestamp": datetime.utcnow().isoformat(),
            "database": db_status,
            "environment": "development" if settings.debug else "production",
        }