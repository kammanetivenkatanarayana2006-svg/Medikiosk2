import React from 'react';

export const Logo = ({ size = 'medium' }) => {
  return (
    <div className={`medikiosk-brand brand-${size}`}>
      <span className="brand-icon">🏥</span>
      <span className="brand-name">Medi<span className="brand-accent">Kiosk</span></span>
    </div>
  );
};