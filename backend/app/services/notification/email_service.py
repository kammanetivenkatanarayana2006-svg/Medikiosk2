"""
Email notification service with provider abstraction.
"""
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmailProviderInterface(ABC):
    """Abstract interface for email providers."""
    
    @abstractmethod
    async def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send email. Returns True if successful."""
        pass

class SMTPEmailProvider(EmailProviderInterface):
    """SMTP email provider implementation."""
    
    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.username = settings.SMTP_USERNAME
        self.password = settings.SMTP_PASSWORD
        
    async def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send email via SMTP."""
        if not self.host:
            logger.warning("SMTP not configured")
            return False
        
        try:
            import aiosmtplib
            from email.mime.text import MIMEText
            
            message = MIMEText(body)
            message["Subject"] = subject
            message["From"] = settings.EMAIL_FROM or self.username
            message["To"] = to
            
            await aiosmtplib.send(
                message,
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                use_tls=True,
            )
            
            logger.info(f"Email sent to {to}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

class ConsoleEmailProvider(EmailProviderInterface):
    """Development email provider that logs to console."""
    
    async def send_email(self, to: str, subject: str, body: str) -> bool:
        """Log email to console (development only)."""
        logger.info(f"[DEV EMAIL] To: {to}, Subject: {subject}")
        logger.info(f"[DEV EMAIL] Body: {body[:200]}...")
        return True

class EmailService:
    """Email notification service."""
    
    def __init__(self):
        self.provider = self._get_provider()
    
    def _get_provider(self) -> EmailProviderInterface:
        """Get email provider based on configuration."""
        provider_name = getattr(settings, 'EMAIL_PROVIDER', '').lower()
        
        if provider_name == 'smtp':
            return SMTPEmailProvider()
        elif provider_name == 'console' and settings.is_development:
            return ConsoleEmailProvider()
        else:
            # Default to console in development, no-op in production
            if settings.is_development:
                return ConsoleEmailProvider()
            return None
    
    async def send_registration_email(self, to: str, full_name: str) -> bool:
        """Send registration notification email."""
        subject = "Welcome to MediKiosk"
        body = f"""Hello {full_name},

Your MediKiosk account registration was received successfully.

Please verify your email address to complete account verification.

Regards,
MediKiosk Team"""
        
        return await self.send_email(to, subject, body)
    
    async def send_verification_email(self, to: str, full_name: str, verification_link: str) -> bool:
        """Send email verification link."""
        subject = "Verify Your Email - MediKiosk"
        body = f"""Hello {full_name},

Please verify your email address by clicking the link below:

{verification_link}

This link will expire in 24 hours.

Regards,
MediKiosk Team"""
        
        return await self.send_email(to, subject, body)
    
    async def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send email using configured provider."""
        if not self.provider:
            logger.warning("Email provider not configured")
            return False
        
        return await self.provider.send_email(to, subject, body)

email_service = EmailService()