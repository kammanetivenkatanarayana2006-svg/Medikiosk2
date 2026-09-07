"""
AYUSH API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies.auth import require_authenticated_user
from app.models.ayush import AYUSHUpdate
from app.services.ayush_service import ayush_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/consultations", tags=["ayush"])

@router.get("/{consultation_id}/ayush")
async def get_ayush_record(
    consultation_id: str,
    current_user: dict = Depends(require_authenticated_user),
):
    """Get AYUSH record."""
    result = await ayush_service.get_ayush_record(current_user, consultation_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"],
        )
    
    return {
        "success": True,
        "data": result["record"],
    }

@router.put("/{consultation_id}/ayush")
async def update_ayush_record(
    consultation_id: str,
    update_data: AYUSHUpdate,
    current_user: dict = Depends(require_authenticated_user),
):
    """Update AYUSH record."""
    result = await ayush_service.update_ayush_record(
        current_user,
        consultation_id,
        update_data,
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"],
        )
    
    return {
        "success": True,
        "message": result["message"],
        "data": result["record"],
    }