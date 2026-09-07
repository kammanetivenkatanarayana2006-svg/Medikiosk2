import React from 'react';
import styles from './Spinner.module.css';

const Spinner = ({ 
  size = 'medium',
  fullScreen = false,
  label = 'Loading...',
  className = '',
  ...props 
}) => {
  const classes = [
    styles.spinner,
    styles[`size_${size}`],
    fullScreen && styles.fullScreen,
    className,
  ].filter(Boolean).join(' ');
  
  return (
    <div className={classes} role="status" aria-label={label} {...props}>
      <div className={styles.spinnerCircle} />
      {label && <span className={styles.label}>{label}</span>}
    </div>
  );
};

export default Spinner;