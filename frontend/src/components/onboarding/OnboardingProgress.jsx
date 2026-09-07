import React from 'react';
import styles from './OnboardingProgress.module.css';

const OnboardingProgress = ({ 
  currentStep = 1, 
  totalSteps = 3,
  className = '',
  ...props 
}) => {
  const steps = [
    { number: 1, label: 'Patient Type' },
    { number: 2, label: 'Your Details' },
    { number: 3, label: 'Confirm' },
  ];
  
  return (
    <div className={`${styles.progress} ${className}`} {...props}>
      {steps.map((step, index) => (
        <React.Fragment key={step.number}>
          <div className={styles.step}>
            <div 
              className={`${styles.circle} ${
                step.number < currentStep ? styles.completed :
                step.number === currentStep ? styles.active : ''
              }`}
              aria-current={step.number === currentStep ? 'step' : undefined}
            >
              {step.number < currentStep ? '✓' : step.number}
            </div>
            <span 
              className={`${styles.label} ${
                step.number === currentStep ? styles.activeLabel : ''
              }`}
            >
              {step.label}
            </span>
          </div>
          {index < steps.length - 1 && (
            <div 
              className={`${styles.line} ${
                step.number < currentStep ? styles.lineCompleted : ''
              }`}
            />
          )}
        </React.Fragment>
      ))}
    </div>
  );
};

export default OnboardingProgress;