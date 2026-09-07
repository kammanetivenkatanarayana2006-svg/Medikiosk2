import React from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../ui/Card';
import Button from '../ui/Button';
import Badge from '../ui/Badge';
import styles from './OnboardingComplete.module.css';

const OnboardingComplete = ({ className = '', ...props }) => {
  const navigate = useNavigate();
  
  return (
    <div className={`${styles.container} ${className}`} {...props}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <div className={styles.icon}>✅</div>
        <Badge variant="success" size="large" className={styles.badge}>
          Profile Ready
        </Badge>
        <h1 className={`${styles.title} text-h1`}>
          You're All Set!
        </h1>
        <p className={`${styles.description} text-body-lg`}>
          Your profile has been prepared. The next phase will guide you
          through the clinical intake process with language selection
          and consent.
        </p>
        <div className={styles.info}>
          <p className={styles.infoText}>
            Phase 7 will implement:
          </p>
          <ul className={styles.features}>
            <li>Language selection</li>
            <li>Consent management</li>
            <li>Consultation initiation</li>
          </ul>
        </div>
        <Button
          variant="primary"
          size="large"
          onClick={() => navigate('/')}
        >
          RETURN TO HOME
        </Button>
      </Card>
    </div>
  );
};

export default OnboardingComplete;