import React from 'react';
import { useThemeContext } from '../contexts/ThemeContext';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';
import Input from '../components/ui/Input';
import ProgressIndicator from '../components/ui/ProgressIndicator';
import styles from './FoundationScreen.module.css';

function FoundationScreen() {
  const { theme, toggleTheme, isDark } = useThemeContext();

  return (
    <div className={styles.container}>
      <div className={styles.themeToggle}>
        <Button 
          variant="ghost" 
          size="small"
          onClick={toggleTheme}
          aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}
        >
          {isDark ? '☀️ Light' : '🌙 Dark'}
        </Button>
      </div>

      <Card variant="glass" padding="xlarge" className={styles.mainCard}>
        <div className={styles.logo}>🏥</div>
        <h1 className={`text-display ${styles.title}`}>MediKiosk</h1>
        <p className={`text-body-lg ${styles.subtitle}`}>
          AI-Powered Clinical Intake & Clinical History Platform
        </p>
        <Badge variant="primary" size="large" className={styles.phaseBadge}>
          Phase 4 — Frontend Design System
        </Badge>
      </Card>

      <div className={styles.componentsGrid}>
        <Card variant="default" padding="large" hoverable>
          <h3 className={`text-h3 ${styles.cardTitle}`}>Buttons</h3>
          <div className={styles.componentRow}>
            <Button variant="primary">Primary</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="outline">Outline</Button>
            <Button variant="ghost">Ghost</Button>
          </div>
        </Card>

        <Card variant="default" padding="large" hoverable>
          <h3 className={`text-h3 ${styles.cardTitle}`}>Badges</h3>
          <div className={styles.componentRow}>
            <Badge variant="success">Success</Badge>
            <Badge variant="warning">Warning</Badge>
            <Badge variant="danger">Critical</Badge>
            <Badge variant="primary">AI Assisted</Badge>
          </div>
        </Card>

        <Card variant="default" padding="large" hoverable>
          <h3 className={`text-h3 ${styles.cardTitle}`}>Input</h3>
          <Input 
            label="Patient Name"
            placeholder="Enter patient name"
            hint="This is a demo input"
          />
        </Card>

        <Card variant="default" padding="large" hoverable>
          <h3 className={`text-h3 ${styles.cardTitle}`}>Progress</h3>
          <ProgressIndicator 
            value={65} 
            showValue
            label="Loading Progress"
          />
        </Card>
      </div>
    </div>
  );
}

export default FoundationScreen;