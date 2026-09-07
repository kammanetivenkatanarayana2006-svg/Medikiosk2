import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../ui/Card';
import Button from '../ui/Button';
import Badge from '../ui/Badge';
import styles from './ProfileConfirmation.module.css';

const ProfileConfirmation = ({ className = '', ...props }) => {
  const navigate = useNavigate();
  const [patientData, setPatientData] = useState(null);
  
  useEffect(() => {
    const storedData = sessionStorage.getItem('medikiosk_onboarding');
    if (storedData) {
      setPatientData(JSON.parse(storedData));
    } else {
      // Redirect back if no data
      navigate('/onboarding');
    }
  }, [navigate]);
  
  if (!patientData) {
    return null;
  }
  
  const handleEdit = () => {
    navigate('/onboarding');
  };
  
  const handleConfirm = () => {
    // In Phase 6, just show success message
    // Future phases will handle actual account creation
    // navigate('/onboarding/complete');
    navigate("/onboarding-complete");
  };
  
  const handleBack = () => {
    navigate('/onboarding');
  };
  
  return (
    <div className={`${styles.container} ${className}`} {...props}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <h1 className={`${styles.title} text-h1`}>
          Please Confirm Your Details
        </h1>
        <p className={`${styles.subtitle} text-body-lg`}>
          Review your information before continuing
        </p>
        
        <div className={styles.details}>
          <div className={styles.detailItem}>
            <span className={styles.detailLabel}>Full Name</span>
            <span className={styles.detailValue}>{patientData.full_name}</span>
          </div>
          
          <div className={styles.detailItem}>
            <span className={styles.detailLabel}>Email</span>
            <span className={styles.detailValue}>{patientData.email}</span>
          </div>
          
          <div className={styles.detailItem}>
            <span className={styles.detailLabel}>Phone</span>
            <span className={styles.detailValue}>{patientData.phone}</span>
          </div>
          
          <div className={styles.detailItem}>
            <span className={styles.detailLabel}>Gender</span>
            <span className={styles.detailValue}>{patientData.gender}</span>
          </div>
          
          {patientData.age && (
            <div className={styles.detailItem}>
              <span className={styles.detailLabel}>Age</span>
              <span className={styles.detailValue}>{patientData.age}</span>
            </div>
          )}
        </div>
        
        <div className={styles.info}>
          <Badge variant="primary" size="medium">
            AI-Assisted Documentation
          </Badge>
          <p className={styles.infoText}>
            Your information helps MediKiosk prepare a personalized
            clinical intake experience. Doctor verification is required
            for all medical assessments.
          </p>
        </div>
        
        <div className={styles.actions}>
          <Button
            variant="outline"
            size="large"
            onClick={handleBack}
          >
            BACK
          </Button>
          <Button
            variant="outline"
            size="large"
            onClick={handleEdit}
          >
            EDIT
          </Button>
          <Button
            variant="primary"
            size="large"
            onClick={handleConfirm}
          >
            CONFIRM & CONTINUE
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default ProfileConfirmation;