import React from 'react';
import styles from './Input.module.css';

const Input = React.forwardRef(function Input(
  { 
    label,
    error,
    hint,
    size = 'medium',
    fullWidth = true,
    className = '',
    id,
    ...props 
  },
  ref
) {
  const inputId = id || `input-${Math.random().toString(36).slice(2)}`;
  
  const classes = [
    styles.input,
    styles[`size_${size}`],
    fullWidth && styles.fullWidth,
    error && styles.error,
    className,
  ].filter(Boolean).join(' ');

  return (
    <div className={styles.wrapper}>
      {label && (
        <label htmlFor={inputId} className={styles.label}>
          {label}
        </label>
      )}
      <input
        ref={ref}
        id={inputId}
        className={classes}
        aria-invalid={!!error}
        aria-describedby={error ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined}
        {...props}
      />
      {error && (
        <span id={`${inputId}-error`} className={styles.errorText}>
          {error}
        </span>
      )}
      {hint && !error && (
        <span id={`${inputId}-hint`} className={styles.hint}>
          {hint}
        </span>
      )}
    </div>
  );
});

export default Input;