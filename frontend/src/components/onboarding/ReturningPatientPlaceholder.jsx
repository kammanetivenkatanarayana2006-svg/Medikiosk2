import React from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../ui/Card';
import Button from '../ui/Button';
import Badge from '../ui/Badge';
import styles from './ReturningPatientPlaceholder.module.css';

const ReturningPatientPlaceholder = ({ className = '', ...props }) => {
  const navigate = useNavigate();
  
  return (
    <div className={`${styles.container} ${className}`} {...props}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <div className={styles.icon}>🔐</div>
        <Badge variant="primary" size="large" className={styles.badge}>
          Secure Login
        </Badge>
        <h1 className={`${styles.title} text-h1`}>
          Welcome Back
        </h1>
        <p className={`${styles.description} text-body-lg`}>
          Login to access your MediKiosk account and continue your
          clinical journey.
        </p>
        <div className={styles.actions}>
          <Button
            variant="primary"
            size="xlarge"
            onClick={() => navigate('/login')}
          >
            LOGIN
          </Button>
          <Button
            variant="outline"
            size="large"
            onClick={() => navigate('/patient-type')}
          >
            BACK
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default ReturningPatientPlaceholder;