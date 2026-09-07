"""
Document storage service.
"""
import os
import uuid
import aiofiles
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class DocumentStorageProvider(ABC):
    """Abstract interface for document storage."""
    
    @abstractmethod
    async def save(self, file_data: bytes, file_extension: str) -> Optional[str]:
        """Save document and return storage key."""
        pass
    
    @abstractmethod
    async def get(self, storage_key: str) -> Optional[bytes]:
        """Get document by storage key."""
        pass
    
    @abstractmethod
    async def delete(self, storage_key: str) -> bool:
        """Delete document by storage key."""
        pass

class LocalDocumentStorage(DocumentStorageProvider):
    """Local filesystem storage for development."""
    
    def __init__(self):
        self.upload_dir = getattr(settings, 'MEDICAL_DOCS_DIR', 'uploads/medical_documents')
        os.makedirs(self.upload_dir, exist_ok=True)
    
    async def save(self, file_data: bytes, file_extension: str) -> Optional[str]:
        """Save document to local filesystem."""
        try:
            storage_key = f"doc_{uuid.uuid4().hex}.{file_extension}"
            filepath = os.path.join(self.upload_dir, storage_key)
            
            async with aiofiles.open(filepath, 'wb') as f:
                await f.write(file_data)
            
            logger.info(f"Document saved: {storage_key}")
            return storage_key
        except Exception as e:
            logger.error(f"Failed to save document: {str(e)}")
            return None
    
    async def get(self, storage_key: str) -> Optional[bytes]:
        """Get document from local filesystem."""
        try:
            filepath = os.path.join(self.upload_dir, storage_key)
            async with aiofiles.open(filepath, 'rb') as f:
                return await f.read()
        except Exception:
            return None
    
    async def delete(self, storage_key: str) -> bool:
        """Delete document from local filesystem."""
        try:
            filepath = os.path.join(self.upload_dir, storage_key)
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Document deleted: {storage_key}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete document: {str(e)}")
            return False

class DocumentStorageService:
    """Document storage service."""
    
    def __init__(self):
        self.provider = self._get_provider()
    
    def _get_provider(self) -> DocumentStorageProvider:
        provider_name = getattr(settings, 'DOCUMENT_STORAGE_PROVIDER', 'local').lower()
        if provider_name == 'local':
            return LocalDocumentStorage()
        return LocalDocumentStorage()
    
    async def save(self, file_data: bytes, file_extension: str) -> Optional[str]:
        return await self.provider.save(file_data, file_extension)
    
    async def get(self, storage_key: str) -> Optional[bytes]:
        return await self.provider.get(storage_key)
    
    async def delete(self, storage_key: str) -> bool:
        return await self.provider.delete(storage_key)

document_storage_service = DocumentStorageService()