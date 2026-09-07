"""
Photo storage service with provider abstraction.
"""
import os
import uuid
import aiofiles
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class PhotoStorageProvider(ABC):
    """Abstract interface for photo storage."""
    
    @abstractmethod
    async def save_photo(self, file_data: bytes, file_extension: str) -> Optional[str]:
        """Save photo and return reference ID."""
        pass
    
    @abstractmethod
    async def get_photo(self, photo_reference: str) -> Optional[bytes]:
        """Get photo by reference."""
        pass
    
    @abstractmethod
    async def delete_photo(self, photo_reference: str) -> bool:
        """Delete photo by reference."""
        pass

class LocalPhotoStorage(PhotoStorageProvider):
    """Local filesystem photo storage for development."""
    
    def __init__(self):
        self.upload_dir = getattr(settings, 'PHOTO_UPLOAD_DIR', 'uploads/patient_photos')
        os.makedirs(self.upload_dir, exist_ok=True)
    
    async def save_photo(self, file_data: bytes, file_extension: str) -> Optional[str]:
        """Save photo to local filesystem."""
        try:
            photo_id = uuid.uuid4().hex
            filename = f"patient_photo_{photo_id}.{file_extension}"
            filepath = os.path.join(self.upload_dir, filename)
            
            async with aiofiles.open(filepath, 'wb') as f:
                await f.write(file_data)
            
            logger.info(f"Photo saved: {photo_id}")
            return filename
        except Exception as e:
            logger.error(f"Failed to save photo: {str(e)}")
            return None
    
    async def get_photo(self, photo_reference: str) -> Optional[bytes]:
        """Get photo from local filesystem."""
        try:
            filepath = os.path.join(self.upload_dir, photo_reference)
            async with aiofiles.open(filepath, 'rb') as f:
                return await f.read()
        except Exception:
            return None
    
    async def delete_photo(self, photo_reference: str) -> bool:
        """Delete photo from local filesystem."""
        try:
            filepath = os.path.join(self.upload_dir, photo_reference)
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Photo deleted: {photo_reference}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete photo: {str(e)}")
            return False

class PhotoStorageService:
    """Photo storage service."""
    
    def __init__(self):
        self.provider = self._get_provider()
    
    def _get_provider(self) -> PhotoStorageProvider:
        """Get photo storage provider."""
        provider_name = getattr(settings, 'PHOTO_STORAGE_PROVIDER', 'local').lower()
        
        if provider_name == 'local':
            return LocalPhotoStorage()
        # Future: Add cloud storage providers
        
        return LocalPhotoStorage()
    
    async def save_photo(self, file_data: bytes, file_extension: str) -> Optional[str]:
        """Save photo using provider."""
        return await self.provider.save_photo(file_data, file_extension)
    
    async def get_photo(self, photo_reference: str) -> Optional[bytes]:
        """Get photo using provider."""
        return await self.provider.get_photo(photo_reference)
    
    async def delete_photo(self, photo_reference: str) -> bool:
        """Delete photo using provider."""
        return await self.provider.delete_photo(photo_reference)

photo_storage_service = PhotoStorageService()