import React from 'react';
import styles from './MediKioskLogo.module.css';

const MediKioskLogo = ({ 
  animated = true,
  reducedMotion = false,
  className = '',
  ...props 
}) => {
  return (
    <div 
      className={`${styles.logoWrapper} ${animated && !reducedMotion ? styles.animated : ''} ${className}`}
      {...props}
    >
      <div className={styles.logoMark} aria-hidden="true">
        <svg 
          width="80" 
          height="80" 
          viewBox="0 0 80 80" 
          fill="none" 
          xmlns="http://www.w3.org/2000/svg"
          className={styles.logoSvg}
        >
          <circle cx="40" cy="40" r="36" className={styles.logoCircle} />
          <path 
            d="M24 40C24 30 28 24 34 24C40 24 42 32 40 36C38 40 36 48 40 52C44 56 50 54 52 48C54 42 50 38 46 36" 
            className={styles.logoPath}
            strokeWidth="2.5"
            strokeLinecap="round"
          />
          <circle cx="40" cy="40" r="4" className={styles.logoDot} />
        </svg>
      </div>
      <div className={styles.logoText}>
        <span className={styles.logoName}>MediKiosk</span>
        <span className={styles.logoSubtext}>Clinical Intelligence</span>
      </div>
    </div>
  );
};

export default MediKioskLogo;