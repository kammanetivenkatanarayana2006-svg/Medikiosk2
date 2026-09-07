import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../ui/Button';
import styles from './WelcomeActions.module.css';

const WelcomeActions = ({ 
  showStart = true,
  onStart = null,
  className = '',
  ...props 
}) => {
  const navigate = useNavigate();
  
  const handleStart = () => {
    if (onStart) {
      onStart();
    } else {
      // navigate('/onboarding');
      navigate('/patient-type');
    }
  };
  
  if (!showStart) return null;
  
  return (
    <div className={`${styles.actions} ${className}`} {...props}>
      <Button
        variant="primary"
        size="xlarge"
        onClick={handleStart}
        aria-label="Start your consultation"
        className={styles.startButton}
      >
        START YOUR CONSULTATION
      </Button>
      <p className={styles.hint}>
        Quick, private, and doctor-guided
      </p>
    </div>
  );
};

export default WelcomeActions;