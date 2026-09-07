import React from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../ui/Card';
import Button from '../ui/Button';
import styles from './PatientTypeSelection.module.css';

const PatientTypeSelection = ({ className = '', ...props }) => {
  const navigate = useNavigate();

  const handleNewPatient = () => {
    console.log('New Patient clicked');
    navigate('/onboarding');
  };

  const handleReturningPatient = () => {
    console.log('Returning Patient clicked');
    navigate('/returning-patient');
  };

  return (
    <div className={`${styles.container} ${className}`} {...props}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <h1 className={`${styles.title} text-h1`}>
          Welcome to MediKiosk
        </h1>

        <p className={`${styles.subtitle} text-body-lg`}>
          Are you a new or returning patient?
        </p>

        <div className={styles.options}>

          {/* New Patient */}
          <Card
            variant="default"
            padding="large"
            hoverable
            className={styles.patientCard}
          >
            <div className={styles.icon}>👤</div>

            <h2 className={`${styles.cardTitle} text-h2`}>
              NEW PATIENT
            </h2>

            <p className={`${styles.cardDescription} text-body-sm`}>
              Start your first consultation
            </p>

            <Button
              variant="primary"
              size="large"
              onClick={handleNewPatient}
            >
              START AS NEW PATIENT
            </Button>
          </Card>

          {/* Returning Patient */}
          <Card
            variant="default"
            padding="large"
            hoverable
            className={styles.patientCard}
          >
            <div className={styles.icon}>🔄</div>

            <h2 className={`${styles.cardTitle} text-h2`}>
              RETURNING PATIENT
            </h2>

            <p className={`${styles.cardDescription} text-body-sm`}>
              Access your existing records
            </p>

            <Button
              variant="outline"
              size="large"
              onClick={handleReturningPatient}
            >
              RETURNING PATIENT
            </Button>
          </Card>

        </div>
      </Card>
    </div>
  );
};

export default PatientTypeSelection;
