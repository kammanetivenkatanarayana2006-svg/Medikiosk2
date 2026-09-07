"""
Consultation API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies.auth import require_authenticated_user
from app.models.consultation import ConsultationCreate
from app.services.consultation_service import consultation_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/consultations", tags=["consultations"])

@router.post("")
async def create_consultation(
    consultation_data: ConsultationCreate,
    current_user: dict = Depends(require_authenticated_user),
):
    """
    Create a new consultation setup.
    Only authenticated PATIENT users can create their own consultation.
    """
    result = await consultation_service.create_consultation(
        current_user,
        consultation_data,
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"],
        )
    
    return {
        "success": True,
        "message": result["message"],
        "data": result["consultation"],
    }

@router.get("/{consultation_id}")
async def get_consultation(
    consultation_id: str,
    current_user: dict = Depends(require_authenticated_user),
):
    """
    Get consultation by ID with ownership verification.
    """
    result = await consultation_service.get_consultation(
        current_user,
        consultation_id,
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"],
        )
    
    return {
        "success": True,
        "data": result["consultation"],
    }

@router.get("")
async def get_my_consultations(
    current_user: dict = Depends(require_authenticated_user),
):
    """
    Get all consultations for authenticated patient.
    """
    result = await consultation_service.get_patient_consultations(current_user)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"],
        )
    
    return {
        "success": True,
        "data": result["consultations"],
    }