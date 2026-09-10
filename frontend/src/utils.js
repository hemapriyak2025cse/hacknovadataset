export function riskColor(level) {
  switch (level) {
    case 'CRITICAL': return 'text-risk-critical'
    case 'HIGH':     return 'text-risk-high'
    case 'MEDIUM':   return 'text-risk-medium'
    default:         return 'text-risk-low'
  }
}

export function riskBadgeClass(level) {
  switch (level) {
    case 'CRITICAL': return 'badge-critical'
    case 'HIGH':     return 'badge-high'
    case 'MEDIUM':   return 'badge-medium'
    default:         return 'badge-low'
  }
}

export function riskBg(level) {
  switch (level) {
    case 'CRITICAL': return 'bg-risk-critical-bg border-risk-critical/30'
    case 'HIGH':     return 'bg-risk-high-bg border-risk-high/30'
    case 'MEDIUM':   return 'bg-risk-medium-bg border-risk-medium/30'
    default:         return 'bg-risk-low-bg border-risk-low/30'
  }
}

export function statusColor(status) {
  if (status === 'STOPPED') return 'text-risk-critical'
  if (status === 'SLOW')    return 'text-risk-medium'
  return 'text-risk-low'
}

export function fmt(val, fallback = '—') {
  if (val === null || val === undefined || val === '') return fallback
  return val
}

export function fmtNum(val, fallback = '—') {
  if (val === null || val === undefined) return fallback
  return Number(val).toLocaleString()
}
