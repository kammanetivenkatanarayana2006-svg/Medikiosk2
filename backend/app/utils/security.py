"""
Security utilities for password hashing and JWT.
"""
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from app.core.config import settings

# Password hashing context using Argon2id
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=65536,
    argon2__time_cost=3,
    argon2__parallelism=4,
)

class SecurityUtils:
    """Security utility functions."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using Argon2id."""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False
    
    @staticmethod
    def create_access_token(
        user_id: str,
        role: str,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """
        Create a JWT access token.
        Token contains only minimal non-sensitive information.
        """
        if expires_delta is None:
            expires_delta = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        
        now = datetime.now(timezone.utc)
        expire = now + expires_delta
        
        payload = {
            "sub": str(user_id),
            "role": role,
            "iat": now,
            "exp": expire,
            "type": "access",
        }
        
        if settings.JWT_ISSUER:
            payload["iss"] = settings.JWT_ISSUER
        
        if settings.JWT_AUDIENCE:
            payload["aud"] = settings.JWT_AUDIENCE
        
        return jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )
    
    @staticmethod
    def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Decode and validate JWT access token.
        Returns None if invalid or expired.
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
                options={"verify_exp": True, "verify_iat": True},
            )
            return payload
        except JWTError as e:
            return None
    
    @staticmethod
    def get_token_expiry() -> int:
        """Get token expiry in seconds."""
        return settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60

security_utils = SecurityUtils()