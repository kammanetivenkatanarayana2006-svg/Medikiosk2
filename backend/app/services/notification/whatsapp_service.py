"""
WhatsApp notification service with provider abstraction.
"""
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class WhatsAppProviderInterface(ABC):
    """Abstract interface for WhatsApp providers."""
    
    @abstractmethod
    async def send_message(self, to: str, message: str) -> bool:
        """Send WhatsApp message. Returns True if successful."""
        pass

class WhatsAppBusinessProvider(WhatsAppProviderInterface):
    """WhatsApp Business Platform provider."""
    
    def __init__(self):
        self.api_url = settings.WHATSAPP_API_URL
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
    
    async def send_message(self, to: str, message: str) -> bool:
        """Send message via WhatsApp Business API."""
        if not self.api_url or not self.access_token or not self.phone_number_id:
            logger.warning("WhatsApp Business not configured")
            return False
        
        try:
            import aiohttp
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {"body": message},
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/{self.phone_number_id}/messages",
                    headers=headers,
                    json=payload,
                ) as response:
                    if response.status == 200:
                        logger.info(f"WhatsApp message sent to {to}")
                        return True
                    else:
                        logger.error(f"WhatsApp API error: {response.status}")
                        return False
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {str(e)}")
            return False

class ConsoleWhatsAppProvider(WhatsAppProviderInterface):
    """Development WhatsApp provider that logs to console."""
    
    async def send_message(self, to: str, message: str) -> bool:
        """Log WhatsApp message to console (development only)."""
        logger.info(f"[DEV WHATSAPP] To: {to}")
        logger.info(f"[DEV WHATSAPP] Message: {message}")
        return True

class WhatsAppService:
    """WhatsApp notification service."""
    
    def __init__(self):
        self.provider = self._get_provider()
    
    def _get_provider(self) -> WhatsAppProviderInterface:
        """Get WhatsApp provider based on configuration."""
        provider_name = getattr(settings, 'WHATSAPP_PROVIDER', '').lower()
        
        if provider_name == 'whatsapp_business':
            return WhatsAppBusinessProvider()
        elif provider_name == 'console' and settings.is_development:
            return ConsoleWhatsAppProvider()
        else:
            if settings.is_development:
                return ConsoleWhatsAppProvider()
            return None
    
    async def send_login_notification(self, to: str, full_name: str) -> bool:
        """Send login notification via WhatsApp."""
        message = f"MediKiosk: Hello {full_name}, you have successfully logged in to your MediKiosk account."
        return await self.send_message(to, message)
    
    async def send_message(self, to: str, message: str) -> bool:
        """Send message using configured provider."""
        if not self.provider:
            logger.warning("WhatsApp provider not configured")
            return False
        
        return await self.provider.send_message(to, message)

whatsapp_service = WhatsAppService()