"""
Clinical history API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies.auth import require_authenticated_user
from app.api.serializers import serialize_doc
from app.models.clinical_history import ClinicalExtractionCreate
from app.services.clinical_extraction_service import clinical_extraction_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/clinical-history", tags=["clinical-history"])

@router.post("/extract")
async def extract_clinical_information(
    request: ClinicalExtractionCreate,
    current_user: dict = Depends(require_authenticated_user),
):
    """
    Extract structured clinical information from a response.
    """
    result = await clinical_extraction_service.extract_from_response(
        current_user,
        request.response_id,
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"],
        )
    
    return {
        "success": True,
        "message": result["message"],
        "data": serialize_doc(result["extraction"]),
    }

@router.get("/{interview_id}/structured")
async def get_structured_history(
    interview_id: str,
    current_user: dict = Depends(require_authenticated_user),
):
    """
    Get aggregated structured clinical history draft.
    """
    result = await clinical_extraction_service.get_structured_history(
        current_user,
        interview_id,
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"],
        )
    
    return {
        "success": True,
        "data": {
            "structured_history": result["structured_history"],
            "extraction_count": result["extraction_count"],
            "status": result["status"],
        },
    }