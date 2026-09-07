export default function Card({ children, style = {} }) {
  return (
    <div
      style={{
        background: 'var(--color-bg-alt)',
        borderRadius: 'var(--radius-lg)',
        padding: 'var(--space-lg)',
        border: '1px solid var(--color-surface-border)',
        ...style,
      }}
    >
      {children}
    </div>
  )
}
