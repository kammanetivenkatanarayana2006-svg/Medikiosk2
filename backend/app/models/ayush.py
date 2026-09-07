"""
AYUSH / Ayurveda clinical information models.
"""
from typing import Optional, Dict, Any, List, Literal
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone

PRAKRITI_VALUES = [
    "Vata", "Pitta", "Kapha", "Vata-Pitta", "Pitta-Kapha",
    "Vata-Kapha", "Tridosha", "Not assessed", "Not recorded",
]

AGNI_VALUES = ["Sama", "Vishama", "Tikshna", "Manda", "Not assessed", "Not recorded"]

KOSHTHA_VALUES = ["Mridu", "Madhyama", "Krura", "Not assessed", "Not recorded"]

DASHAVIDHA_FIELDS = [
    "prakriti", "vikriti", "sara", "samhanana", "pramana",
    "satmya", "satva", "ahara_shakti", "vyayama_shakti", "vaya",
]

class AYUSHField(BaseModel):
    """Single AYUSH field with provenance."""
    value: Optional[str] = None
    source_type: Optional[Literal["patient_reported", "clinician_entered", "ai_assisted_extraction"]] = None
    source_id: Optional[str] = None
    verified: bool = False
    original_text: Optional[str] = None

class DashavidhaPariksha(BaseModel):
    """Dashavidha Pariksha fields."""
    prakriti: Optional[str] = None
    vikriti: Optional[str] = None
    sara: Optional[str] = None
    samhanana: Optional[str] = None
    pramana: Optional[str] = None
    satmya: Optional[str] = None
    satva: Optional[str] = None
    ahara_shakti: Optional[str] = None
    vyayama_shakti: Optional[str] = None
    vaya: Optional[str] = None

class AYUSHRecord(BaseModel):
    """Complete AYUSH clinical record."""
    id: Optional[str] = Field(None, alias="_id")
    patient_id: str
    consultation_id: str
    user_id: str
    prakriti: Optional[AYUSHField] = None
    vikriti: Optional[AYUSHField] = None
    agni: Optional[AYUSHField] = None
    koshtha: Optional[AYUSHField] = None
    ahara: Optional[AYUSHField] = None
    vihara: Optional[AYUSHField] = None
    nidra: Optional[AYUSHField] = None
    dashavidha_pariksha: Optional[DashavidhaPariksha] = None
    additional_information: Optional[AYUSHField] = None
    status: str = "draft"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class AYUSHUpdate(BaseModel):
    """Schema for updating AYUSH record."""
    prakriti: Optional[str] = None
    vikriti: Optional[str] = None
    agni: Optional[str] = None
    koshtha: Optional[str] = None
    ahara: Optional[str] = None
    vihara: Optional[str] = None
    nidra: Optional[str] = None
    dashavidha_pariksha: Optional[DashavidhaPariksha] = None
    additional_information: Optional[str] = None
    source_type: Literal["patient_reported", "clinician_entered"] = "patient_reported"
    
    @field_validator("prakriti")
    @classmethod
    def validate_prakriti(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in PRAKRITI_VALUES:
            raise ValueError(f"Invalid Prakriti value: {v}")
        return v
    
    @field_validator("agni")
    @classmethod
    def validate_agni(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in AGNI_VALUES:
            raise ValueError(f"Invalid Agni value: {v}")
        return v
    
    @field_validator("koshtha")
    @classmethod
    def validate_koshtha(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in KOSHTHA_VALUES:
            raise ValueError(f"Invalid Koshtha value: {v}")
        return v