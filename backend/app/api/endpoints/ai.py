"""
AI interview API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies.auth import require_authenticated_user
from app.models.ai import AINextQuestionRequest
from app.services.ai_interview_service import ai_interview_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["ai"])

@router.get("/status")
async def get_ai_status(current_user: dict = Depends(require_authenticated_user)):
    """
    Get AI provider status (safe, no secrets).
    """
    status = await ai_interview_service.check_ai_status()
    return {
        "success": True,
        "data": {
            "available": status.get("available", False),
            "model_available": status.get("model_available", False),
            "model_name": status.get("model_name"),
        },
    }

@router.post("/interviews/{interview_id}/next-question")
async def get_ai_next_question(
    interview_id: str,
    request: AINextQuestionRequest,
    current_user: dict = Depends(require_authenticated_user),
):
    """
    Get AI-generated next question with fallback.
    """
    result = await ai_interview_service.get_next_question_ai(
        current_user,
        interview_id,
        request.current_question_id,
        request.response,
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