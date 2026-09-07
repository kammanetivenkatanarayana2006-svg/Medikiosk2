"""
Consultation models for Phase 10.
"""
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId

SUPPORTED_LANGUAGES = [
    "english",
    "telugu",
    "hindi",
    "tamil",
    "kannada",
    "malayalam",
    "marathi",
    "bengali",
]

SUPPORTED_CONSULTATION_TYPES = [
    "general",
    "ayurveda",
    "follow_up",
]

class ConsultationCreate(BaseModel):
    """Schema for creating consultation setup."""
    language: str = Field(..., description="Selected language")
    consultation_type: str = Field(..., description="Type of consultation")
    consent_given: bool = Field(..., description="Explicit patient consent")
    
    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        """Validate and normalize language."""
        v = v.strip().lower()
        if v not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {v}")
        return v
    
    @field_validator("consultation_type")
    @classmethod
    def validate_consultation_type(cls, v: str) -> str:
        """Validate and normalize consultation type."""
        v = v.strip().lower()
        if v not in SUPPORTED_CONSULTATION_TYPES:
            raise ValueError(f"Invalid consultation type: {v}")
        return v
    
    @field_validator("consent_given")
    @classmethod
    def validate_consent(cls, v: bool) -> bool:
        """Consent must be explicitly true."""
        if not v:
            raise ValueError("Patient consent is required")
        return v

class ConsultationResponse(BaseModel):
    """Response schema for consultation."""
    id: str
    patient_id: str
    user_id: str
    language: str
    consultation_type: str
    consent_given: bool
    consent_timestamp: datetime
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True