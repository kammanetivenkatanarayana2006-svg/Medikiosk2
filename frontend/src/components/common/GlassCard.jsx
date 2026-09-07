export default function GlassCard({ children, style = {} }) {
  return (
    <div
      style={{
        background: 'var(--color-surface)',
        backdropFilter: 'var(--blur-glass)',
        WebkitBackdropFilter: 'var(--blur-glass)',
        borderRadius: 'var(--radius-lg)',
        border: '1px solid var(--color-surface-border)',
        boxShadow: 'var(--shadow-glass)',
        padding: 'var(--space-lg)',
        ...style,
      }}
    >
      {children}
    </div>
  )
}
