import React, { useState, useEffect, useCallback } from 'react';
import MediKioskLogo from './MediKioskLogo';
import WelcomeHero from './WelcomeHero';
import AIOrb from './AIOrb';
import HeartbeatWave from './HeartbeatWave';
import WelcomeActions from './WelcomeActions';
import SkipIntroButton from './SkipIntroButton';
import WelcomeBackground from './WelcomeBackground';
import styles from './CinematicSequence.module.css';

const CinematicSequence = ({ 
  reducedMotion = false,
  onComplete = null,
  className = '',
  ...props 
}) => {
  const [step, setStep] = useState(0);
  const [showStart, setShowStart] = useState(false);
  const [skipped, setSkipped] = useState(false);
  
  const totalSteps = 2;
  
  const completeIntro = useCallback(() => {
    setSkipped(true);
    setStep(totalSteps - 1);
    setShowStart(true);
    if (onComplete) onComplete();
  }, [onComplete]);
  
  useEffect(() => {
    if (skipped) return;
    
    const timeouts = [];
    
    if (!reducedMotion) {
      timeouts.push(setTimeout(() => setStep(0), 100));
      timeouts.push(setTimeout(() => setStep(1), 3000));
      timeouts.push(setTimeout(() => setShowStart(true), 6000));
      timeouts.push(setTimeout(() => {
        if (onComplete) onComplete();
      }, 8000));
    } else {
      setStep(1);
      setShowStart(true);
      if (onComplete) onComplete();
    }
    
    return () => {
      timeouts.forEach(clearTimeout);
    };
  }, [reducedMotion, skipped, onComplete]);
  
  const handleSkip = () => {
    completeIntro();
  };
  
  return (
    <div className={`${styles.cinematic} ${className}`} {...props}>
      <WelcomeBackground reducedMotion={reducedMotion} />
      
      <SkipIntroButton 
        onSkip={handleSkip}
        visible={!skipped && !showStart}
        className={styles.skipButton}
      />
      
      <div className={styles.content}>
        <MediKioskLogo 
          reducedMotion={reducedMotion}
          className={styles.logo}
        />
        
        <WelcomeHero 
          step={step}
          reducedMotion={reducedMotion}
          className={styles.hero}
        />
        
        <div className={styles.visualElements}>
          <AIOrb 
            reducedMotion={reducedMotion}
            className={styles.orb}
          />
          <HeartbeatWave 
            reducedMotion={reducedMotion}
            className={styles.waveform}
          />
        </div>
        
        <WelcomeActions 
          showStart={showStart}
          className={styles.actions}
        />
      </div>
    </div>
  );
};

export default CinematicSequence;