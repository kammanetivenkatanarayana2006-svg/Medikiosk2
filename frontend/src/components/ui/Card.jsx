import React from 'react';
import styles from './Card.module.css';

const Card = React.forwardRef(function Card(
  { 
    children,
    variant = 'default',
    padding = 'medium',
    hoverable = false,
    className = '',
    ...props 
  },
  ref
) {
  const classes = [
    styles.card,
    styles[`variant_${variant}`],
    styles[`padding_${padding}`],
    hoverable && styles.hoverable,
    className,
  ].filter(Boolean).join(' ');

  return (
    <div ref={ref} className={classes} {...props}>
      {children}
    </div>
  );
});

export default Card;