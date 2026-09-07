import React from 'react';
import styles from './SkipIntroButton.module.css';

const SkipIntroButton = ({ 
  onSkip,
  visible = true,
  className = '',
  ...props 
}) => {
  if (!visible) return null;
  
  return (
    <button
      className={`${styles.skipButton} ${className}`}
      onClick={onSkip}
      aria-label="Skip intro animation"
      {...props}
    >
      Skip Intro
      <span className={styles.skipIcon} aria-hidden="true">
        →
      </span>
    </button>
  );
};

export default SkipIntroButton;