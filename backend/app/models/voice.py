"""
Voice processing models.
"""
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class ASRRequest(BaseModel):
    """Schema for ASR request."""
    interview_id: str = Field(..., description="Interview session ID")
    language: str = Field(..., description="Selected language for ASR")
    
    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        v = v.strip().lower()
        allowed = ["english", "telugu", "hindi", "tamil", "kannada", "malayalam", "marathi", "bengali"]
        if v not in allowed:
            raise ValueError(f"Unsupported language for ASR: {v}")
        return v

class ASRResponse(BaseModel):
    """Normalized ASR response."""
    text: str
    language: str
    provider: str = "sarvam"
    confidence: Optional[float] = None

class TTSRequest(BaseModel):
    """Schema for TTS request."""
    interview_id: str = Field(..., description="Interview session ID")
    text: str = Field(..., min_length=1, max_length=500, description="Text to synthesize")
    language: str = Field(..., description="Language for TTS")
    voice_id: Optional[str] = Field(None, description="Specific voice ID")
    
    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        v = v.strip().lower()
        allowed = ["english", "telugu", "hindi", "tamil", "kannada", "malayalam", "marathi", "bengali"]
        if v not in allowed:
            raise ValueError(f"Unsupported language for TTS: {v}")
        return v