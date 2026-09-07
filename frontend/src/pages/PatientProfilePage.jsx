import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';
import { useAuth } from '../contexts/AuthContext';
import { patientService } from '../services/patient';
import styles from './PatientProfilePage.module.css';

const PatientProfilePage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    loadProfile();
  }, []);
  
  const loadProfile = async () => {
    setLoading(true);
    setError(null);
    
    const result = await patientService.getMyProfile();
    
    setLoading(false);
    
    if (result.success) {
      setProfile(result.patient);
    } else {
      setError(result.error);
    }
  };
  
  const handleContinue = () => {
    navigate('/photo-consent');
  };
  
  if (loading) {
    return (
      <div className={styles.container}>
        <Card variant="glass" padding="xlarge" className={styles.card}>
          <p className={styles.loading}>Loading profile...</p>
        </Card>
      </div>
    );
  }
  
  return (
    <div className={styles.container}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <h1 className={`${styles.title} text-h1`}>
          Your Patient Profile
        </h1>
        <p className={`${styles.subtitle} text-body-lg`}>
          Review your information before continuing
        </p>
        
        {error && (
          <div className={styles.error} role="alert">
            {error}
          </div>
        )}
        
        {profile && (
          <>
            <div className={styles.details}>
              <div className={styles.detailItem}>
                <span className={styles.detailLabel}>Full Name</span>
                <span className={styles.detailValue}>{profile.full_name}</span>
              </div>
              
              <div className={styles.detailItem}>
                <span className={styles.detailLabel}>Email</span>
                <span className={styles.detailValue}>{profile.email}</span>
              </div>
              
              <div className={styles.detailItem}>
                <span className={styles.detailLabel}>Phone</span>
                <span className={styles.detailValue}>{profile.phone}</span>
              </div>
              
              <div className={styles.detailItem}>
                <span className={styles.detailLabel}>Gender</span>
                <span className={styles.detailValue}>{profile.gender}</span>
              </div>
              
              {profile.age && (
                <div className={styles.detailItem}>
                  <span className={styles.detailLabel}>Age</span>
                  <span className={styles.detailValue}>{profile.age}</span>
                </div>
              )}
              
              <div className={styles.detailItem}>
                <span className={styles.detailLabel}>Photo</span>
                <span className={styles.detailValue}>
                  {profile.has_photo ? (
                    <Badge variant="success">Added</Badge>
                  ) : (
                    <Badge variant="warning">Not added</Badge>
                  )}
                </span>
              </div>
            </div>
            
            <Button
              variant="primary"
              size="xlarge"
              fullWidth
              onClick={handleContinue}
              className={styles.continueButton}
            >
              CONTINUE TO PHOTO
            </Button>
          </>
        )}
      </Card>
    </div>
  );
};

export default PatientProfilePage;