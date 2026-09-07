"""
Interview service for clinical interview management.
"""
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from app.db.repositories.interview_repository import interview_repository
from app.db.repositories.consultation_repository import consultation_repository
from app.db.repositories.patient_repository import patient_repository
from app.data.interview_questions import (
    get_question_by_id,
    get_first_question,
    get_next_question,
    get_question_text,
    INTERVIEW_QUESTIONS,
)
from app.models.interview import VALID_TRANSITIONS, INTERVIEW_STATUS
import logging

logger = logging.getLogger(__name__)

class InterviewService:
    """Service for interview operations."""
    
    @staticmethod
    async def create_interview(
        user: Dict[str, Any],
        consultation_id: str,
    ) -> Dict[str, Any]:
        """Create interview session for authenticated patient."""
        # Get consultation
        consultation = await consultation_repository.find_by_id(consultation_id)
        if not consultation:
            return {"success": False, "error": "Consultation not found.", "status_code": 404}
        
        # Verify ownership
        if str(consultation.get("user_id")) != str(user["_id"]):
            return {"success": False, "error": "Access denied.", "status_code": 403}
        
        # Check if interview already exists
        existing = await interview_repository.find_by_consultation_id(consultation_id)
        if existing:
            return {
                "success": True,
                "message": "Interview already exists",
                "interview": existing,
            }
        
        # Get patient
        patient = await patient_repository.find_by_user_id(str(user["_id"]))
        if not patient:
            return {"success": False, "error": "Patient profile not found.", "status_code": 404}
        
        # Create interview
        interview = await interview_repository.create_interview(
            consultation_id=consultation_id,
            patient_id=str(patient["_id"]),
            user_id=str(user["_id"]),
            language=consultation.get("language", "english"),
            consultation_type=consultation.get("consultation_type", "general"),
        )
        
        if not interview:
            return {"success": False, "error": "Failed to create interview.", "status_code": 500}
        
        return {
            "success": True,
            "message": "Interview created",
            "interview": interview,
        }
    
    @staticmethod
    async def start_interview(
        user: Dict[str, Any],
        interview_id: str,
    ) -> Dict[str, Any]:
        """Start interview (ready → in_progress)."""
        interview = await interview_repository.find_by_id(interview_id)
        
        if not interview:
            return {"success": False, "error": "Interview not found.", "status_code": 404}
        
        if str(interview.get("user_id")) != str(user["_id"]):
            return {"success": False, "error": "Access denied.", "status_code": 403}
        
        current_status = interview.get("status")
        if current_status not in VALID_TRANSITIONS or "in_progress" not in VALID_TRANSITIONS.get(current_status, []):
            return {"success": False, "error": f"Cannot start from status: {current_status}", "status_code": 400}
        
        success = await interview_repository.update_interview(
            interview_id,
            {
                "status": "in_progress",
                "started_at": datetime.now(timezone.utc),
                "progress": 5.0,
            }
        )
        
        if not success:
            return {"success": False, "error": "Failed to start interview.", "status_code": 500}
        
        return {"success": True, "message": "Interview started"}
    
    @staticmethod
    async def get_interview(
        user: Dict[str, Any],
        interview_id: str,
    ) -> Dict[str, Any]:
        """Get interview with ownership check."""
        interview = await interview_repository.find_by_id(interview_id)
        
        if not interview:
            return {"success": False, "error": "Interview not found.", "status_code": 404}
        
        if str(interview.get("user_id")) != str(user["_id"]):
            return {"success": False, "error": "Access denied.", "status_code": 403}
        
        # Get responses
        responses = await interview_repository.get_responses(interview_id)
        
        # Get current question
        current_question_id = interview.get("current_question_id")
        current_question = get_question_by_id(current_question_id)
        
        question_text = ""
        question_options = []
        question_type = "open_text"
        
        if current_question:
            language = interview.get("language", "english")
            question_text = get_question_text(current_question, language)
            question_options = current_question.get("options", {}).get(language, [])
            question_type = current_question.get("question_type", "open_text")
        
        return {
            "success": True,
            "interview": interview,
            "responses": responses,
            "current_question": {
                "question_id": current_question_id,
                "text": question_text,
                "question_type": question_type,
                "options": question_options,
                "section": interview.get("current_section"),
            },
            "progress": interview.get("progress", 0),
        }
    
    @staticmethod
    async def submit_response(
        user: Dict[str, Any],
        interview_id: str,
        question_id: str,
        response_text: str,
        input_method: str = "text",
    ) -> Dict[str, Any]:
        """Submit interview response."""
        interview = await interview_repository.find_by_id(interview_id)
        
        if not interview:
            return {"success": False, "error": "Interview not found.", "status_code": 404}
        
        if str(interview.get("user_id")) != str(user["_id"]):
            return {"success": False, "error": "Access denied.", "status_code": 403}
        
        if interview.get("status") not in ["in_progress", "ready"]:
            return {"success": False, "error": "Interview is not active.", "status_code": 400}
        
        # Follow-up and AI clarification answers use client-generated IDs
        # that are not part of INTERVIEW_QUESTIONS and do not advance the
        # interview. They are recorded as extra responses against the
        # current state.
        is_clarification = question_id.startswith("followup_") or question_id.startswith("ai_")
        
        # Verify question matches current question
        if not is_clarification and question_id != interview.get("current_question_id"):
            return {"success": False, "error": "Invalid question for current state.", "status_code": 400}
        
        # Check if already answered
        has_response = await interview_repository.has_response(interview_id, question_id)
        if has_response:
            return {"success": False, "error": "Question already answered.", "status_code": 409}
        
        # Get question definition
        question = get_question_by_id(question_id)
        if not question and not is_clarification:
            return {"success": False, "error": "Question not found.", "status_code": 404}
        
        section = question.get("section") if question else interview.get("current_section", "")
        
        # Save response
        saved = await interview_repository.save_response(
            interview_id=interview_id,
            question_id=question_id,
            response_text=response_text.strip(),
            input_method=input_method,
            language=interview.get("language", "english"),
            section=section,
        )
        
        if not saved:
            return {"success": False, "error": "Failed to save response.", "status_code": 500}
        
        if is_clarification:
            # Keep the current question pending - the interview advances
            # only when a standard question is answered.
            return {
                "success": True,
                "message": "Response saved",
                "response_id": str(saved["_id"]),
                "next_question_id": interview.get("current_question_id"),
                "next_section": interview.get("current_section"),
                "progress": interview.get("progress", 0),
            }
        
        # Get next question
        next_question = get_next_question(question_id)
        
        if next_question:
            # Update current question and progress
            total_questions = len(INTERVIEW_QUESTIONS)
            answered_count = len(await interview_repository.get_responses(interview_id))
            progress = (answered_count / total_questions) * 100
            
            await interview_repository.update_interview(
                interview_id,
                {
                    "current_question_id": next_question["question_id"],
                    "current_section": next_question["section"],
                    "progress": round(progress, 1),
                }
            )
            
            return {
                "success": True,
                "message": "Response saved",
                "response_id": str(saved["_id"]),
                "next_question_id": next_question["question_id"],
                "next_section": next_question["section"],
                "progress": round(progress, 1),
            }
        else:
            # Interview complete
            await interview_repository.update_interview(
                interview_id,
                {
                    "status": "completed",
                    "completed_at": datetime.now(timezone.utc),
                    "progress": 100.0,
                }
            )
            
            return {
                "success": True,
                "message": "Interview completed",
                "response_id": str(saved["_id"]),
                "completed": True,
                "progress": 100.0,
            }
    
    @staticmethod
    async def pause_interview(
        user: Dict[str, Any],
        interview_id: str,
    ) -> Dict[str, Any]:
        """Pause interview."""
        return await InterviewService._change_status(user, interview_id, "paused")
    
    @staticmethod
    async def resume_interview(
        user: Dict[str, Any],
        interview_id: str,
    ) -> Dict[str, Any]:
        """Resume interview."""
        return await InterviewService._change_status(user, interview_id, "in_progress")
    
    @staticmethod
    async def cancel_interview(
        user: Dict[str, Any],
        interview_id: str,
    ) -> Dict[str, Any]:
        """Cancel interview."""
        return await InterviewService._change_status(user, interview_id, "cancelled")
    
    @staticmethod
    async def _change_status(
        user: Dict[str, Any],
        interview_id: str,
        new_status: str,
    ) -> Dict[str, Any]:
        """Change interview status with validation."""
        interview = await interview_repository.find_by_id(interview_id)
        
        if not interview:
            return {"success": False, "error": "Interview not found.", "status_code": 404}
        
        if str(interview.get("user_id")) != str(user["_id"]):
            return {"success": False, "error": "Access denied.", "status_code": 403}
        
        current_status = interview.get("status")
        valid_transitions = VALID_TRANSITIONS.get(current_status, [])
        
        if new_status not in valid_transitions:
            return {
                "success": False,
                "error": f"Cannot transition from {current_status} to {new_status}",
                "status_code": 400,
            }
        
        update_data = {"status": new_status}
        
        if new_status == "completed":
            update_data["completed_at"] = datetime.now(timezone.utc)
        
        success = await interview_repository.update_interview(interview_id, update_data)
        
        if not success:
            return {"success": False, "error": f"Failed to {new_status} interview.", "status_code": 500}
        
        return {"success": True, "message": f"Interview {new_status}"}

interview_service = InterviewService()