"""
Patient service for profile operations.
"""
from typing import Optional, Dict, Any
from app.db.repositories.patient_repository import patient_repository
from app.models.patient import PatientProfileUpdate
from app.services.storage.photo_storage import photo_storage_service
import logging

logger = logging.getLogger(__name__)

class PatientService:
    """Service for patient operations."""
    
    @staticmethod
    async def get_patient_by_user_id(user_id: str) -> Optional[Dict[str, Any]]:
        """Get patient profile by user ID."""
        return await patient_repository.find_by_user_id(user_id)
    
    @staticmethod
    async def get_or_create_patient(
        user: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Get existing patient profile or create from user data.
        """
        patient = await patient_repository.find_by_user_id(str(user["_id"]))
        
        if patient:
            return patient
        
        # Create patient from user data
        created_patient = await patient_repository.create_patient(
            user_id=str(user["_id"]),
            full_name=user["full_name"],
            email=user["email"],
            phone=user["phone"],
            gender=user.get("gender", "Prefer not to say"),
        )
        
        return created_patient
    
    @staticmethod
    async def update_patient_profile(
        user: Dict[str, Any],
        update_data: PatientProfileUpdate,
    ) -> Dict[str, Any]:
        """Update patient profile."""
        patient = await patient_repository.find_by_user_id(str(user["_id"]))
        
        if not patient:
            # Create patient first
            patient = await patient_repository.create_patient(
                user_id=str(user["_id"]),
                full_name=user["full_name"],
                email=user["email"],
                phone=user["phone"],
                gender=user.get("gender", "Prefer not to say"),
            )
            if not patient:
                return {"success": False, "error": "Failed to create patient profile."}
        
        # Prepare update data
        update_dict = {}
        if update_data.full_name is not None:
            update_dict["full_name"] = update_data.full_name
        if update_data.email is not None:
            update_dict["email"] = update_data.email
        if update_data.phone is not None:
            update_dict["phone"] = update_data.phone
        if update_data.gender is not None:
            update_dict["gender"] = update_data.gender
        if update_data.age is not None:
            update_dict["age"] = update_data.age
        if update_data.date_of_birth is not None:
            update_dict["date_of_birth"] = update_data.date_of_birth
        
        if not update_dict:
            return {"success": True, "message": "No changes", "patient": patient}
        
        success = await patient_repository.update_patient(
            str(patient["_id"]),
            update_dict,
        )
        
        if not success:
            return {"success": False, "error": "Failed to update patient profile."}
        
        updated_patient = await patient_repository.find_by_id(str(patient["_id"]))
        return {"success": True, "message": "Profile updated", "patient": updated_patient}
    
    @staticmethod
    async def save_patient_photo(
        user: Dict[str, Any],
        file_data: bytes,
        file_extension: str,
    ) -> Dict[str, Any]:
        """Save patient photo."""
        patient = await patient_repository.find_by_user_id(str(user["_id"]))
        
        if not patient:
            patient = await patient_repository.create_patient(
                user_id=str(user["_id"]),
                full_name=user["full_name"],
                email=user["email"],
                phone=user["phone"],
                gender=user.get("gender", "Prefer not to say"),
            )
            if not patient:
                return {"success": False, "error": "Failed to create patient profile."}
        
        # Delete old photo if exists
        old_photo = patient.get("photo_reference")
        if old_photo:
            await photo_storage_service.delete_photo(old_photo)
        
        # Save new photo
        photo_reference = await photo_storage_service.save_photo(file_data, file_extension)
        if not photo_reference:
            return {"success": False, "error": "Failed to save photo."}
        
        # Update patient record
        success = await patient_repository.update_photo_reference(
            str(patient["_id"]),
            photo_reference,
            True,
        )
        
        if not success:
            return {"success": False, "error": "Failed to update photo reference."}
        
        return {"success": True, "message": "Photo saved", "photo_reference": photo_reference}
    
    @staticmethod
    async def get_patient_photo(user: Dict[str, Any]) -> Dict[str, Any]:
        """Get patient photo."""
        patient = await patient_repository.find_by_user_id(str(user["_id"]))
        
        if not patient or not patient.get("photo_reference"):
            return {"success": False, "error": "No photo found."}
        
        photo_data = await photo_storage_service.get_photo(patient["photo_reference"])
        if not photo_data:
            return {"success": False, "error": "Photo not available."}
        
        return {"success": True, "photo_data": photo_data}
    
    @staticmethod
    async def delete_patient_photo(user: Dict[str, Any]) -> Dict[str, Any]:
        """Delete patient photo."""
        patient = await patient_repository.find_by_user_id(str(user["_id"]))
        
        if not patient or not patient.get("photo_reference"):
            return {"success": True, "message": "No photo to delete."}
        
        await photo_storage_service.delete_photo(patient["photo_reference"])
        await patient_repository.delete_photo(str(patient["_id"]))
        
        return {"success": True, "message": "Photo deleted."}

patient_service = PatientService()