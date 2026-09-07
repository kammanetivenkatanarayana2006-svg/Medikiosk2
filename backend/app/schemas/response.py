from pydantic import BaseModel
from typing import Any, Optional

class APIResponse(BaseModel):
    """
    Standard API response format.
    """
    success: bool = True
    message: str = ""
    data: Optional[Any] = None
    error: Optional[str] = None