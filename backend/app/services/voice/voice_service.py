"""
Voice service for ASR and TTS operations.
"""
from typing import Optional, Dict, Any
from app.services.voice.asr_provider import SarvamASRProvider, MockASRProvider
from app.services.voice.tts_provider import SarvamTTSProvider, MockTTSProvider
from app.db.repositories.interview_repository import interview_repository
from app.utils.photo_validation import MAX_PHOTO_SIZE
import logging

logger = logging.getLogger(__name__)

MAX_AUDIO_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_AUDIO_TYPES = ["audio/wav", "audio/mp3", "audio/mpeg", "audio/webm", "audio/ogg"]

class VoiceService:
    """Service for voice operations."""
    
    def __init__(self):
        self.asr_provider = self._get_asr_provider()
        self.tts_provider = self._get_tts_provider()
    
    def _get_asr_provider(self):
        """Get ASR provider based on configuration."""
        from app.core.config import settings
        if settings.SARVAM_API_KEY:
            return SarvamASRProvider()
        return MockASRProvider()
    
    def _get_tts_provider(self):
        """Get TTS provider based on configuration."""
        from app.core.config import settings
        tts_provider = getattr(settings, 'TTS_PROVIDER', '').lower()
        if tts_provider == 'sarvam' and settings.SARVAM_API_KEY:
            return SarvamTTSProvider()
        return MockTTSProvider()
    
    async def verify_interview_ownership(
        self,
        user: Dict[str, Any],
        interview_id: str,
    ) -> Dict[str, Any]:
        """Verify user owns the interview."""
        interview = await interview_repository.find_by_id(interview_id)
        
        if not interview:
            return {"success": False, "error": "Interview not found.", "status_code": 404}
        
        if str(interview.get("user_id")) != str(user["_id"]):
            return {"success": False, "error": "Access denied.", "status_code": 403}
        
        if interview.get("status") not in ["in_progress", "ready"]:
            return {"success": False, "error": "Interview is not active.", "status_code": 400}
        
        return {"success": True, "interview": interview}
    
    async def transcribe_audio(
        self,
        user: Dict[str, Any],
        interview_id: str,
        audio_data: bytes,
        language: str,
        mime_type: str,
    ) -> Dict[str, Any]:
        """Transcribe audio to text."""
        # Verify ownership
        ownership = await self.verify_interview_ownership(user, interview_id)
        if not ownership["success"]:
            return ownership
        
        # Validate audio
        if not audio_data:
            return {"success": False, "error": "No audio data provided.", "status_code": 400}
        
        if len(audio_data) > MAX_AUDIO_SIZE:
            return {"success": False, "error": "Audio file too large.", "status_code": 400}
        
        if mime_type not in ALLOWED_AUDIO_TYPES:
            return {"success": False, "error": "Unsupported audio format.", "status_code": 400}
        
        # Check ASR provider
        if not await self.asr_provider.is_available():
            return {
                "success": False,
                "error": "Voice transcription is not configured. Please use text input.",
                "status_code": 503,
            }
        
        # Transcribe
        result = await self.asr_provider.transcribe(audio_data, language, mime_type)
        
        if not result.get("success"):
            return {
                "success": False,
                "error": result.get("error", "Transcription failed."),
                "status_code": 502,
            }
        
        return {
            "success": True,
            "transcription": {
                "text": result["text"],
                "language": result.get("language", language),
                "provider": result.get("provider", "sarvam"),
                "confidence": result.get("confidence"),
            },
        }
    
    async def synthesize_speech(
        self,
        user: Dict[str, Any],
        interview_id: str,
        text: str,
        language: str,
        voice_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Synthesize text to speech."""
        # Verify ownership
        ownership = await self.verify_interview_ownership(user, interview_id)
        if not ownership["success"]:
            return ownership
        
        # Check TTS provider
        if not await self.tts_provider.is_available():
            return {
                "success": False,
                "error": "Voice playback is not configured.",
                "status_code": 503,
            }
        
        # Synthesize
        result = await self.tts_provider.synthesize(text, language, voice_id)
        
        if not result.get("success"):
            return {
                "success": False,
                "error": result.get("error", "Speech synthesis failed."),
                "status_code": 502,
            }
        
        return {
            "success": True,
            "audio": {
                "data": result["audio_data"],
                "mime_type": result.get("mime_type", "audio/wav"),
                "provider": result.get("provider"),
            },
        }

voice_service = VoiceService()