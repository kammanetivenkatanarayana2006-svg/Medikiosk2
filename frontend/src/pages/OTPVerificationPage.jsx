import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import { useAuth } from '../contexts/AuthContext';
import { authService } from '../services/auth';
import styles from './OTPVerificationPage.module.css';

const OTPVerificationPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [resendCooldown, setResendCooldown] = useState(0);
  const inputRefs = useRef([]);
  
  useEffect(() => {
    inputRefs.current[0]?.focus();
  }, []);
  
  useEffect(() => {
    if (resendCooldown > 0) {
      const timer = setTimeout(() => setResendCooldown(resendCooldown - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [resendCooldown]);
  
  const handleChange = (index, value) => {
    const newOtp = [...otp];
    newOtp[index] = value.replace(/\D/g, '').slice(0, 1);
    setOtp(newOtp);
    
    if (value && index < 5) {
      inputRefs.current[index + 1]?.focus();
    }
  };
  
  const handleKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !otp[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };
  
  const handlePaste = (e) => {
    e.preventDefault();
    const pastedData = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6);
    const newOtp = [...otp];
    pastedData.split('').forEach((char, index) => {
      if (index < 6) newOtp[index] = char;
    });
    setOtp(newOtp);
    inputRefs.current[Math.min(pastedData.length, 5)]?.focus();
  };
  
  const handleVerify = async () => {
    const otpString = otp.join('');
    if (otpString.length !== 6) {
      setError('Please enter all 6 digits.');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    const result = await authService.verifyPhone(otpString);
    
    setLoading(false);
    
    if (result.success) {
      navigate('/email-verification');
    } else {
      setError(result.error);
    }
  };
  
  const handleResend = async () => {
    if (resendCooldown > 0) return;
    
    setLoading(true);
    setError(null);
    
    const result = await authService.requestPhoneOTP();
    
    setLoading(false);
    
    if (result.success) {
      setResendCooldown(30);
    } else {
      setError(result.error);
    }
  };
  
  return (
    <div className={styles.container}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <h1 className={`${styles.title} text-h1`}>
          Verify Your Phone
        </h1>
        <p className={`${styles.subtitle} text-body-lg`}>
          Enter the 6-digit verification code sent to your registered mobile number.
        </p>
        
        {error && (
          <div className={styles.error} role="alert">
            {error}
          </div>
        )}
        
        <div className={styles.otpContainer} onPaste={handlePaste}>
          {otp.map((digit, index) => (
            <input
              key={index}
              ref={el => inputRefs.current[index] = el}
              type="text"
              inputMode="numeric"
              maxLength={1}
              value={digit}
              onChange={(e) => handleChange(index, e.target.value)}
              onKeyDown={(e) => handleKeyDown(index, e)}
              className={styles.otpInput}
              aria-label={`Digit ${index + 1}`}
              disabled={loading}
            />
          ))}
        </div>
        
        <Button
          variant="primary"
          size="xlarge"
          fullWidth
          onClick={handleVerify}
          loading={loading}
          className={styles.verifyButton}
        >
          VERIFY
        </Button>
        
        <div className={styles.resendContainer}>
          {resendCooldown > 0 ? (
            <span className={styles.cooldown}>
              Resend available in {resendCooldown} seconds
            </span>
          ) : (
            <button
              className={styles.resendButton}
              onClick={handleResend}
              disabled={loading}
            >
              Resend Code
            </button>
          )}
        </div>
      </Card>
    </div>
  );
};

export default OTPVerificationPage;