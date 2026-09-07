"""
Patient API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response, status
from typing import Optional
from app.api.dependencies.auth import require_authenticated_user
from app.services.patient_service import patient_service
from app.models.patient import PatientProfileUpdate, PatientProfileResponse
from app.utils.photo_validation import photo_validator
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/patients", tags=["patients"])

@router.get("/me")
async def get_my_profile(current_user: dict = Depends(require_authenticated_user)):
    """Get current patient's profile."""
    patient = await patient_service.get_or_create_patient(current_user)
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    
    return {
        "success": True,
        "patient": {
            "id": str(patient["_id"]),
            "full_name": patient.get("full_name", current_user["full_name"]),
            "email": patient.get("email", current_user["email"]),
            "phone": patient.get("phone", current_user["phone"]),
            "gender": patient.get("gender", "Prefer not to say"),
            "age": patient.get("age"),
            "date_of_birth": patient.get("date_of_birth"),
            "photo_reference": patient.get("photo_reference"),
            "photo_consent": patient.get("photo_consent", False),
            "has_photo": bool(patient.get("photo_reference")),
        }
    }

@router.put("/me")
async def update_my_profile(
    update_data: PatientProfileUpdate,
    current_user: dict = Depends(require_authenticated_user),
):
    """Update current patient's profile."""
    result = await patient_service.update_patient_profile(current_user, update_data)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    patient = result["patient"]
    return {
        "success": True,
        "message": result.get("message", "Profile updated"),
        "patient": {
            "id": str(patient["_id"]),
            "full_name": patient.get("full_name"),
            "email": patient.get("email"),
            "phone": patient.get("phone"),
            "gender": patient.get("gender"),
            "age": patient.get("age"),
            "date_of_birth": patient.get("date_of_birth"),
            "photo_consent": patient.get("photo_consent", False),
            "has_photo": bool(patient.get("photo_reference")),
        }
    }

@router.post("/me/photo")
async def upload_photo(
    file: UploadFile = File(...),
    current_user: dict = Depends(require_authenticated_user),
):
    """Upload patient photo."""
    # Read file data
    file_data = await file.read()
    
    # Validate photo
    is_valid, error_msg, file_extension = photo_validator.validate_photo(file_data)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)
    
    # Save photo
    result = await patient_service.save_patient_photo(
        current_user,
        file_data,
        file_extension,
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return {
        "success": True,
        "message": "Photo uploaded successfully",
    }

@router.get("/me/photo")
async def get_photo(current_user: dict = Depends(require_authenticated_user)):
    """Get patient photo."""
    result = await patient_service.get_patient_photo(current_user)
    
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return Response(
        content=result["photo_data"],
        media_type="image/jpeg",
    )

@router.delete("/me/photo")
async def delete_photo(current_user: dict = Depends(require_authenticated_user)):
    """Delete patient photo."""
    result = await patient_service.delete_patient_photo(current_user)
    
    return {
        "success": True,
        "message": result["message"],
    }