"""
Medical document repository.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from bson import ObjectId
from app.db.database import DatabaseRepository
from app.db.connection import mongo_connection
import logging

logger = logging.getLogger(__name__)

class MedicalDocumentRepository(DatabaseRepository):
    """Repository for medical documents."""
    
    def __init__(self):
        super().__init__("medical_documents")
    
    async def create_indexes(self):
        """Create indexes."""
        if not mongo_connection.is_connected:
            return
        
        try:
            collection = mongo_connection.database["medical_documents"]
            await collection.create_index("patient_id")
            await collection.create_index("user_id")
            await collection.create_index("consultation_id")
            await collection.create_index("ocr_status")
            await collection.create_index([("created_at", -1)])
            
            # OCR results collection
            ocr_collection = mongo_connection.database["ocr_results"]
            await ocr_collection.create_index("medical_document_id", unique=True)
            await ocr_collection.create_index("patient_id")
            
            logger.info("Medical document indexes created")
        except Exception as e:
            logger.error(f"Failed to create document indexes: {str(e)}")
    
    async def create_document(
        self,
        patient_id: str,
        user_id: str,
        consultation_id: Optional[str],
        original_filename: str,
        document_type: str,
        mime_type: str,
        file_size: int,
        storage_key: str,
        ocr_status: str = "pending",
    ) -> Optional[Dict[str, Any]]:
        """Create medical document record."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        now = datetime.now(timezone.utc)
        
        doc = {
            "patient_id": patient_id,
            "user_id": user_id,
            "consultation_id": consultation_id,
            "original_filename": original_filename,
            "document_type": document_type,
            "mime_type": mime_type,
            "file_size": file_size,
            "storage_key": storage_key,
            "ocr_status": ocr_status,
            "processing_status": "uploaded",
            "uploaded_at": now,
            "updated_at": now,
        }
        
        try:
            result = await collection.insert_one(doc)
            doc["_id"] = result.inserted_id
            return doc
        except Exception as e:
            logger.error(f"Failed to create document: {str(e)}")
            return None
    
    async def find_by_id(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Find document by ID."""
        collection = await self.get_collection()
        if collection is None:
            return None
        
        try:
            obj_id = ObjectId(document_id)
            return await collection.find_one({"_id": obj_id})
        except Exception:
            return None
    
    async def find_by_patient_id(self, patient_id: str) -> List[Dict[str, Any]]:
        """Find documents by patient ID."""
        collection = await self.get_collection()
        if collection is None:
            return []
        
        try:
            cursor = collection.find({"patient_id": patient_id}).sort("created_at", -1)
            return await cursor.to_list(length=100)
        except Exception:
            return []
    
    async def update_ocr_status(
        self,
        document_id: str,
        ocr_status: str,
    ) -> bool:
        """Update document OCR status."""
        collection = await self.get_collection()
        if collection is None:
            return False
        
        try:
            obj_id = ObjectId(document_id)
            result = await collection.update_one(
                {"_id": obj_id},
                {
                    "$set": {
                        "ocr_status": ocr_status,
                        "updated_at": datetime.now(timezone.utc),
                    }
                }
            )
            return result.modified_count > 0
        except Exception:
            return False
    
    async def delete_document(self, document_id: str) -> bool:
        """Delete document record."""
        collection = await self.get_collection()
        if collection is None:
            return False
        
        try:
            obj_id = ObjectId(document_id)
            result = await collection.delete_one({"_id": obj_id})
            return result.deleted_count > 0
        except Exception:
            return False
    
    async def save_ocr_result(
        self,
        medical_document_id: str,
        patient_id: str,
        consultation_id: Optional[str],
        text: str,
        page_count: int,
        language: Optional[str],
        ocr_provider: str,
        status: str = "completed",
    ) -> Optional[Dict[str, Any]]:
        """Save OCR result."""
        collection = mongo_connection.database["ocr_results"]
        if collection is None:
            return None
        
        now = datetime.now(timezone.utc)
        
        ocr_doc = {
            "medical_document_id": medical_document_id,
            "patient_id": patient_id,
            "consultation_id": consultation_id,
            "text": text,
            "page_count": page_count,
            "language": language,
            "ocr_provider": ocr_provider,
            "status": status,
            "created_at": now,
            "updated_at": now,
        }
        
        try:
            result = await collection.insert_one(ocr_doc)
            ocr_doc["_id"] = result.inserted_id
            return ocr_doc
        except Exception as e:
            logger.error(f"Failed to save OCR result: {str(e)}")
            return None
    
    async def get_ocr_result(self, medical_document_id: str) -> Optional[Dict[str, Any]]:
        """Get OCR result for document."""
        collection = mongo_connection.database["ocr_results"]
        if collection is None:
            return None
        
        try:
            return await collection.find_one({"medical_document_id": medical_document_id})
        except Exception:
            return None
    
    async def delete_ocr_result(self, medical_document_id: str) -> bool:
        """Delete OCR result."""
        collection = mongo_connection.database["ocr_results"]
        if collection is None:
            return False
        
        try:
            result = await collection.delete_one({"medical_document_id": medical_document_id})
            return result.deleted_count > 0
        except Exception:
            return False

medical_document_repository = MedicalDocumentRepository()