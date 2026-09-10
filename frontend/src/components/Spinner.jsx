export default function Spinner({ size = 'md' }) {
  const s = size === 'sm' ? 'w-4 h-4' : size === 'lg' ? 'w-8 h-8' : 'w-6 h-6'
  return (
    <div className={`${s} border-2 border-charcoal-200 border-t-accent rounded-full animate-spin`} />
  )
}

export function LoadingCard({ label = 'Loading...' }) {
  return (
    <div className="bg-card border border-charcoal-200 rounded-xl p-6 flex items-center justify-center gap-3 text-charcoal-500 text-sm">
      <Spinner />
      <span>{label}</span>
    </div>
  )
}

export function ErrorCard({ message }) {
  return (
    <div className="bg-risk-high-bg border border-risk-high/30 rounded-xl p-4 text-risk-high text-sm font-medium">
      {message || 'Failed to load data. Is the backend running?'}
    </div>
  )
}
