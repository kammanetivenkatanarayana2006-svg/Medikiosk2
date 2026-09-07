"""
Authentication API endpoints with verification.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.models.user import UserCreate, UserLogin
from app.services.auth_service import auth_service
from app.services.otp_service import otp_service
from app.services.email_verification_service import email_verification_service
from app.api.dependencies.auth import require_authenticated_user
from app.db.repositories.user_repository import user_repository
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

# ... existing register and login endpoints ...

@router.post("/request-phone-otp")
async def request_phone_otp(current_user: dict = Depends(require_authenticated_user)):
    """
    Request OTP for phone verification.
    """
    user_id = str(current_user["_id"])
    
    # Check if phone already verified
    if current_user.get("phone_verified"):
        return {
            "success": True,
            "message": "Phone already verified",
        }
    
    # Check resend cooldown
    resend_check = await otp_service.can_resend_otp(user_id)
    if not resend_check["can_resend"]:
        raise HTTPException(
            status_code=429,
            detail=f"Please wait {resend_check['retry_after']} seconds before requesting another OTP.",
        )
    
    # Create OTP
    otp_data = await otp_service.create_otp(user_id, "PHONE_VERIFICATION")
    
    # TODO: Send OTP via configured provider
    # For now, in development, log the OTP
    if settings.is_development:
        logger.info(f"[DEV OTP] User: {user_id}, OTP: {otp_data['otp']}")
    
    return {
        "success": True,
        "message": "OTP sent successfully",
    }

@router.post("/verify-phone")
async def verify_phone(
    otp: str,
    current_user: dict = Depends(require_authenticated_user),
):
    """
    Verify phone number with OTP.
    """
    user_id = str(current_user["_id"])
    
    result = await otp_service.verify_otp(user_id, otp, "PHONE_VERIFICATION")
    
    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )
    
    # Update user phone_verified
    await user_repository.update_user(user_id, {"phone_verified": True})
    
    return {
        "success": True,
        "message": "Phone verified successfully",
    }

@router.get("/verify-email")
async def verify_email(token: str = Query(...)):
    """
    Verify email with token.
    """
    result = await email_verification_service.verify_token(token)
    
    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )
    
    # Update user email_verified
    await user_repository.update_user(result["user_id"], {"email_verified": True})
    
    return {
        "success": True,
        "message": "Email verified successfully",
    }

@router.post("/resend-verification-email")
async def resend_verification_email(current_user: dict = Depends(require_authenticated_user)):
    """
    Resend email verification link.
    """
    user_id = str(current_user["_id"])
    
    if current_user.get("email_verified"):
        return {
            "success": True,
            "message": "Email already verified",
        }
    
    verification_data = await email_verification_service.create_verification_token(user_id)
    verification_link = f"/api/auth/verify-email?token={verification_data['token']}"
    
    # Send verification email
    await email_service.send_verification_email(
        to=current_user["email"],
        full_name=current_user["full_name"],
        verification_link=f"http://localhost:5173{verification_link}",
    )
    
    return {
        "success": True,
        "message": "Verification email sent",
    }