"""
OCR provider abstraction.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class OCRProvider(ABC):
    """Abstract interface for OCR providers."""
    
    @abstractmethod
    async def extract_text(
        self,
        file_data: bytes,
        mime_type: str,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Extract text from document.
        Returns dict with text, page_count, language, confidence.
        """
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """Check if OCR provider is available."""
        pass

class TesseractOCRProvider(OCRProvider):
    """
    Tesseract OCR provider using pytesseract.
    Local OCR engine.
    """
    
    def __init__(self):
        self.name = "tesseract"
        self.version = "local"
    
    async def is_available(self) -> bool:
        """Check if Tesseract is available."""
        try:
            import pytesseract
            return True
        except ImportError:
            return False
    
    async def extract_text(
        self,
        file_data: bytes,
        mime_type: str,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Extract text using Tesseract."""
        try:
            import pytesseract
            from PIL import Image
            import io
            
            image = Image.open(io.BytesIO(file_data))
            text = pytesseract.image_to_string(image)
            
            return {
                "success": True,
                "text": text.strip(),
                "page_count": 1,
                "language": language,
                "confidence": None,
                "provider": self.name,
            }
        except Exception as e:
            logger.error(f"Tesseract OCR failed: {str(e)}")
            return {
                "success": False,
                "error": "OCR processing failed",
            }

class PDFTextExtractorProvider(OCRProvider):
    """
    PDF text extractor using PyPDF2.
    Extracts selectable text from PDFs.
    """
    
    def __init__(self):
        self.name = "pdf_text_extractor"
        self.version = "local"
    
    async def is_available(self) -> bool:
        """Check if PyPDF2 is available."""
        try:
            import PyPDF2
            return True
        except ImportError:
            return False
    
    async def extract_text(
        self,
        file_data: bytes,
        mime_type: str,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Extract text from PDF."""
        try:
            import PyPDF2
            import io
            
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_data))
            text_parts = []
            page_count = len(pdf_reader.pages)
            
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            
            full_text = "\n\n".join(text_parts)
            
            if not full_text.strip():
                return {
                    "success": False,
                    "error": "No selectable text in PDF. Requires image OCR.",
                }
            
            return {
                "success": True,
                "text": full_text.strip(),
                "page_count": page_count,
                "language": language,
                "confidence": None,
                "provider": self.name,
            }
        except Exception as e:
            logger.error(f"PDF text extraction failed: {str(e)}")
            return {
                "success": False,
                "error": "PDF processing failed",
            }

class MockOCRProvider(OCRProvider):
    """
    Mock OCR provider for when no OCR engine is configured.
    Does NOT fake successful extraction.
    """
    
    async def is_available(self) -> bool:
        return False
    
    async def extract_text(
        self,
        file_data: bytes,
        mime_type: str,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        return {
            "success": False,
            "error": "OCR not configured",
        }