"""
ASR provider abstraction.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ASRProvider(ABC):
    """Abstract interface for ASR providers."""
    
    @abstractmethod
    async def transcribe(
        self,
        audio_data: bytes,
        language: str,
        mime_type: str = "audio/wav",
    ) -> Dict[str, Any]:
        """
        Transcribe audio to text.
        Returns dict with text, language, confidence, provider.
        """
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """Check if provider is available."""
        pass

class SarvamASRProvider(ASRProvider):
    """
    Sarvam ASR provider implementation.
    Uses Sarvam Speech-to-Text API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        from app.core.config import settings
        self.api_key = api_key or settings.SARVAM_API_KEY
        self.api_url = getattr(settings, 'SARVAM_ASR_URL', 'https://api.sarvam.ai/speech-to-text')
    
    async def is_available(self) -> bool:
        """Check if Sarvam ASR is configured."""
        return bool(self.api_key)
    
    async def transcribe(
        self,
        audio_data: bytes,
        language: str,
        mime_type: str = "audio/wav",
    ) -> Dict[str, Any]:
        """
        Transcribe audio using Sarvam API.
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "Sarvam ASR not configured",
            }
        
        try:
            import aiohttp
            
            # Map language to Sarvam language code
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
            }
            
            # Prepare form data
            form_data = aiohttp.FormData()
            form_data.add_field(
                "file",
                audio_data,
                filename=f"audio_{sar_language}.wav",
                content_type=mime_type,
            )
            form_data.add_field("language", sar_language)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=headers,
                    data=form_data,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        text = result.get("transcript", result.get("text", ""))
                        
                        if not text:
                            return {
                                "success": False,
                                "error": "Empty transcription",
                            }
                        
                        return {
                            "success": True,
                            "text": text,
                            "language": language,
                            "provider": "sarvam",
                            "confidence": result.get("confidence"),
                        }
                    else:
                        error_text = await response.text()
                        logger.warning(f"Sarvam ASR error {response.status}: {error_text[:200]}")
                        return {
                            "success": False,
                            "error": "ASR provider error",
                        }
        except Exception as e:
            logger.error(f"Sarvam ASR exception: {str(e)}")
            return {
                "success": False,
                "error": "ASR service unavailable",
            }

class MockASRProvider(ASRProvider):
    """
    Development mock ASR provider.
    Only for testing when Sarvam is not configured.
    Does NOT fake successful transcription.
    """
    
    async def is_available(self) -> bool:
        return False
    
    async def transcribe(
        self,
        audio_data: bytes,
        language: str,
        mime_type: str = "audio/wav",
    ) -> Dict[str, Any]:
        return {
            "success": False,
            "error": "ASR not configured. Please use text input.",
        }