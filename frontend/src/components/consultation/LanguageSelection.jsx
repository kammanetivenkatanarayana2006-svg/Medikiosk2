import React from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../ui/Card';
import Button from '../ui/Button';
import { useConsultation } from '../../contexts/ConsultationContext';
import styles from './LanguageSelection.module.css';

const LANGUAGES = [
  { code: 'english', name: 'English', native: 'English' },
  { code: 'telugu', name: 'Telugu', native: 'తెలుగు' },
  { code: 'hindi', name: 'Hindi', native: 'हिन्दी' },
  { code: 'tamil', name: 'Tamil', native: 'தமிழ்' },
  { code: 'kannada', name: 'Kannada', native: 'ಕನ್ನಡ' },
  { code: 'malayalam', name: 'Malayalam', native: 'മലയാളം' },
  { code: 'marathi', name: 'Marathi', native: 'मराठी' },
  { code: 'bengali', name: 'Bengali', native: 'বাংলা' },
];

const LanguageSelection = ({ className = '', ...props }) => {
  const navigate = useNavigate();
  const { consultationSetup, setLanguage } = useConsultation();
  
  const handleLanguageSelect = (code) => {
    setLanguage(code);
  };
  
  const handleContinue = () => {
    if (consultationSetup.language) {
      navigate('/consultation/type');
    }
  };
  
  return (
    <div className={`${styles.container} ${className}`} {...props}>
      <Card variant="glass" padding="xlarge" className={styles.card}>
        <h1 className={`${styles.title} text-h1`}>
          Select Your Language
        </h1>
        <p className={`${styles.subtitle} text-body-lg`}>
          Choose the language for your consultation
        </p>
        
        <div className={styles.languageGrid}>
          {LANGUAGES.map((lang) => (
            <button
              key={lang.code}
              className={`${styles.languageCard} ${
                consultationSetup.language === lang.code ? styles.selected : ''
              }`}
              onClick={() => handleLanguageSelect(lang.code)}
              role="radio"
              aria-checked={consultationSetup.language === lang.code}
              aria-label={`${lang.name} - ${lang.native}`}
            >
              <span className={styles.languageName}>{lang.name}</span>
              <span className={styles.languageNative}>{lang.native}</span>
              {consultationSetup.language === lang.code && (
                <span className={styles.selectedIndicator}>✓</span>
              )}
            </button>
          ))}
        </div>
        
        <div className={styles.actions}>
          <Button
            variant="outline"
            size="large"
            onClick={() => navigate('/patient-profile')}
          >
            BACK
          </Button>
          <Button
            variant="primary"
            size="large"
            onClick={handleContinue}
            disabled={!consultationSetup.language}
          >
            CONTINUE
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default LanguageSelection;