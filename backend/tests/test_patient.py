"""
Tests for patient profile functionality.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app
from app.api.dependencies.auth import get_current_user


client = TestClient(app)


class TestPatientProfile:
    """Test patient profile endpoints."""

    def test_unauthenticated_access(self):
        """Test unauthenticated access is rejected."""
        response = client.get("/api/patients/me")
        assert response.status_code == 401

    def test_get_patient_profile(self):
        """Test getting patient profile."""

        mock_user = {
            "_id": "507f1f77bcf86cd799439011",
            "full_name": "Test User",
            "email": "test@example.com",
            "phone": "9876543210",
            "role": "PATIENT",
        }

        mock_patient = {
            "_id": "507f1f77bcf86cd799439012",
            "user_id": "507f1f77bcf86cd799439011",
            "full_name": "Test User",
            "email": "test@example.com",
            "phone": "9876543210",
            "gender": "Male",
            "photo_reference": None,
            "photo_consent": False,
        }

        async def override_get_current_user():
            return mock_user

        app.dependency_overrides[
            get_current_user
        ] = override_get_current_user

        try:
            with patch(
                "app.services.patient_service.patient_repository.find_by_user_id",
                new_callable=AsyncMock,
                return_value=mock_patient,
            ):
                response = client.get("/api/patients/me")

            assert response.status_code == 200

        finally:
            app.dependency_overrides.clear()