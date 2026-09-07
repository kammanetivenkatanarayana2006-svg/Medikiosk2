"""
Tests for OTP functionality.
"""
import pytest
from app.services.otp_service import otp_service

class TestOTPService:
    def test_generate_otp(self):
        otp = otp_service.generate_otp()
        assert len(otp) == 6
        assert otp.isdigit()
    
    def test_hash_otp(self):
        otp = "123456"
        hashed = otp_service.hash_otp(otp)
        assert hashed != otp
        assert len(hashed) == 64  # SHA-256
    
    def test_verify_otp_hash(self):
        otp = "123456"
        hashed = otp_service.hash_otp(otp)
        assert otp_service.hash_otp("654321") != hashed
        assert otp_service.hash_otp(otp) == hashed