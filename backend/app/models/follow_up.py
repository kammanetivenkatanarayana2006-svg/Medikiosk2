"""
Smart follow-up questioning models.
"""
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone

FOLLOWUP_STATUS = ["generated", "asked", "answered", "skipped", "declined", "expired", "cancelled"]

CLINICAL_FIELDS = [
    "chief_complaint", "duration", "onset", "symptoms", "severity",
    "aggravating_factors", "relieving_factors", "medical_history",
    "medications", "allergies", "family_history", "appetite",
    "bowel_habits", "sleep", "lifestyle", "additional_information",
]

FIELD_STATUS = ["captured", "missing", "unclear", "conflicting", "not_applicable", "declined"]

class MissingFieldInfo(BaseModel):
    """Missing information field."""
    field: str
    status: Literal["captured", "missing", "unclear", "conflicting", "not_applicable", "declined"]
    importance: Literal["required_for_documentation", "useful", "optional"] = "useful"
    source: Optional[str] = None

class FollowUpDecision(BaseModel):
    """Structured follow-up decision from AI."""
    should_follow_up: bool = Field(..., description="Whether follow-up is needed")
    target_field: Optional[str] = Field(None, description="Clinical field to ask about")
    question: Optional[str] = Field(None, min_length=5, max_length=500)
    reason: Optional[str] = Field(None, max_length=300)
    language: str = Field(default="english")
    
    @field_validator("target_field")
    @classmethod
    def validate_target_field(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in CLINICAL_FIELDS:
            raise ValueError(f"Invalid clinical field: {v}")
        return v
    
    @field_validator("question")
    @classmethod
    def validate_question(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        dangerous_patterns = [
            "password", "otp", "credit card", "aadhaar",
            "diagnose", "you have", "prescribe", "take this medicine",
        ]
        v_lower = v.lower()
        for pattern in dangerous_patterns:
            if pattern in v_lower:
                raise ValueError(f"Question contains inappropriate content: {pattern}")
        return v

class FollowUpRequest(BaseModel):
    """Request for follow-up generation."""
    response_id: str = Field(..., description="Current response ID")

class FollowUpResponse(BaseModel):
    """Response for follow-up."""
    should_follow_up: bool
    target_field: Optional[str] = None
    question: Optional[str] = None
    source: str = "ai"  # ai or deterministic
    ai_available: bool = True