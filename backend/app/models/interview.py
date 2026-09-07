"""
Interview session and response models.
"""
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId

INTERVIEW_STATUS = ["ready", "in_progress", "paused", "completed", "cancelled"]
VALID_TRANSITIONS = {
    "ready": ["in_progress", "cancelled"],
    "in_progress": ["paused", "completed", "cancelled"],
    "paused": ["in_progress", "cancelled"],
    "completed": [],
    "cancelled": [],
}

INTERVIEW_SECTIONS = [
    "introduction",
    "chief_complaint",
    "duration",
    "onset",
    "symptoms",
    "severity",
    "aggravating_factors",
    "relieving_factors",
    "medical_history",
    "medication_history",
    "allergies",
    "family_history",
    "appetite",
    "bowel_habits",
    "sleep",
    "lifestyle",
    "additional_information",
    "completion",
]

QUESTION_TYPES = [
    "open_text",
    "yes_no",
    "single_choice",
    "multiple_choice",
    "number",
    "date",
    "duration",
    "severity",
]

class InterviewCreate(BaseModel):
    """Schema for creating interview session."""
    consultation_id: str = Field(..., description="Consultation ID from Phase 10")

class InterviewResponse(BaseModel):
    """Schema for submitting interview response."""
    question_id: str = Field(..., description="Question being answered")
    response_text: str = Field(..., min_length=1, max_length=2000, description="Patient response")
    input_method: str = Field(default="text", description="Input method (text/voice)")
    
    @field_validator("input_method")
    @classmethod
    def validate_input_method(cls, v: str) -> str:
        if v not in ["text", "voice"]:
            raise ValueError(f"Invalid input method: {v}")
        return v
    
    @field_validator("response_text")
    @classmethod
    def validate_response(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Response cannot be empty")
        return v

class InterviewResponseModel(BaseModel):
    """Response schema for interview."""
    id: str
    consultation_id: str
    patient_id: str
    user_id: str
    language: str
    consultation_type: str
    current_section: str
    current_question_id: str
    status: str
    progress: float
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime