"""
Medical document service.
"""
from typing import Optional, Dict, Any, List
from app.db.repositories.medical_document_repository import medical_document_repository
from app.db.repositories.patient_repository import patient_repository
from app.db.repositories.consultation_repository import consultation_repository
from app.services.storage.document_storage import document_storage_service
from app.services.ocr.ocr_provider import TesseractOCRProvider, PDFTextExtractorProvider, MockOCRProvider
from app.models.medical_document import ALLOWED_MIME_TYPES, MAX_DOCUMENT_SIZE
import logging

logger = logging.getLogger(__name__)

class MedicalDocumentService:
    """Service for medical document operations."""
    
    def __init__(self):
        self.tesseract_ocr = TesseractOCRProvider()
        self.pdf_extractor = PDFTextExtractorProvider()
        self.mock_ocr = MockOCRProvider()
    
    async def upload_document(
        self,
        user: Dict[str, Any],
        file_data: bytes,
        filename: str,
        mime_type: str,
        consultation_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Upload and process medical document."""
        # Validate file
        validation = await self._validate_file(file_data, mime_type, filename)
        if not validation["success"]:
            return validation
        
        file_extension = validation["file_extension"]
        document_type = validation["document_type"]
        
        # Get patient
        patient = await patient_repository.find_by_user_id(str(user["_id"]))
        if not patient:
            return {"success": False, "error": "Patient profile not found.", "status_code": 404}
        
        # Verify consultation ownership if provided
        if consultation_id:
            consultation = await consultation_repository.find_by_id(consultation_id)
            if not consultation:
                return {"success": False, "error": "Consultation not found.", "status_code": 404}
            if str(consultation.get("user_id")) != str(user["_id"]):
                return {"success": False, "error": "Access denied.", "status_code": 403}
        
        # Store document securely
        storage_key = await document_storage_service.save(file_data, file_extension)
        if not storage_key:
            return {"success": False, "error": "Failed to store document.", "status_code": 500}
        
        # Create database record
        document = await medical_document_repository.create_document(
            patient_id=str(patient["_id"]),
            user_id=str(user["_id"]),
            consultation_id=consultation_id,
            original_filename=self._sanitize_filename(filename),
            document_type=document_type,
            mime_type=mime_type,
            file_size=len(file_data),
            storage_key=storage_key,
        )
        
        if not document:
            await document_storage_service.delete(storage_key)
            return {"success": False, "error": "Failed to create document record.", "status_code": 500}
        
        # Process OCR
        await self._process_ocr(str(document["_id"]), file_data, mime_type, patient, consultation_id)
        
        return {
            "success": True,
            "message": "Document uploaded and processed",
            "document": {
                "id": str(document["_id"]),
                "original_filename": document["original_filename"],
                "document_type": document["document_type"],
                "file_size": document["file_size"],
                "ocr_status": document["ocr_status"],
                "processing_status": document["processing_status"],
            },
            "status_code": 201,
        }
    
    async def _validate_file(self, file_data: bytes, mime_type: str, filename: str) -> Dict[str, Any]:
        """Validate uploaded file."""
        if not file_data:
            return {"success": False, "error": "No file data provided.", "status_code": 400}
        
        if len(file_data) > MAX_DOCUMENT_SIZE:
            return {"success": False, "error": "File too large. Maximum 10MB.", "status_code": 400}
        
        if mime_type not in ALLOWED_MIME_TYPES:
            return {"success": False, "error": "Unsupported file format.", "status_code": 400}
        
        file_extension = ALLOWED_MIME_TYPES[mime_type]
        document_type = "pdf" if file_extension == "pdf" else "image"
        
        return {
            "success": True,
            "file_extension": file_extension,
            "document_type": document_type,
        }
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal."""
        import os
        basename = os.path.basename(filename)
        # Remove suspicious characters
        safe = "".join(c for c in basename if c.isalnum() or c in "._- ")
        return safe[:200] or "document"
    
    async def _process_ocr(
        self,
        document_id: str,
        file_data: bytes,
        mime_type: str,
        patient: Dict[str, Any],
        consultation_id: Optional[str],
    ):
        """Process document through OCR."""
        await medical_document_repository.update_ocr_status(document_id, "processing")
        
        try:
            # Choose provider based on document type
            result = None
            
            if mime_type == "application/pdf":
                # Try PDF text extraction first
                result = await self.pdf_extractor.extract_text(file_data, mime_type)
                
                if not result.get("success"):
                    # Try OCR on PDF (if image-based)
                    result = await self.tesseract_ocr.extract_text(file_data, mime_type)
            else:
                # Image OCR
                result = await self.tesseract_ocr.extract_text(file_data, mime_type)
            
            if result and result.get("success"):
                # Save OCR result
                await medical_document_repository.save_ocr_result(
                    medical_document_id=document_id,
                    patient_id=str(patient["_id"]),
                    consultation_id=consultation_id,
                    text=result.get("text", ""),
                    page_count=result.get("page_count", 1),
                    language=result.get("language"),
                    ocr_provider=result.get("provider", "unknown"),
                )
                
                await medical_document_repository.update_ocr_status(document_id, "completed")
            else:
                await medical_document_repository.update_ocr_status(document_id, "failed")
        
        except Exception as e:
            logger.error(f"OCR processing failed: {str(e)}")
            await medical_document_repository.update_ocr_status(document_id, "failed")
    
    async def get_patient_documents(
        self,
        user: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Get all documents for patient."""
        patient = await patient_repository.find_by_user_id(str(user["_id"]))
        if not patient:
            return {"success": False, "error": "Patient not found.", "status_code": 404}
        
        documents = await medical_document_repository.find_by_patient_id(str(patient["_id"]))
        
        return {
            "success": True,
            "documents": documents,
        }
    
    async def get_document(
        self,
        user: Dict[str, Any],
        document_id: str,
    ) -> Dict[str, Any]:
        """Get document with ownership check."""
        document = await medical_document_repository.find_by_id(document_id)
        
        if not document:
            return {"success": False, "error": "Document not found.", "status_code": 404}
        
        if str(document.get("user_id")) != str(user["_id"]):
            return {"success": False, "error": "Access denied.", "status_code": 403}
        
        return {
            "success": True,
            "document": document,
        }
    
    async def get_document_ocr(
        self,
        user: Dict[str, Any],
        document_id: str,
    ) -> Dict[str, Any]:
        """Get OCR result for document."""
        document = await medical_document_repository.find_by_id(document_id)
        
        if not document:
            return {"success": False, "error": "Document not found.", "status_code": 404}
        
        if str(document.get("user_id")) != str(user["_id"]):
            return {"success": False, "error": "Access denied.", "status_code": 403}
        
        ocr_result = await medical_document_repository.get_ocr_result(document_id)
        
        if not ocr_result:
            return {"success": False, "error": "OCR result not found.", "status_code": 404}
        
        return {
            "success": True,
            "ocr_result": ocr_result,
        }
    
    async def delete_document(
        self,
        user: Dict[str, Any],
        document_id: str,
    ) -> Dict[str, Any]:
        """Delete document with ownership check."""
        document = await medical_document_repository.find_by_id(document_id)
        
        if not document:
            return {"success": False, "error": "Document not found.", "status_code": 404}
        
        if str(document.get("user_id")) != str(user["_id"]):
            return {"success": False, "error": "Access denied.", "status_code": 403}
        
        # Delete file from storage
        await document_storage_service.delete(document.get("storage_key", ""))
        
        # Delete OCR result
        await medical_document_repository.delete_ocr_result(document_id)
        
        # Delete database record
        await medical_document_repository.delete_document(document_id)
        
        return {"success": True, "message": "Document deleted."}

medical_document_service = MedicalDocumentService()