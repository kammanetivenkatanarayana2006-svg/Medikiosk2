"""
Tests for email verification.
"""
import pytest
from app.services.email_verification_service import email_verification_service

class TestEmailVerification:
    def test_generate_token(self):
        token = email_verification_service.generate_token()
        assert len(token) > 32
        assert token != email_verification_service.generate_token()
    
    def test_hash_token(self):
        token = "test-token-123"
        hashed = email_verification_service.hash_token(token)
        assert hashed != token
        assert len(hashed) == 64