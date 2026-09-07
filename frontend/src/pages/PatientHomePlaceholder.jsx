import React from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';
import { useAuth } from '../contexts/AuthContext';
import styles from './PatientHomePlaceholder.module.css';

const PatientHomePlaceholder = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  
  const handleLogout = () => {
    logout();
    navigate('/login');
  };
  
  return (
    <div className={styles.container}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <div className={styles.icon}>🏥</div>
        <Badge variant="success" size="large" className={styles.badge}>
          Authenticated
        </Badge>
        <h1 className={`${styles.title} text-h1`}>
          Welcome, {user?.full_name}
        </h1>
        <p className={`${styles.description} text-body-lg`}>
          Authenticated successfully. Patient workspace will be available
          in the next phase.
        </p>
        <div className={styles.info}>
          <p className={styles.infoText}>
            Your secure session is active. Future phases will provide:
          </p>
          <ul className={styles.features}>
            <li>Language selection</li>
            <li>Consent management</li>
            <li>AI clinical interview</li>
          </ul>
        </div>
        <Button
          variant="outline"
          size="large"
          onClick={handleLogout}
        >
          LOGOUT
        </Button>
      </Card>
    </div>
  );
};

export default PatientHomePlaceholder;