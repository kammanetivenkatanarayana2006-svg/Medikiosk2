export default function Button({ children, onClick, variant = 'primary', disabled = false, type = 'button' }) {
  const styles = {
    base: {
      padding: '12px 24px',
      borderRadius: 'var(--radius-md)',
      border: 'none',
      fontSize: '1rem',
      fontWeight: 600,
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.5 : 1,
      transition: 'var(--transition-fast)',
    },
    primary: {
      background: 'linear-gradient(135deg, var(--color-primary), var(--color-primary-alt))',
      color: '#0b1120',
    },
    ghost: {
      background: 'transparent',
      color: 'var(--color-text)',
      border: '1px solid var(--color-surface-border)',
    },
  }

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      style={{ ...styles.base, ...(variant === 'ghost' ? styles.ghost : styles.primary) }}
    >
      {children}
    </button>
  )
}
