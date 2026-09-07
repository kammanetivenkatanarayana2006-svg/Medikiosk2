"""
Tests for authentication functionality.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app
from app.utils.security import security_utils

client = TestClient(app)

class TestAuthentication:
    """Test authentication endpoints."""

    def test_register_success(self):
        """Test successful registration."""
        with patch('app.db.repositories.user_repository.user_repository.find_by_email', new_callable=AsyncMock, return_value=None), \
             patch('app.db.repositories.user_repository.user_repository.find_by_phone', new_callable=AsyncMock, return_value=None), \
             patch('app.db.repositories.user_repository.user_repository.create_user', new_callable=AsyncMock) as mock_create:

            mock_create.return_value = {
                "_id": "507f1f77bcf86cd799439011",
                "full_name": "Test User",
                "email": "test@example.com",
                "phone": "9876543210",
                "role": "PATIENT",
                "email_verified": False,
                "phone_verified": False,
            }

            # Trying route without /api prefix first, then fallback
            response = client.post("/auth/register", json={
                "full_name": "Test User",
                "email": "test@example.com",
                "phone": "9876543210",
                "password": "Test@123",
            })
            if response.status_code == 404:
                response = client.post("/api/auth/register", json={
                    "full_name": "Test User",
                    "email": "test@example.com",
                    "phone": "9876543210",
                    "password": "Test@123",
                })

            assert response.status_code in [200, 201]
            data = response.json()
            assert "password" not in data

    def test_register_duplicate_email(self):
        """Test duplicate email registration."""
        with patch('app.db.repositories.user_repository.user_repository.find_by_email', new_callable=AsyncMock) as mock_find:
            mock_find.return_value = {"email": "test@example.com"}

            response = client.post("/auth/register", json={
                "full_name": "Test User",
                "email": "test@example.com",
                "phone": "9876543210",
                "password": "Test@123",
            })
            if response.status_code == 404:
                response = client.post("/api/auth/register", json={
                    "full_name": "Test User",
                    "email": "test@example.com",
                    "phone": "9876543210",
                    "password": "Test@123",
                })

            assert response.status_code in [400, 409]

    def test_register_invalid_email(self):
        """Test invalid email registration."""
        response = client.post("/auth/register", json={
            "full_name": "Test User",
            "email": "invalid-email",
            "phone": "9876543210",
            "password": "Test@123",
        })
        if response.status_code == 404:
            response = client.post("/api/auth/register", json={
                "full_name": "Test User",
                "email": "invalid-email",
                "phone": "9876543210",
                "password": "Test@123",
            })

        assert response.status_code == 422

    def test_register_weak_password(self):
        """Test weak password registration."""
        response = client.post("/auth/register", json={
            "full_name": "Test User",
            "email": "test@example.com",
            "phone": "9876543210",
            "password": "weak",
        })
        if response.status_code == 404:
            response = client.post("/api/auth/register", json={
                "full_name": "Test User",
                "email": "test@example.com",
                "phone": "9876543210",
                "password": "weak",
            })

        assert response.status_code in [400, 422]

    def test_login_success(self):
        """Test successful login."""
        mock_user = {
            "_id": "507f1f77bcf86cd799439011",
            "full_name": "Test User",
            "email": "test@example.com",
            "phone": "9876543210",
            "role": "PATIENT",
            "password_hash": security_utils.hash_password("Test@123"),
            "is_active": True,
        }

        with patch('app.db.repositories.user_repository.user_repository.find_by_email', new_callable=AsyncMock, return_value=mock_user), \
             patch('app.db.repositories.user_repository.user_repository.verify_credentials', new_callable=AsyncMock, return_value=mock_user):

            response = client.post("/auth/login", json={
                "username": "test@example.com",
                "email": "test@example.com",
                "password": "Test@123",
            })
            if response.status_code == 404:
                response = client.post("/api/auth/login", json={
                    "username": "test@example.com",
                    "email": "test@example.com",
                    "password": "Test@123",
                })

            if response.status_code == 422:
                response = client.post("/auth/login", data={
                    "username": "test@example.com",
                    "password": "Test@123",
                })

            assert response.status_code == 200
            data = response.json()
            assert "access_token" in data or "token" in data

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        with patch('app.db.repositories.user_repository.user_repository.find_by_email', new_callable=AsyncMock, return_value=None), \
             patch('app.db.repositories.user_repository.user_repository.verify_credentials', new_callable=AsyncMock, return_value=None):

            response = client.post("/auth/login", json={
                "email": "test@example.com",
                "password": "Wrong@123",
            })
            if response.status_code == 404:
                response = client.post("/api/auth/login", json={
                    "email": "test@example.com",
                    "password": "Wrong@123",
                })

            if response.status_code == 422:
                response = client.post("/auth/login", data={
                    "username": "test@example.com",
                    "password": "Wrong@123",
                })

            assert response.status_code in [400, 401]

    def test_protected_endpoint_without_token(self):
        """Test protected endpoint without token."""
        response = client.get("/auth/me")
        if response.status_code == 404:
            response = client.get("/api/auth/me")

        assert response.status_code in [401, 403]

    def test_password_hashing(self):
        """Test password hashing."""
        password = "Test@123"
        hashed = security_utils.hash_password(password)

        assert hashed != password
        assert security_utils.verify_password(password, hashed) is True
        assert security_utils.verify_password("Wrong@123", hashed) is False

    def test_jwt_creation_and_decode(self):
        """Test JWT creation and decoding."""
        token = security_utils.create_access_token(
            user_id="507f1f77bcf86cd799439011",
            role="PATIENT",
        )

        assert token is not None

        payload = security_utils.decode_access_token(token)
        assert payload is not None
        assert payload["sub"] == "507f1f77bcf86cd799439011"
        assert payload["role"] == "PATIENT"