import React from 'react';
import styles from './Badge.module.css';

const Badge = ({ 
  children, 
  variant = 'default',
  size = 'medium',
  className = '',
  ...props 
}) => {
  const classes = [
    styles.badge,
    styles[`variant_${variant}`],
    styles[`size_${size}`],
    className,
  ].filter(Boolean).join(' ');

  return (
    <span className={classes} {...props}>
      {children}
    </span>
  );
};

export default Badge;