/**
 * Validation utilities for patient onboarding
 */

export const validateFullName = (value) => {
  const trimmed = value.trim();
  if (!trimmed) {
    return 'Please enter your full name.';
  }
  if (trimmed.length < 2) {
    return 'Name must be at least 2 characters.';
  }
  if (trimmed.length > 100) {
    return 'Name must be less than 100 characters.';
  }
  return null;
};

export const validateEmail = (value) => {
  const trimmed = value.trim();
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!trimmed) {
    return 'Please enter your email address.';
  }
  if (!emailRegex.test(trimmed)) {
    return 'Please enter a valid email address.';
  }
  return null;
};

export const validatePhone = (value) => {
  const phoneRegex = /^\d{10}$/;
  if (!value) {
    return 'Please enter your mobile number.';
  }
  if (!phoneRegex.test(value)) {
    return 'Enter a valid 10-digit mobile number.';
  }
  return null;
};

export const validateGender = (value) => {
  if (!value) {
    return 'Please select your gender.';
  }
  return null;
};

export const validateAge = (value) => {
  if (!value) {
    return null; // Optional field
  }
  const ageNum = parseInt(value, 10);
  if (isNaN(ageNum) || ageNum < 0 || ageNum > 150) {
    return 'Please enter a valid age.';
  }
  return null;
};

export const validatePatientData = (data) => {
  return {
    full_name: validateFullName(data.full_name || ''),
    email: validateEmail(data.email || ''),
    phone: validatePhone(data.phone || ''),
    gender: validateGender(data.gender || ''),
    age: validateAge(data.age || ''),
  };
};