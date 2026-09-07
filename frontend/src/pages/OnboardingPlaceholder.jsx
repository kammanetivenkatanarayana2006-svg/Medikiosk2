import React from 'react';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';
import Button from '../components/ui/Button';
import styles from './OnboardingPlaceholder.module.css';

const OnboardingPlaceholder = () => {
  return (
    <div className={styles.container}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <div className={styles.icon}>👤</div>
        <Badge variant="primary" size="large" className={styles.badge}>
          Coming Soon
        </Badge>
        <h1 className={`${styles.title} text-h1`}>
          Patient Onboarding
        </h1>
        <p className={`${styles.description} text-body-lg`}>
          The patient onboarding experience will be available in the next phase.
          This will include language selection, patient profile setup, and
          consultation initiation.
        </p>
        <div className={styles.features}>
          <div className={styles.feature}>
            <span className={styles.featureIcon}>🌐</span>
            <span className={styles.featureText}>Multilingual Support</span>
          </div>
          <div className={styles.feature}>
            <span className={styles.featureIcon}>📋</span>
            <span className={styles.featureText}>Patient Profile</span>
          </div>
          <div className={styles.feature}>
            <span className={styles.featureIcon}>🤖</span>
            <span className={styles.featureText}>AI-Assisted Intake</span>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default OnboardingPlaceholder;