"""
Email verification service.
"""
import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from app.db.repositories.verification_token_repository import verification_token_repository
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmailVerificationService:
    """Service for email verification."""
    
    def __init__(self):
        self.token_expiry_hours = getattr(settings, 'EMAIL_TOKEN_EXPIRE_HOURS', 24)
    
    @staticmethod
    def generate_token() -> str:
        """Generate secure random verification token."""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_token(token: str) -> str:
        """Hash token for secure storage."""
        return hashlib.sha256(token.encode()).hexdigest()
    
    async def create_verification_token(self, user_id: str) -> Dict[str, Any]:
        """Create verification token for user."""
        token = self.generate_token()
        token_hash = self.hash_token(token)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=self.token_expiry_hours)
        
        # Invalidate previous tokens
        await verification_token_repository.invalidate_previous_tokens(user_id, "EMAIL_VERIFICATION")
        
        token_record = await verification_token_repository.create_token(
            user_id=user_id,
            token_hash=token_hash,
            purpose="EMAIL_VERIFICATION",
            expires_at=expires_at,
        )
        
        return {
            "token": token,  # Only for email delivery
            "record_id": str(token_record["_id"]),
            "expires_at": expires_at,
        }
    
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify email verification token."""
        token_hash = self.hash_token(token)
        result = await verification_token_repository.verify_token(
            token_hash=token_hash,
            purpose="EMAIL_VERIFICATION",
        )
        
        if not result["success"]:
            return result
        
        # Mark token as used
        await verification_token_repository.mark_token_used(result["token_record"]["_id"])
        
        return {
            "success": True,
            "user_id": result["token_record"]["user_id"],
        }

email_verification_service = EmailVerificationService()