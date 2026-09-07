"""
Medical document models.
"""
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator

DOCUMENT_STATUS = ["uploaded", "pending", "processing", "completed", "failed", "needs_review"]
ALLOWED_MIME_TYPES = {
    "application/pdf": "pdf",
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
}
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB

class MedicalDocumentCreate(BaseModel):
    """Schema for uploading medical document."""
    consultation_id: Optional[str] = Field(None, description="Associated consultation ID")
    
    @field_validator("consultation_id")
    @classmethod
    def validate_consultation_id(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) != 24:
            raise ValueError("Invalid consultation ID")
        return v

class MedicalDocumentResponse(BaseModel):
    """Response schema for medical document."""
    id: str
    patient_id: str
    user_id: str
    consultation_id: Optional[str] = None
    original_filename: str
    document_type: str
    mime_type: str
    file_size: int
    storage_key: str
    ocr_status: str
    processing_status: str
    created_at: datetime
    updated_at: datetime

class OCRResultResponse(BaseModel):
    """Response schema for OCR result."""
    id: str
    medical_document_id: str
    text: str
    page_count: int
    language: Optional[str] = None
    ocr_provider: str
    status: str
    created_at: datetime