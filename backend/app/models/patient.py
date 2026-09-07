"""
Patient profile models.
"""
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId

class PatientProfile(BaseModel):
    """Patient profile schema."""
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    full_name: str
    email: str
    phone: str
    gender: str
    age: Optional[int] = None
    date_of_birth: Optional[str] = None
    photo_reference: Optional[str] = None
    photo_consent: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class PatientProfileUpdate(BaseModel):
    """Schema for patient profile update."""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = None
    phone: Optional[str] = Field(None, pattern=r'^\d{10}$')
    gender: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=150)
    date_of_birth: Optional[str] = None
    
    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        allowed = ["Male", "Female", "Other", "Prefer not to say"]
        if v not in allowed:
            raise ValueError(f"Invalid gender: {v}")
        return v

class PatientProfileResponse(BaseModel):
    """Response schema for patient profile (no sensitive data)."""
    id: str
    full_name: str
    email: str
    phone: str
    gender: str
    age: Optional[int] = None
    date_of_birth: Optional[str] = None
    photo_reference: Optional[str] = None
    photo_consent: bool = False
    has_photo: bool = False