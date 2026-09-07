import React from 'react';

export default function StatusBadge({ status }) {
  const isOk = status === 'ok';
  
  return (
    <div style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: '0.5rem',
      padding: '0.35rem 0.85rem',
      borderRadius: '20px',
      background: 'rgba(15, 23, 42, 0.8)',
      border: `1px solid ${isOk ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
      fontSize: '0.8rem',
      fontWeight: '500'
    }}>
      <span style={{
        width: '8px',
        height: '8px',
        borderRadius: '50%',
        backgroundColor: isOk ? 'var(--status-ok)' : 'var(--status-error)',
        boxShadow: `0 0 8px ${isOk ? 'var(--status-ok)' : 'var(--status-error)'}`
      }} />
      <span style={{ color: 'var(--text-muted)' }}>
        System: <strong style={{ color: isOk ? 'var(--text-main)' : 'var(--status-error)' }}>
          {isOk ? 'Online' : 'Connecting...'}
        </strong>
      </span>
    </div>
  );
}