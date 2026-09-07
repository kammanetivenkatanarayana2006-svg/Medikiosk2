"""
Authentication API endpoints with verification.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.models.user import UserCreate, UserLogin
from app.services.auth_service import auth_service
from app.services.otp_service import otp_service
from app.services.email_verification_service import email_verification_service
from app.services.notification.email_service import email_service
from app.api.dependencies.auth import require_authenticated_user
from app.db.repositories.user_repository import user_repository
from app.core.config import settings

import logging

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


# ============================================================
# REGISTER
# ============================================================

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new patient.
    """

    result = await auth_service.register_user(user_data)

    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"],
        )

    return {
        "success": True,
        "message": result["message"],
        "user": result["user"],
    }


# ============================================================
# LOGIN
# ============================================================

@router.post("/login")
async def login(login_data: UserLogin):
    """
    Login user and return JWT access token.
    """

    result = await auth_service.login_user(login_data)

    if not result["success"]:
        raise HTTPException(
            status_code=result["status_code"],
            detail=result["error"],
        )

    # TokenResponse object returned by AuthService
    token_data = result["data"]

    return {
        "success": True,
        "message": result["message"],

        # IMPORTANT:
        # access_token is returned at the top level
        # because the authentication tests expect it here.
        "access_token": token_data.access_token,
        "token_type": token_data.token_type,
        "expires_in": token_data.expires_in,

        "user": token_data.user,

        "verification_required": result["verification_required"],
    }


# ============================================================
# CURRENT USER
# ============================================================

@router.get("/me")
async def get_current_user(
    current_user: dict = Depends(require_authenticated_user),
):
    """
    Get the currently authenticated user.
    """

    return {
        "success": True,
        "user": {
            "id": str(current_user["_id"]),
            "full_name": current_user["full_name"],
            "email": current_user["email"],
            "phone": current_user["phone"],
            "role": current_user["role"],
            "email_verified": current_user.get(
                "email_verified",
                False,
            ),
            "phone_verified": current_user.get(
                "phone_verified",
                False,
            ),
        },
    }


# ============================================================
# REQUEST PHONE OTP
# ============================================================

@router.post("/request-phone-otp")
async def request_phone_otp(
    current_user: dict = Depends(require_authenticated_user),
):
    """
    Request OTP for phone verification.
    """

    user_id = str(current_user["_id"])

    # Phone already verified
    if current_user.get("phone_verified"):
        return {
            "success": True,
            "message": "Phone already verified",
        }

    # Check resend cooldown
    resend_check = await otp_service.can_resend_otp(user_id)

    if not resend_check["can_resend"]:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=(
                f"Please wait "
                f"{resend_check['retry_after']} "
                "seconds before requesting another OTP."
            ),
        )

    # Create OTP
    otp_data = await otp_service.create_otp(
        user_id,
        "PHONE_VERIFICATION",
    )

    # Development environment:
    # OTP will be printed in application logs.
    if settings.is_development:
        logger.info(
            f"[DEV OTP] User: {user_id}, OTP: {otp_data['otp']}"
        )

    return {
        "success": True,
        "message": "OTP sent successfully",
    }


# ============================================================
# VERIFY PHONE
# ============================================================

@router.post("/verify-phone")
async def verify_phone(
    otp: str,
    current_user: dict = Depends(require_authenticated_user),
):
    """
    Verify phone number with OTP.
    """

    user_id = str(current_user["_id"])

    result = await otp_service.verify_otp(
        user_id,
        otp,
        "PHONE_VERIFICATION",
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"],
        )

    # Mark phone as verified
    await user_repository.update_user(
        user_id,
        {"phone_verified": True},
    )

    return {
        "success": True,
        "message": "Phone verified successfully",
    }


# ============================================================
# VERIFY EMAIL
# ============================================================

@router.get("/verify-email")
async def verify_email(
    token: str = Query(...),
):
    """
    Verify email using verification token.
    """

    result = await email_verification_service.verify_token(token)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"],
        )

    # Mark email as verified
    await user_repository.update_user(
        result["user_id"],
        {"email_verified": True},
    )

    return {
        "success": True,
        "message": "Email verified successfully",
    }


# ============================================================
# RESEND VERIFICATION EMAIL
# ============================================================

@router.post("/resend-verification-email")
async def resend_verification_email(
    current_user: dict = Depends(require_authenticated_user),
):
    """
    Resend email verification link.
    """

    user_id = str(current_user["_id"])

    # Email already verified
    if current_user.get("email_verified"):
        return {
            "success": True,
            "message": "Email already verified",
        }

    # Create verification token
    verification_data = (
        await email_verification_service.create_verification_token(
            user_id
        )
    )

    verification_link = (
        f"/api/auth/verify-email?"
        f"token={verification_data['token']}"
    )

    # Send verification email
    await email_service.send_verification_email(
        to=current_user["email"],
        full_name=current_user["full_name"],
        verification_link=(
            f"http://localhost:5173{verification_link}"
        ),
    )

    return {
        "success": True,
        "message": "Verification email sent",
    }
