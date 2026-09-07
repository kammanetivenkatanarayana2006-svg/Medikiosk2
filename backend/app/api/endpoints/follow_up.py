"""
Smart follow-up API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies.auth import require_authenticated_user
from app.models.follow_up import FollowUpRequest
from app.services.smart_follow_up_service import smart_follow_up_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/interviews", tags=["follow-up"])

@router.post("/{interview_id}/follow-up")
async def get_follow_up(
    interview_id: str,
    request: FollowUpRequest,
    current_user: dict = Depends(require_authenticated_user),
):
    """
    Get smart follow-up question.
    """
    result = await smart_follow_up_service.get_follow_up(
        current_user,
        interview_id,
        request.response_id,
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"],
        )
    
    return {
        "success": True,
        "data": result["data"],
    }