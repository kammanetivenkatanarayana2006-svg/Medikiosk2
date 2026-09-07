import React from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../ui/Card';
import Button from '../ui/Button';
import Badge from '../ui/Badge';
import styles from './InterviewPlaceholder.module.css';

const InterviewPlaceholder = ({ className = '', ...props }) => {
  const navigate = useNavigate();
  
  return (
    <div className={`${styles.container} ${className}`} {...props}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <div className={styles.icon}>🤖</div>
        <Badge variant="primary" size="large" className={styles.badge}>
          Coming in Phase 11
        </Badge>
        <h1 className={`${styles.title} text-h1`}>
          AI Clinical Interview
        </h1>
        <p className={`${styles.description} text-body-lg`}>
          The AI-assisted clinical interview will be available in the next phase.
          Your consultation setup is complete and ready.
        </p>
        <Button
          variant="outline"
          size="large"
          onClick={() => navigate('/patient/home')}
        >
          RETURN TO HOME
        </Button>
      </Card>
    </div>
  );
};

export default InterviewPlaceholder;