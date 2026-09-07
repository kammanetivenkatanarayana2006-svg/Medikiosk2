import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import styles from './PhotoConsentPage.module.css';

const PhotoConsentPage = () => {
  const navigate = useNavigate();
  const [consented, setConsented] = useState(false);
  
  const handleContinue = () => {
    if (consented) {
      navigate('/photo-capture');
    }
  };
  
  return (
    <div className={styles.container}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <div className={styles.icon}>📸</div>
        <h1 className={`${styles.title} text-h1`}>
          Patient Photo
        </h1>
        <p className={`${styles.description} text-body-lg`}>
          Your photo will be used for identification and clinical documentation.
          It will not be used for diagnosis or any medical assessment.
        </p>
        
        <div className={styles.consentBox}>
          <label className={styles.consentLabel}>
            <input
              type="checkbox"
              checked={consented}
              onChange={(e) => setConsented(e.target.checked)}
              className={styles.checkbox}
            />
            <span className={styles.consentText}>
              I consent to capturing and storing my photo for MediKiosk
              identification and documentation.
            </span>
          </label>
        </div>
        
        <div className={styles.actions}>
          <Button
            variant="outline"
            size="large"
            onClick={() => navigate('/patient-profile')}
          >
            BACK
          </Button>
          <Button
            variant="primary"
            size="large"
            onClick={handleContinue}
            disabled={!consented}
          >
            CONTINUE
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default PhotoConsentPage;