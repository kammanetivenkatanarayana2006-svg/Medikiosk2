import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import { useAuth } from '../contexts/AuthContext';
import styles from './RegisterPage.module.css';

const RegisterPage = () => {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone: '',
    password: '',
    confirm_password: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState(null);
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === 'phone') {
      setFormData(prev => ({ ...prev, [name]: value.replace(/\D/g, '').slice(0, 10) }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
    setErrors(prev => ({ ...prev, [name]: undefined }));
    setApiError(null);
  };
  
  const validate = () => {
    const newErrors = {};
    
    if (!formData.full_name.trim()) {
      newErrors.full_name = 'Please enter your full name.';
    }
    
    if (!formData.email.trim()) {
      newErrors.email = 'Please enter your email address.';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address.';
    }
    
    if (!formData.phone) {
      newErrors.phone = 'Please enter your mobile number.';
    } else if (!/^\d{10}$/.test(formData.phone)) {
      newErrors.phone = 'Enter a valid 10-digit mobile number.';
    }
    
    if (!formData.password) {
      newErrors.password = 'Please enter a password.';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters.';
    } else if (!/[A-Z]/.test(formData.password)) {
      newErrors.password = 'Password must contain an uppercase letter.';
    } else if (!/[a-z]/.test(formData.password)) {
      newErrors.password = 'Password must contain a lowercase letter.';
    } else if (!/\d/.test(formData.password)) {
      newErrors.password = 'Password must contain a number.';
    } else if (!/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(formData.password)) {
      newErrors.password = 'Password must contain a special character.';
    }
    
    if (formData.confirm_password !== formData.password) {
      newErrors.confirm_password = 'Passwords do not match.';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validate()) return;
    
    setLoading(true);
    setApiError(null);
    
    const result = await register({
      full_name: formData.full_name,
      email: formData.email,
      phone: formData.phone,
      password: formData.password,
    });
    
    setLoading(false);
    
    if (result.success) {
      navigate('/registration-success');
    } else {
      setApiError(result.error);
    }
  };
  
  return (
    <div className={styles.container}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <h1 className={`${styles.title} text-h1`}>
          Create Your MediKiosk Account
        </h1>
        <p className={`${styles.subtitle} text-body-lg`}>
          Register securely to continue your clinical journey
        </p>
        
        {apiError && (
          <div className={styles.apiError} role="alert">
            {apiError}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className={styles.form}>
          <Input
            label="Full Name"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
            error={errors.full_name}
            placeholder="Enter your full name"
            size="large"
            required
          />
          
          <Input
            label="Email Address"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            error={errors.email}
            placeholder="Enter your email address"
            size="large"
            required
          />
          
          <Input
            label="Mobile Number"
            name="phone"
            type="tel"
            value={formData.phone}
            onChange={handleChange}
            error={errors.phone}
            placeholder="10-digit mobile number"
            size="large"
            required
          />
          
          <Input
            label="Password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            error={errors.password}
            placeholder="Create a strong password"
            size="large"
            hint="Use uppercase, lowercase, number, and special character"
            required
          />
          
          <Input
            label="Confirm Password"
            name="confirm_password"
            type="password"
            value={formData.confirm_password}
            onChange={handleChange}
            error={errors.confirm_password}
            placeholder="Re-enter your password"
            size="large"
            required
          />
          
          <Button
            type="submit"
            variant="primary"
            size="xlarge"
            fullWidth
            loading={loading}
          >
            CREATE ACCOUNT
          </Button>
        </form>
        
        <p className={styles.loginLink}>
          Already have an account?{' '}
          <button
            className={styles.link}
            onClick={() => navigate('/login')}
          >
            Login
          </button>
        </p>
      </Card>
    </div>
  );
};

export default RegisterPage;