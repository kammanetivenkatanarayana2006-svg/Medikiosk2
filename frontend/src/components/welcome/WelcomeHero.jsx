import React from 'react';
import styles from './WelcomeHero.module.css';

const WelcomeHero = ({ 
  step = 0,
  reducedMotion = false,
  className = '',
  ...props 
}) => {
  const messages = [
    {
      title: 'WELCOME TO',
      highlight: 'MEDIKIOSK',
      subtitle: null,
    },
    {
      title: 'Your AI-powered clinical intake assistant',
      highlight: null,
      subtitle: 'A smarter way to share your health history with your doctor.',
    },
  ];
  
  const currentMessage = messages[step] || messages[0];
  
  return (
    <div 
      className={`${styles.hero} ${!reducedMotion ? styles.animated : ''} ${className}`}
      {...props}
    >
      {currentMessage.title && (
        <h1 className={`${styles.title} text-h1`}>
          {currentMessage.title}
        </h1>
      )}
      {currentMessage.highlight && (
        <span className={`${styles.highlight} text-display`}>
          {currentMessage.highlight}
        </span>
      )}
      {currentMessage.subtitle && (
        <p className={`${styles.subtitle} text-body-lg`}>
          {currentMessage.subtitle}
        </p>
      )}
    </div>
  );
};

export default WelcomeHero;