"""
OTP service for phone verification.
"""
import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from app.db.repositories.otp_repository import otp_repository
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class OTPService:
    """Service for OTP generation and verification."""
    
    def __init__(self):
        self.otp_length = 6
        self.otp_expiry_minutes = getattr(settings, 'OTP_EXPIRE_MINUTES', 10)
        self.otp_max_attempts = getattr(settings, 'OTP_MAX_ATTEMPTS', 5)
        self.otp_resend_cooldown = getattr(settings, 'OTP_RESEND_COOLDOWN_SECONDS', 30)
    
    @staticmethod
    def generate_otp() -> str:
        """Generate cryptographically secure 6-digit OTP."""
        return ''.join([str(secrets.randbelow(10)) for _ in range(6)])
    
    @staticmethod
    def hash_otp(otp: str) -> str:
        """Hash OTP for secure storage."""
        return hashlib.sha256(otp.encode()).hexdigest()
    
    async def create_otp(self, user_id: str, purpose: str = "PHONE_VERIFICATION") -> Dict[str, Any]:
        """
        Create and store OTP for user.
        Returns OTP only for provider delivery (not stored in response).
        """
        # Generate OTP
        otp = self.generate_otp()
        otp_hash = self.hash_otp(otp)
        
        # Calculate expiry
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=self.otp_expiry_minutes)
        
        # Invalidate previous OTPs
        await otp_repository.invalidate_previous_otps(user_id, purpose)
        
        # Store OTP hash
        otp_record = await otp_repository.create_otp(
            user_id=user_id,
            otp_hash=otp_hash,
            purpose=purpose,
            expires_at=expires_at,
            max_attempts=self.otp_max_attempts,
        )
        
        return {
            "otp": otp,  # Only for provider delivery
            "record_id": str(otp_record["_id"]),
            "expires_at": expires_at,
        }
    
    async def verify_otp(self, user_id: str, otp: str, purpose: str = "PHONE_VERIFICATION") -> Dict[str, Any]:
        """
        Verify OTP for user.
        Returns success/failure status.
        """
        otp_hash = self.hash_otp(otp)
        result = await otp_repository.verify_otp(
            user_id=user_id,
            otp_hash=otp_hash,
            purpose=purpose,
        )
        
        if not result["success"]:
            return result
        
        # Mark OTP as used
        await otp_repository.mark_otp_used(result["otp_record"]["_id"])
        
        return {
            "success": True,
            "message": "Phone verified successfully",
        }
    
    async def can_resend_otp(self, user_id: str, purpose: str = "PHONE_VERIFICATION") -> Dict[str, Any]:
        """Check if user can resend OTP."""
        last_otp = await otp_repository.get_latest_otp(user_id, purpose)
        
        if not last_otp:
            return {"can_resend": True}
        
        created_at = last_otp.get("created_at")
        if not created_at:
            return {"can_resend": True}
        
        now = datetime.now(timezone.utc)
        elapsed = (now - created_at).total_seconds()
        
        if elapsed < self.otp_resend_cooldown:
            return {
                "can_resend": False,
                "retry_after": int(self.otp_resend_cooldown - elapsed),
            }
        
        return {"can_resend": True}

otp_service = OTPService()