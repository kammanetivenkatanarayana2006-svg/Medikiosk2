"""
Medical document API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Optional
from app.api.dependencies.auth import require_authenticated_user
from app.api.serializers import serialize_doc, serialize_docs
from app.services.medical_document_service import medical_document_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/medical-documents", tags=["medical-documents"])

@router.post("")
async def upload_document(
    consultation_id: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: dict = Depends(require_authenticated_user),
):
    """Upload medical document."""
    file_data = await file.read()
    mime_type = file.content_type or "application/octet-stream"
    
    result = await medical_document_service.upload_document(
        current_user,
        file_data,
        file.filename or "document",
        mime_type,
        consultation_id,
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"],
        )
    
    return {
        "success": True,
        "message": result["message"],
        "data": result["document"],
    }

@router.get("")
async def get_my_documents(current_user: dict = Depends(require_authenticated_user)):
    """Get all documents for patient."""
    result = await medical_document_service.get_patient_documents(current_user)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"],
        )
    
    return {
        "success": True,
        "data": serialize_docs(result["documents"]),
    }

@router.get("/{document_id}")
async def get_document(
    document_id: str,
    current_user: dict = Depends(require_authenticated_user),
):
    """Get document metadata."""
    result = await medical_document_service.get_document(current_user, document_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"],
        )
    
    return {
        "success": True,
        "data": serialize_doc(result["document"]),
    }

@router.get("/{document_id}/ocr")
async def get_document_ocr(
    document_id: str,
    current_user: dict = Depends(require_authenticated_user),
):
    """Get OCR result for document."""
    result = await medical_document_service.get_document_ocr(current_user, document_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"],
        )
    
    return {
        "success": True,
        "data": serialize_doc(result["ocr_result"]),
    }

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: dict = Depends(require_authenticated_user),
):
    """Delete document."""
    result = await medical_document_service.delete_document(current_user, document_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"],
        )
    
    return {
        "success": True,
        "message": result["message"],
    }