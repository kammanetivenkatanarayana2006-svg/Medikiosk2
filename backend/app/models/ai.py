"""
AI interview models for Ollama/Qwen integration.
"""
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, field_validator

class AIInterviewDecision(BaseModel):
    """Structured output from AI interview provider."""
    answer_status: Literal["complete", "incomplete", "unclear"] = Field(
        ..., description="Whether the answer is sufficient"
    )
    missing_information: List[str] = Field(
        default_factory=list, description="What information is missing"
    )
    next_question: str = Field(
        ..., min_length=5, max_length=500, description="Next question to ask"
    )
    section: str = Field(
        ..., description="Current interview section"
    )
    reason: str = Field(
        default="", max_length=300, description="Brief reason for decision"
    )
    
    @field_validator("next_question")
    @classmethod
    def validate_next_question(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Next question cannot be empty")
        if len(v) < 5:
            raise ValueError("Next question too short")
        # Reject dangerous content
        dangerous_patterns = [
            "password", "otp", "credit card", "aadhaar", "pan number",
            "diagnose", "you have", "prescribe", "take this medicine",
        ]
        v_lower = v.lower()
        for pattern in dangerous_patterns:
            if pattern in v_lower:
                raise ValueError(f"Question contains inappropriate content: {pattern}")
        return v
    
    @field_validator("section")
    @classmethod
    def validate_section(cls, v: str) -> str:
        v = v.strip().lower()
        allowed_sections = [
            "introduction", "chief_complaint", "duration", "onset", "symptoms",
            "severity", "aggravating_factors", "relieving_factors", "medical_history",
            "medication_history", "allergies", "family_history", "appetite",
            "bowel_habits", "sleep", "lifestyle", "additional_information", "completion",
        ]
        if v not in allowed_sections:
            # Fallback to current section validation
            raise ValueError(f"Invalid section: {v}")
        return v

class AIProviderStatus(BaseModel):
    """Status of AI provider."""
    available: bool = False
    model_available: bool = False
    model_name: Optional[str] = None
    error: Optional[str] = None

class AINextQuestionRequest(BaseModel):
    """Request for AI-generated next question."""
    current_question_id: str = Field(..., description="Current question ID")
    response: str = Field(..., min_length=1, max_length=2000, description="Patient response")