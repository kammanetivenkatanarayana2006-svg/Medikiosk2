"""
Interview API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies.auth import require_authenticated_user
from app.models.interview import InterviewCreate, InterviewResponse
from app.services.interview_service import interview_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/interviews", tags=["interviews"])

@router.post("")
async def create_interview(
    interview_data: InterviewCreate,
    current_user: dict = Depends(require_authenticated_user),
):
    """Create interview session."""
    result = await interview_service.create_interview(
        current_user,
        interview_data.consultation_id,
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"],
        )
    
    interview = result["interview"]
    return {
        "success": True,
        "message": result["message"],
        "data": {
            "interview_id": str(interview["_id"]),
            "consultation_id": interview["consultation_id"],
            "status": interview["status"],
        }
    }

@router.get("/{interview_id}")
async def get_interview(
    interview_id: str,
    current_user: dict = Depends(require_authenticated_user),
):
    """Get interview state."""
    result = await interview_service.get_interview(current_user, interview_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"],
        )
    
    return {
        "success": True,
        "data": {
            "interview": result["interview"],
            "responses": result["responses"],
            "current_question": result["current_question"],
            "progress": result["progress"],
        }
    }

@router.post("/{interview_id}/start")
async def start_interview(
    interview_id: str,
    current_user: dict = Depends(require_authenticated_user),
):
    """Start interview."""
    result = await interview_service.start_interview(current_user, interview_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"],
        )
    
    return {"success": True, "message": result["message"]}

@router.post("/{interview_id}/responses")
async def submit_response(
    interview_id: str,
    response_data: InterviewResponse,
    current_user: dict = Depends(require_authenticated_user),
):
    """Submit interview response."""
    result = await interview_service.submit_response(
        current_user,
        interview_id,
        response_data.question_id,
        response_data.response_text,
        response_data.input_method,
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"],
        )
    
    return {
        "success": True,
        "message": result["message"],
        "data": result,
    }

@router.post("/{interview_id}/pause")
async def pause_interview(
    interview_id: str,
    current_user: dict = Depends(require_authenticated_user),
):
    """Pause interview."""
    result = await interview_service.pause_interview(current_user, interview_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"],
        )
    
    return {"success": True, "message": result["message"]}

@router.post("/{interview_id}/resume")
async def resume_interview(
    interview_id: str,
    current_user: dict = Depends(require_authenticated_user),
):
    """Resume interview."""
    result = await interview_service.resume_interview(current_user, interview_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"],
        )
    
    return {"success": True, "message": result["message"]}

@router.post("/{interview_id}/cancel")
async def cancel_interview(
    interview_id: str,
    current_user: dict = Depends(require_authenticated_user),
):
    """Cancel interview."""
    result = await interview_service.cancel_interview(current_user, interview_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"],
        )
    
    return {"success": True, "message": result["message"]}