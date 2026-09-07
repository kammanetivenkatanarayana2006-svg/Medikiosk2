"""
Voice API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Response
from typing import Optional
from app.api.dependencies.auth import require_authenticated_user
from app.services.voice.voice_service import voice_service
from app.models.voice import ASRRequest, TTSRequest
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/voice", tags=["voice"])

@router.post("/asr")
async def transcribe_audio(
    interview_id: str = Form(...),
    language: str = Form(...),
    file: UploadFile = File(...),
    current_user: dict = Depends(require_authenticated_user),
):
    """
    Transcribe audio using ASR provider.
    """
    # Read audio data
    audio_data = await file.read()
    mime_type = file.content_type or "audio/wav"
    
    result = await voice_service.transcribe_audio(
        current_user,
        interview_id,
        audio_data,
        language,
        mime_type,
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"],
        )
    
    return {
        "success": True,
        "data": result["transcription"],
    }

@router.post("/tts")
async def synthesize_speech(
    request: TTSRequest,
    current_user: dict = Depends(require_authenticated_user),
):
    """
    Synthesize text to speech.
    Returns audio data.
    """
    result = await voice_service.synthesize_speech(
        current_user,
        request.interview_id,
        request.text,
        request.language,
        request.voice_id,
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=result.get("status_code", 400),
            detail=result["error"],
        )
    
    audio = result["audio"]
    return Response(
        content=audio["data"],
        media_type=audio["mime_type"],
        headers={"X-Provider": audio["provider"]},
    )