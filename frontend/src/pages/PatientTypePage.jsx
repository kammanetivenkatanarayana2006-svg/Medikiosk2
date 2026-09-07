import React from 'react';
import PatientTypeSelection from '../components/onboarding/PatientTypeSelection';
import OnboardingProgress from '../components/onboarding/OnboardingProgress';
import styles from './PatientTypePage.module.css';

const PatientTypePage = () => {
  return (
    <div className={styles.page}>
      <div className={styles.progress}>
        <OnboardingProgress currentStep={1} totalSteps={3} />
      </div>
      <PatientTypeSelection />
    </div>
  );
};

export default PatientTypePage;