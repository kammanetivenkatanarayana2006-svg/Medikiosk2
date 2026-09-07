from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BaseDBModel(BaseModel):
    """
    Base model for database documents.
    """
    id: Optional[str] = Field(None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True