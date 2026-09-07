"""
Longitudinal patient history models.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class TimelineEvent(BaseModel):
    """Single timeline event."""
    event_id: str
    patient_id: str
    consultation_id: Optional[str] = None
    event_type: str
    event_date: datetime
    title: str
    description: Optional[str] = None
    source_type: str
    source_id: Optional[str] = None
    
class ConsultationSummary(BaseModel):
    """Summary of a consultation for timeline."""
    id: str
    consultation_type: str
    language: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    has_clinical_history: bool = False
    document_count: int = 0
    ocr_completed_count: int = 0
    
class ConsultationDetail(BaseModel):
    """Detailed consultation information."""
    id: str
    consultation_type: str
    language: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    clinical_history: Optional[Dict[str, Any]] = None
    documents: List[Dict[str, Any]] = Field(default_factory=list)
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    
class LongitudinalHistory(BaseModel):
    """Complete longitudinal patient history."""
    patient_id: str
    total_consultations: int
    consultations: List[ConsultationSummary]
    timeline: List[TimelineEvent]