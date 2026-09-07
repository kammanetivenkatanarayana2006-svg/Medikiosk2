import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function PlaceholderNextPhase() {
  const navigate = useNavigate();

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: 'calc(100vh - 120px)',
      padding: '2rem',
      textAlign: 'center',
      zIndex: 1,
      position: 'relative'
    }}>
      <div className="glass-panel" style={{
        maxWidth: '520px',
        width: '100%',
        padding: '2.5rem',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '1.25rem'
      }}>
        <div style={{
          width: '56px',
          height: '56px',
          borderRadius: '50%',
          background: 'rgba(56, 189, 248, 0.1)',
          border: '1px solid var(--cyan-bright)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'var(--cyan-bright)',
          fontSize: '1.5rem',
          fontWeight: 'bold'
        }}>
          P2
        </div>

        <h2 style={{ color: 'var(--text-main)', fontSize: '1.5rem' }}>Next Phase Horizon</h2>
        <p style={{ color: 'var(--text-muted)', lineHeight: '1.5', fontSize: '0.95rem' }}>
          This workflow step belongs to <strong>Phase 2+</strong> (Language Selection & Patient Registration).
          Phase 1 establishes the complete visual, architectural, and server baseline.
        </p>

        <button
          onClick={() => navigate('/')}
          style={{
            marginTop: '1rem',
            padding: '0.75rem 1.75rem',
            fontSize: '0.95rem',
            fontWeight: '600',
            color: 'var(--cyan-bright)',
            background: 'transparent',
            border: '1px solid var(--border-glass-bright)',
            borderRadius: '8px',
            cursor: 'pointer'
          }}
        >
          ← Return to Welcome
        </button>
      </div>
    </div>
  );
}