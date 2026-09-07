import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../ui/Card';
import Button from '../ui/Button';
import { useConsultation } from '../../contexts/ConsultationContext';
import styles from './ConsentStep.module.css';

const ConsentStep = ({ className = '', ...props }) => {
  const navigate = useNavigate();
  const { consultationSetup, setConsent } = useConsultation();
  const [consentChecked, setConsentChecked] = useState(consultationSetup.consent_given);
  
  const handleConsentChange = (e) => {
    const checked = e.target.checked;
    setConsentChecked(checked);
    setConsent(checked);
  };
  
  const handleContinue = () => {
    if (consentChecked) {
      navigate('/consultation/ready');
    }
  };
  
  return (
    <div className={`${styles.container} ${className}`} {...props}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <h1 className={`${styles.title} text-h1`}>
          Patient Consent
        </h1>
        <p className={`${styles.subtitle} text-body-lg`}>
          Please review and provide consent before continuing
        </p>
        
        <div className={styles.consentContent}>
          <p className={styles.consentText}>
            Your responses will be used to prepare your clinical history for
            review by a healthcare professional.
          </p>
          <p className={styles.consentText}>
            Some information may be processed using AI-assisted tools to
            organize and summarize the information you provide.
          </p>
          <p className={styles.consentText}>
            AI assistance does not replace a doctor. A healthcare professional
            must review and verify the information before it is finalized.
          </p>
        </div>
        
        <div className={styles.disclaimer}>
          <span className={styles.disclaimerIcon}>ℹ️</span>
          <p className={styles.disclaimerText}>
            AI-assisted documentation only. MediKiosk does not independently
            diagnose medical conditions or prescribe treatment.
          </p>
        </div>
        
        <div className={styles.consentCheck}>
          <label className={styles.consentLabel}>
            <input
              type="checkbox"
              checked={consentChecked}
              onChange={handleConsentChange}
              className={styles.checkbox}
            />
            <span className={styles.consentText}>
              I understand and consent to continue.
            </span>
          </label>
        </div>
        
        <div className={styles.actions}>
          <Button
            variant="outline"
            size="large"
            onClick={() => navigate('/consultation/type')}
          >
            BACK
          </Button>
          <Button
            variant="primary"
            size="large"
            onClick={handleContinue}
            disabled={!consentChecked}
          >
            CONTINUE
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default ConsentStep;