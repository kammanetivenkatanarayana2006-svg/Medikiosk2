"""
TTS provider abstraction.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class TTSProvider(ABC):
    """Abstract interface for TTS providers."""
    
    @abstractmethod
    async def synthesize(
        self,
        text: str,
        language: str,
        voice_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Synthesize text to speech.
        Returns dict with audio_data, mime_type, provider.
        """
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """Check if provider is available."""
        pass

class SarvamTTSProvider(TTSProvider):
    """
    Sarvam TTS provider implementation.
    Uses Sarvam Text-to-Speech API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        from app.core.config import settings
        self.api_key = api_key or settings.SARVAM_API_KEY
        self.api_url = getattr(settings, 'SARVAM_TTS_URL', 'https://api.sarvam.ai/text-to-speech')
    
    async def is_available(self) -> bool:
        return bool(self.api_key)
    
    async def synthesize(
        self,
        text: str,
        language: str,
        voice_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Synthesize text using Sarvam TTS API."""
        if not self.api_key:
            return {
                "success": False,
                "error": "TTS not configured",
            }
        
        try:
            import aiohttp
            
            language_codes = {
                "english": "en",
                "telugu": "te",
                "hindi": "hi",
                "tamil": "ta",
                "kannada": "kn",
                "malayalam": "ml",
                "marathi": "mr",
                "bengali": "bn",
            }
            
            sar_language = language_codes.get(language, "en")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "text": text,
                "language": sar_language,
            }
            
            if voice_id:
                payload["voice_id"] = voice_id
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status == 200:
                        audio_data = await response.read()
                        return {
                            "success": True,
                            "audio_data": audio_data,
                            "mime_type": "audio/wav",
                            "provider": "sarvam",
                        }
                    else:
                        return {
                            "success": False,
                            "error": "TTS provider error",
                        }
        except Exception as e:
            logger.error(f"Sarvam TTS exception: {str(e)}")
            return {
                "success": False,
                "error": "TTS service unavailable",
            }

class MockTTSProvider(TTSProvider):
    """
    Development mock TTS provider.
    Does NOT generate fake audio.
    """
    
    async def is_available(self) -> bool:
        return False
    
    async def synthesize(
        self,
        text: str,
        language: str,
        voice_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        return {
            "success": False,
            "error": "TTS not configured.",
        }