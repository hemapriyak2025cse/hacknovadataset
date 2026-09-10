import { riskBadgeClass } from '../utils'

export default function RiskBadge({ level }) {
  if (!level) return <span className="badge-low">—</span>
  return <span className={riskBadgeClass(level)}>{level}</span>
}
