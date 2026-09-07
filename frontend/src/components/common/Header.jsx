import React from 'react';
import StatusBadge from './StatusBadge';

export default function Header({ apiStatus }) {
  return (
    <header className="header-container" style={{
      display: 'flex',
      justify: 'space-between',
      alignItems: 'center',
      padding: '1.25rem 2rem',
      width: '100%',
      position: 'relative',
      zIndex: 10
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <div style={{
          width: '32px',
          height: '32px',
          borderRadius: '8px',
          background: 'linear-gradient(135deg, #0EA5E9, #2563EB)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontWeight: 'bold',
          color: '#FFF',
          boxShadow: '0 0 12px rgba(14, 165, 233, 0.5)'
        }}>
          MK
        </div>
        <span style={{ fontWeight: 700, fontSize: '1.25rem', letterSpacing: '0.05em' }}>
          MEDI<span style={{ color: 'var(--cyan-bright)' }}>KIOSK</span>
        </span>
      </div>

      <StatusBadge status={apiStatus} />
    </header>
  );
}