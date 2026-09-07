import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';
import { useAuth } from '../contexts/AuthContext';
import { patientService } from '../services/patient';
import styles from './ProfileFinalConfirmation.module.css';

const ProfileFinalConfirmation = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadProfile();
  }, []);
  
  const loadProfile = async () => {
    const result = await patientService.getMyProfile();
    setLoading(false);
    if (result.success) {
      setProfile(result.patient);
    }
  };
  
  const handleConfirm = () => {
    // Navigate to next phase placeholder
    navigate('/patient/home');
  };
  
  if (loading) {
    return (
      <div className={styles.container}>
        <Card variant="glass" padding="xlarge" className={styles.card}>
          <p className={styles.loading}>Loading...</p>
        </Card>
      </div>
    );
  }
  
  return (
    <div className={styles.container}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <h1 className={`${styles.title} text-h1`}>
          Confirm Your Profile
        </h1>
        <p className={`${styles.subtitle} text-body-lg`}>
          Review your information and photo before continuing
        </p>
        
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
            
            <div className={styles.actions}>
              <Button
                variant="outline"
                size="large"
                onClick={() => navigate('/patient-profile')}
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
          </>
        )}
      </Card>
    </div>
  );
};

export default ProfileFinalConfirmation;