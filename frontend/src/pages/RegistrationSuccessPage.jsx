import React from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';
import styles from './RegistrationSuccessPage.module.css';

const RegistrationSuccessPage = () => {
  const navigate = useNavigate();
  
  return (
    <div className={styles.container}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <div className={styles.icon}>✅</div>
        <Badge variant="success" size="large" className={styles.badge}>
          Account Created
        </Badge>
        <h1 className={`${styles.title} text-h1`}>
          Your MediKiosk Account Has Been Created
        </h1>
        <p className={`${styles.description} text-body-lg`}>
          Phone verification and email verification will be added in a
          future phase. You can now login to your account.
        </p>
        <Button
          variant="primary"
          size="xlarge"
          fullWidth
          onClick={() => navigate('/login')}
        >
          CONTINUE TO LOGIN
        </Button>
      </Card>
    </div>
  );
};

export default RegistrationSuccessPage;