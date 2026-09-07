from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator
from bson import ObjectId

class UserModel(BaseModel):
    """User model for MongoDB documents."""
    id: Optional[str] = Field(None, alias="_id")
    full_name: str
    email: str
    phone: str
    password_hash: str
    role: str = "PATIENT"
    email_verified: bool = False
    phone_verified: bool = False
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
    
    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        """Normalize email to lowercase and strip whitespace."""
        return v.strip().lower()
    
    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, v: str) -> str:
        """Normalize phone to digits only."""
        return ''.join(filter(str.isdigit, v))
    
    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Ensure role is valid."""
        allowed_roles = ["PATIENT", "DOCTOR", "ADMIN"]
        if v.upper() not in allowed_roles:
            raise ValueError(f"Invalid role: {v}")
        return v.upper()

class UserCreate(BaseModel):
    """Schema for user registration."""
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., pattern=r'^\d{10}$')
    password: str = Field(..., min_length=8, max_length=128)
    
    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        """Validate full name."""
        v = v.strip()
        if not v:
            raise ValueError("Full name cannot be empty")
        return v
    
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v):
            raise ValueError("Password must contain at least one special character")
        return v

class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Schema for user response (no sensitive data)."""
    id: str
    full_name: str
    email: str
    phone: str
    role: str
    email_verified: bool
    phone_verified: bool
    
    class Config:
        populate_by_name = True

class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse