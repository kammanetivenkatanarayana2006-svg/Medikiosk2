import React from 'react';
import styles from './AIOrb.module.css';

const AIOrb = ({ 
  active = true,
  reducedMotion = false,
  className = '',
  ...props 
}) => {
  return (
    <div 
      className={`${styles.orbContainer} ${active && !reducedMotion ? styles.active : ''} ${className}`}
      aria-hidden="true"
      {...props}
    >
      <div className={styles.orbOuter}>
        <div className={styles.orbMiddle}>
          <div className={styles.orbCore}>
            <div className={styles.orbPulse} />
          </div>
        </div>
      </div>
      <div className={styles.orbRing1} />
      <div className={styles.orbRing2} />
      <div className={styles.orbParticles}>
        {[...Array(8)].map((_, i) => (
          <div 
            key={i} 
            className={styles.particle}
            style={{ 
              transform: `rotate(${i * 45}deg) translateY(-60px)`,
              animationDelay: `${i * 0.15}s`
            }}
          />
        ))}
      </div>
    </div>
  );
};

export default AIOrb;