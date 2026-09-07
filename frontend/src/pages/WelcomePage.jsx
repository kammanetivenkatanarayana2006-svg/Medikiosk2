import React from 'react';
import { useNavigate } from 'react-router-dom';
import CinematicSequence from '../components/welcome/CinematicSequence';
import { useThemeContext } from '../contexts/ThemeContext';
import styles from './WelcomePage.module.css';

const WelcomePage = () => {
  const navigate = useNavigate();
  const { theme } = useThemeContext();
  
  const handleIntroComplete = () => {
    // Intro completed - user can now see the start button
    console.log('Intro completed');
  };
  
  return (
    <div className={styles.page}>
      <CinematicSequence 
        onComplete={handleIntroComplete}
      />
    </div>
  );
};

export default WelcomePage;