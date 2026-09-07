"""
Photo validation utilities.
"""
from typing import Optional, Tuple
import magic
import logging

logger = logging.getLogger(__name__)

ALLOWED_MIME_TYPES = {
    'image/jpeg': 'jpg',
    'image/png': 'png',
    'image/webp': 'webp',
}

MAX_PHOTO_SIZE = 5 * 1024 * 1024  # 5MB

class PhotoValidator:
    """Validates patient photos."""
    
    @staticmethod
    def validate_photo(file_data: bytes) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate photo data.
        Returns (is_valid, error_message, file_extension).
        """
        if not file_data:
            return False, "No photo data provided.", None
        
        if len(file_data) > MAX_PHOTO_SIZE:
            return False, "Photo size exceeds maximum limit of 5MB.", None
        
        # Detect MIME type
        try:
            mime_type = magic.from_buffer(file_data, mime=True)
        except Exception:
            mime_type = None
        
        if mime_type not in ALLOWED_MIME_TYPES:
            return False, "Unsupported image format. Please use JPEG, PNG, or WebP.", None
        
        file_extension = ALLOWED_MIME_TYPES[mime_type]
        return True, None, file_extension
    
    @staticmethod
    def get_file_extension(mime_type: str) -> Optional[str]:
        """Get file extension from MIME type."""
        return ALLOWED_MIME_TYPES.get(mime_type)

photo_validator = PhotoValidator()