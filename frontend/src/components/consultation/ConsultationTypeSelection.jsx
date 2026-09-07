import React from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../ui/Card';
import Button from '../ui/Button';
import { useConsultation } from '../../contexts/ConsultationContext';
import styles from './ConsultationTypeSelection.module.css';

const CONSULTATION_TYPES = [
  {
    code: 'general',
    name: 'General Clinical Consultation',
    description: 'General health consultation with a healthcare professional',
    icon: '🏥',
  },
  {
    code: 'ayurveda',
    name: 'Ayurveda / AYUSH Consultation',
    description: 'Traditional Ayurvedic and AYUSH consultation',
    icon: '🌿',
  },
  {
    code: 'follow_up',
    name: 'Follow-up Consultation',
    description: 'Follow-up visit for ongoing care',
    icon: '🔁',
  },
];

const ConsultationTypeSelection = ({ className = '', ...props }) => {
  const navigate = useNavigate();
  const { consultationSetup, setConsultationType } = useConsultation();
  
  const handleTypeSelect = (code) => {
    setConsultationType(code);
  };
  
  const handleContinue = () => {
    if (consultationSetup.consultation_type) {
      navigate('/consultation/consent');
    }
  };
  
  return (
    <div className={`${styles.container} ${className}`} {...props}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <h1 className={`${styles.title} text-h1`}>
          Select Consultation Type
        </h1>
        <p className={`${styles.subtitle} text-body-lg`}>
          Choose the type of consultation you need
        </p>
        
        <div className={styles.typeList}>
          {CONSULTATION_TYPES.map((type) => (
            <button
              key={type.code}
              className={`${styles.typeCard} ${
                consultationSetup.consultation_type === type.code ? styles.selected : ''
              }`}
              onClick={() => handleTypeSelect(type.code)}
              role="radio"
              aria-checked={consultationSetup.consultation_type === type.code}
            >
              <span className={styles.typeIcon}>{type.icon}</span>
              <div className={styles.typeInfo}>
                <span className={styles.typeName}>{type.name}</span>
                <span className={styles.typeDescription}>{type.description}</span>
              </div>
              {consultationSetup.consultation_type === type.code && (
                <span className={styles.selectedIndicator}>✓</span>
              )}
            </button>
          ))}
        </div>
        
        <div className={styles.actions}>
          <Button
            variant="outline"
            size="large"
            onClick={() => navigate('/consultation/language')}
          >
            BACK
          </Button>
          <Button
            variant="primary"
            size="large"
            onClick={handleContinue}
            disabled={!consultationSetup.consultation_type}
          >
            CONTINUE
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default ConsultationTypeSelection;