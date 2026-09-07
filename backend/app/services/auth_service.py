"""
Authentication service with verification support.
"""
from typing import Optional, Dict, Any
from app.db.repositories.user_repository import user_repository
from app.utils.security import security_utils
from app.models.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.services.notification.email_service import email_service
from app.services.notification.whatsapp_service import whatsapp_service
from app.services.otp_service import otp_service
from app.services.email_verification_service import email_verification_service
import logging

logger = logging.getLogger(__name__)

class AuthService:
    """Service for authentication operations."""
    
    @staticmethod
    async def register_user(user_data: UserCreate) -> Dict[str, Any]:
        """Register a new user with verification workflow."""
        # Check for existing email
        existing_email = await user_repository.find_by_email(user_data.email)
        if existing_email:
            return {
                "success": False,
                "error": "An account with this email already exists.",
                "status_code": 409,
            }
        
        # Check for existing phone
        existing_phone = await user_repository.find_by_phone(user_data.phone)
        if existing_phone:
            return {
                "success": False,
                "error": "An account with this phone number already exists.",
                "status_code": 409,
            }
        
        # Create user
        try:
            user = await user_repository.create_user(
                full_name=user_data.full_name,
                email=user_data.email,
                phone=user_data.phone,
                password=user_data.password,
                role="PATIENT",
            )
            
            if not user:
                return {
                    "success": False,
                    "error": "Registration failed. Please try again.",
                    "status_code": 500,
                }
            
            # Send registration email notification (non-blocking)
            try:
                await email_service.send_registration_email(
                    to=user["email"],
                    full_name=user["full_name"],
                )
            except Exception as e:
                logger.warning(f"Failed to send registration email: {str(e)}")
            
            # Create verification token
            try:
                verification_data = await email_verification_service.create_verification_token(
                    user_id=str(user["_id"])
                )
                verification_link = f"/api/auth/verify-email?token={verification_data['token']}"
                
                # Send verification email
                await email_service.send_verification_email(
                    to=user["email"],
                    full_name=user["full_name"],
                    verification_link=f"http://localhost:5173{verification_link}",
                )
            except Exception as e:
                logger.warning(f"Failed to create/send verification email: {str(e)}")
            
            # Create response
            user_response = UserResponse(
                id=str(user["_id"]),
                full_name=user["full_name"],
                email=user["email"],
                phone=user["phone"],
                role=user["role"],
                email_verified=user.get("email_verified", False),
                phone_verified=user.get("phone_verified", False),
            )
            
            return {
                "success": True,
                "message": "Registration successful. Please verify your email and phone.",
                "user": user_response,
                "status_code": 201,
            }
            
        except Exception as e:
            logger.error(f"Registration failed: {str(e)}")
            return {
                "success": False,
                "error": "Registration failed. Please try again.",
                "status_code": 500,
            }
    
    @staticmethod
    async def login_user(login_data: UserLogin) -> Dict[str, Any]:
        """Authenticate user with verification check."""
        user = await user_repository.verify_credentials(
            login_data.email,
            login_data.password,
        )
        
        if not user:
            return {
                "success": False,
                "error": "Invalid email or password.",
                "status_code": 401,
            }
        
        # Send WhatsApp login notification (non-blocking)
        try:
            await whatsapp_service.send_login_notification(
                to=user["phone"],
                full_name=user["full_name"],
            )
        except Exception as e:
            logger.warning(f"Failed to send WhatsApp notification: {str(e)}")
        
        # Generate token
        token = security_utils.create_access_token(
            user_id=str(user["_id"]),
            role=user["role"],
        )
        
        user_response = UserResponse(
            id=str(user["_id"]),
            full_name=user["full_name"],
            email=user["email"],
            phone=user["phone"],
            role=user["role"],
            email_verified=user.get("email_verified", False),
            phone_verified=user.get("phone_verified", False),
        )
        
        token_response = TokenResponse(
            access_token=token,
            expires_in=security_utils.get_token_expiry(),
            user=user_response,
        )
        
        return {
            "success": True,
            "message": "Login successful",
            "data": token_response,
            "verification_required": not (user.get("email_verified") and user.get("phone_verified")),
            "status_code": 200,
        }

auth_service = AuthService()