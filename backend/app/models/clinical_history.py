"""
Clinical history extraction models.
"""
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator

EXTRACTION_STATUS = ["pending", "processing", "completed", "failed", "needs_review"]

class ExtractedField(BaseModel):
    """Single extracted clinical field."""
    value: Optional[str] = Field(None, description="Extracted value")
    source: Literal["patient_response"] = Field(default="patient_response")
    question_id: Optional[str] = Field(None, description="Source question ID")
    response_id: Optional[str] = Field(None, description="Source response ID")
    confidence: Optional[float] = Field(None, description="Confidence score (null if not provided)")
    original_text: Optional[str] = Field(None, description="Original patient wording")

class ClinicalHistoryExtraction(BaseModel):
    """Structured clinical history extraction."""
    chief_complaint: Optional[ExtractedField] = None
    duration: Optional[ExtractedField] = None
    onset: Optional[ExtractedField] = None
    symptoms: List[ExtractedField] = Field(default_factory=list)
    severity: Optional[ExtractedField] = None
    aggravating_factors: List[ExtractedField] = Field(default_factory=list)
    relieving_factors: List[ExtractedField] = Field(default_factory=list)
    medical_history: List[ExtractedField] = Field(default_factory=list)
    medications: List[ExtractedField] = Field(default_factory=list)
    allergies: List[ExtractedField] = Field(default_factory=list)
    family_history: List[ExtractedField] = Field(default_factory=list)
    appetite: Optional[ExtractedField] = None
    bowel_habits: Optional[ExtractedField] = None
    sleep: Optional[ExtractedField] = None
    lifestyle: Optional[ExtractedField] = None
    additional_information: List[ExtractedField] = Field(default_factory=list)

class ClinicalExtractionCreate(BaseModel):
    """Request to trigger extraction."""
    response_id: str = Field(..., description="Response ID to extract from")

class ClinicalExtractionResponse(BaseModel):
    """Response schema for extraction."""
    id: str
    interview_id: str
    consultation_id: str
    patient_id: str
    response_id: str
    question_id: str
    section: str
    extracted_fields: Dict[str, Any]
    source: str = "ai_extracted"
    extraction_version: int = 1
    status: str = "pending"
    created_at: datetime
    updated_at: datetime