import React from 'react';
import styles from './ProgressIndicator.module.css';

const ProgressIndicator = ({ 
  value = 0, 
  max = 100,
  variant = 'bar',
  size = 'medium',
  label = null,
  showValue = false,
  className = '',
  ...props 
}) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);
  
  const classes = [
    styles.indicator,
    styles[`variant_${variant}`],
    styles[`size_${size}`],
    className,
  ].filter(Boolean).join(' ');

  return (
    <div className={styles.wrapper}>
      {label && <span className={styles.label}>{label}</span>}
      <div 
        className={classes}
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
        {...props}
      >
        {variant === 'bar' && (
          <div 
            className={styles.bar}
            style={{ width: `${percentage}%` }}
          />
        )}
        {variant === 'circular' && (
          <svg className={styles.circular} viewBox="0 0 36 36">
            <path
              className={styles.circularBg}
              d="M18 2.0845
                a 15.9155 15.9155 0 0 1 0 31.831
                a 15.9155 15.9155 0 0 1 0 -31.831"
            />
            <path
              className={styles.circularFg}
              d="M18 2.0845
                a 15.9155 15.9155 0 0 1 0 31.831
                a 15.9155 15.9155 0 0 1 0 -31.831"
              strokeDasharray={`${percentage}, 100`}
            />
          </svg>
        )}
      </div>
      {showValue && (
        <span className={styles.value}>{Math.round(percentage)}%</span>
      )}
    </div>
  );
};

export default ProgressIndicator;