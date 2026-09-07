import React from 'react';
import PatientIdentityForm from '../components/onboarding/PatientIdentityForm';
import OnboardingProgress from '../components/onboarding/OnboardingProgress';
import styles from './PatientOnboardingPage.module.css';

const PatientOnboardingPage = () => {
  return (
    <div className={styles.page}>
      <div className={styles.progress}>
        <OnboardingProgress currentStep={2} totalSteps={3} />
      </div>
      <PatientIdentityForm />
    </div>
  );
};

export default PatientOnboardingPage;