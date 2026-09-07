"""
Longitudinal history API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from app.api.dependencies.auth import require_authenticated_user
from app.services.longitudinal_service import longitudinal_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/history", tags=["history"])

@router.get("")
async def get_patient_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    sort_order: str = Query("newest_first", pattern="^(newest_first|oldest_first)$"),
    current_user: dict = Depends(require_authenticated_user),
):
    """
    Get longitudinal patient history.
    """
    result = await longitudinal_service.get_patient_history(
        current_user,
        page,
        page_size,
        sort_order,
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"],
        )
    
    return {
        "success": True,
        "data": result["history"],
    }

@router.get("/consultations/{consultation_id}")
async def get_consultation_detail(
    consultation_id: str,
    current_user: dict = Depends(require_authenticated_user),
):
    """
    Get detailed consultation information.
    """
    result = await longitudinal_service.get_consultation_detail(
        current_user,
        consultation_id,
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"],
        )
    
    return {
        "success": True,
        "data": result["detail"],
    }