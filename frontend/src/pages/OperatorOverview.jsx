import {
  Activity, Bus, AlertTriangle, Users, Radio, Clock,
  TrendingUp, ChevronRight, Zap, MapPin, Send,
  ArrowUpRight, ArrowDownRight, MoreHorizontal, Navigation,
  ShieldAlert, Clock3, UserCheck, BarChart3, RouteIcon
} from 'lucide-react'

// ─────────────────────────────────────────────────────────────────────────────
// KPI SECTION
// Placeholder values are clearly marked — replace with real API data later.
// Each card receives: label, value, sub, icon, trend?, variant ('light'|'dark')
// ─────────────────────────────────────────────────────────────────────────────

// Palette constants (mirrors tailwind.config.js tokens)
const C = {
  canvas:      '#F5F2EE',
  card:        '#FDFCFB',
  dark:        '#1C1917',
  dark800:     '#292524',
  dark700:     '#44403C',
  dark500:     '#78716C',
  dark400:     '#A8A29E',
  dark300:     '#D6D3D1',
  dark200:     '#E7E5E4',
  dark100:     '#F5F5F4',
  accent:      '#E8440A',
  accentLight: '#FDF1EC',
  teal:        '#0D9488',
  tealLight:   '#CCFBF1',
  green:       '#16A34A',
  red:         '#DC2626',
  amber:       '#D97706',
}

function TrendBadge({ trend }) {
  if (trend === undefined || trend === null) return null
  const up = trend >= 0
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: '2px',
      fontSize: '10px', fontWeight: 700,
      color: up ? C.green : C.red,
    }}>
      {up ? <ArrowUpRight size={10} /> : <ArrowDownRight size={10} />}
      {Math.abs(trend)}%
    </span>
  )
}

// Light card — warm white surface, thin top accent bar
function KpiCardLight({ icon: Icon, iconColor, accentColor, label, value, valueColor, sub, trend }) {
  return (
    <div style={{
      background: C.card,
      border: `1px solid ${C.dark200}`,
      borderRadius: '12px',
      padding: '18px 20px',
      display: 'flex',
      flexDirection: 'column',
      gap: '12px',
      boxShadow: '0 1px 3px rgba(28,25,23,0.05)',
      transition: 'box-shadow 0.15s',
    }}
      onMouseEnter={e => e.currentTarget.style.boxShadow = '0 4px 16px rgba(28,25,23,0.09)'}
      onMouseLeave={e => e.currentTarget.style.boxShadow = '0 1px 3px rgba(28,25,23,0.05)'}
    >
      {/* Top row: icon + trend */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{
          width: '32px', height: '32px', borderRadius: '8px',
          background: accentColor + '18',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>
          <Icon size={14} strokeWidth={2} style={{ color: accentColor }} />
        </div>
        <TrendBadge trend={trend} />
      </div>
      {/* Value + label */}
      <div>
        <div style={{
          fontSize: '28px', fontWeight: 900, lineHeight: 1,
          letterSpacing: '-0.02em',
          color: valueColor || C.dark,
        }}>{value}</div>
        <div style={{
          fontSize: '9px', fontWeight: 700, textTransform: 'uppercase',
          letterSpacing: '0.1em', color: C.dark400, marginTop: '5px',
        }}>{label}</div>
      </div>
      {/* Footer */}
      <div style={{
        paddingTop: '10px',
        borderTop: `1px solid ${C.dark100}`,
        fontSize: '11px', color: C.dark400,
      }}>{sub}</div>
    </div>
  )
}

// Dark card — charcoal surface, light text
function KpiCardDark({ icon: Icon, iconColor, label, value, valueColor, sub, trend }) {
  return (
    <div style={{
      background: C.dark,
      border: `1px solid ${C.dark800}`,
      borderRadius: '12px',
      padding: '18px 20px',
      display: 'flex',
      flexDirection: 'column',
      gap: '12px',
      boxShadow: '0 1px 3px rgba(0,0,0,0.15)',
    }}>
      {/* Top row: icon + trend */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{
          width: '32px', height: '32px', borderRadius: '8px',
          background: 'rgba(255,255,255,0.07)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>
          <Icon size={14} strokeWidth={2} style={{ color: iconColor || 'rgba(255,255,255,0.5)' }} />
        </div>
        <TrendBadge trend={trend} />
      </div>
      {/* Value + label */}
      <div>
        <div style={{
          fontSize: '28px', fontWeight: 900, lineHeight: 1,
          letterSpacing: '-0.02em',
          color: valueColor || '#ffffff',
        }}>{value}</div>
        <div style={{
          fontSize: '9px', fontWeight: 700, textTransform: 'uppercase',
          letterSpacing: '0.1em', color: C.dark500, marginTop: '5px',
        }}>{label}</div>
      </div>
      {/* Footer */}
      <div style={{
        paddingTop: '10px',
        borderTop: `1px solid ${C.dark800}`,
        fontSize: '11px', color: C.dark500,
      }}>{sub}</div>
    </div>
  )
}

// ── KPI data — PLACEHOLDER values, clearly marked ────────────────────────────
// TODO: replace each `value` with real API data when connected
const KPI_PLACEHOLDER = [
  {
    id: 'network_health',
    variant: 'light',
    icon: Activity,
    iconColor: C.green,
    accentColor: C.green,
    label: 'Network Health',
    value: '87%',           // TODO: from /api/risk aggregate
    valueColor: C.green,
    sub: 'Normal operations',
    trend: 2,
  },
  {
    id: 'active_buses',
    variant: 'dark',
    icon: Bus,
    iconColor: C.accent,
    label: 'Active Buses',
    value: '16',            // TODO: from /api/live-buses count
    sub: '2 slow · 0 stopped',
    trend: null,
  },
  {
    id: 'predicted_risks',
    variant: 'light',
    icon: AlertTriangle,
    iconColor: C.red,
    accentColor: C.red,
    label: 'Predicted Risks',
    value: '4',             // TODO: from /api/risk HIGH+CRITICAL count
    valueColor: C.red,
    sub: '1 critical · 3 high',
    trend: -12,
  },
  {
    id: 'passengers_at_risk',
    variant: 'dark',
    icon: Users,
    iconColor: C.accent,
    label: 'Passengers at Risk',
    value: '1,240',         // TODO: from /api/alerts affected_passengers sum
    valueColor: '#F4A07A',
    sub: 'Across 3 routes',
    trend: -5,
  },
  {
    id: 'active_incidents',
    variant: 'light',
    icon: Radio,
    iconColor: C.amber,
    accentColor: C.amber,
    label: 'Active Incidents',
    value: '2',             // TODO: from /api/alerts count
    sub: 'Require attention',
    trend: null,
  },
  {
    id: 'avg_delay',
    variant: 'dark',
    icon: Clock,
    iconColor: C.teal,
    label: 'Avg Delay',
    value: '8 min',         // TODO: from /api/traffic aggregate
    valueColor: C.tealLight,
    sub: 'Across network',
    trend: 3,
  },
]

function KpiSection() {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(6, 1fr)',
      gap: '12px',
    }}
      className="kpi-grid"
    >
      {KPI_PLACEHOLDER.map(kpi =>
        kpi.variant === 'dark' ? (
          <KpiCardDark key={kpi.id} {...kpi} />
        ) : (
          <KpiCardLight key={kpi.id} {...kpi} />
        )
      )}
    </div>
  )
}

// ─── Section card wrapper ─────────────────────────────────────────────────────
function Panel({ title, badge, icon: Icon, iconClass = 'text-charcoal-400', action, children }) {
  return (
    <div className="bg-card border border-charcoal-200 rounded-xl shadow-card overflow-hidden">
      <div className="flex items-center justify-between px-5 py-3.5 border-b border-charcoal-100">
        <div className="flex items-center gap-2">
          <Icon size={13} strokeWidth={2} className={iconClass} />
          <span className="card-title">{title}</span>
          {badge && (
            <span className="px-1.5 py-0.5 rounded-md bg-charcoal-100 text-charcoal-500 text-[10px] font-bold">{badge}</span>
          )}
        </div>
        {action
          ? <button className="text-[11px] font-semibold text-accent hover:underline flex items-center gap-0.5">{action}<ChevronRight size={11} /></button>
          : <button className="w-6 h-6 flex items-center justify-center rounded-md hover:bg-charcoal-100 text-charcoal-400 transition-colors"><MoreHorizontal size={13} /></button>
        }
      </div>
      <div className="p-5">{children}</div>
    </div>
  )
}

// ─── Risk level pill ──────────────────────────────────────────────────────────
function RiskPill({ level }) {
  const s = {
    HIGH:     'bg-risk-high-bg text-risk-high border-risk-high/20',
    MEDIUM:   'bg-risk-medium-bg text-risk-medium border-risk-medium/20',
    LOW:      'bg-risk-low-bg text-risk-low border-risk-low/20',
    CRITICAL: 'bg-risk-critical-bg text-risk-critical border-risk-critical/20',
  }
  return <span className={`inline-flex px-2 py-0.5 rounded-md text-[10px] font-bold border ${s[level] || s.LOW}`}>{level}</span>
}

// ─── Risk row ─────────────────────────────────────────────────────────────────
function RiskRow({ bus, route, stop, level, score }) {
  const dot = { HIGH: 'bg-risk-high', MEDIUM: 'bg-risk-medium', LOW: 'bg-risk-low', CRITICAL: 'bg-risk-critical' }
  return (
    <div className="flex items-center gap-3 py-2.5 border-b border-charcoal-100 last:border-0">
      <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${dot[level] || 'bg-charcoal-300'}`} />
      <div className="flex-1 min-w-0">
        <div className="text-[12px] font-semibold text-charcoal-900">
          Bus {bus} <span className="text-charcoal-400 font-normal">· {route}</span>
        </div>
        <div className="text-[10px] text-charcoal-400 flex items-center gap-1 mt-0.5">
          <MapPin size={8} strokeWidth={2} />{stop}
        </div>
      </div>
      <div className="text-right shrink-0 space-y-0.5">
        <RiskPill level={level} />
        <div className="text-[9px] text-charcoal-400 font-mono text-right">{score}/100</div>
      </div>
    </div>
  )
}

// ─── Bus table row ────────────────────────────────────────────────────────────
function BusRow({ bus, route, stop, speed, status }) {
  const s = { ON_TIME: 'text-risk-low', SLOW: 'text-risk-medium', STOPPED: 'text-risk-high' }
  return (
    <tr className="border-b border-charcoal-100 hover:bg-charcoal-50/60 transition-colors">
      <td className="py-2.5 px-4 text-[12px] font-bold text-charcoal-900 font-mono">{bus}</td>
      <td className="py-2.5 px-4 text-[11px] text-charcoal-500 font-mono">{route}</td>
      <td className="py-2.5 px-4 text-[12px] text-charcoal-700">{stop}</td>
      <td className="py-2.5 px-4 text-[11px] font-mono text-charcoal-500">{speed} km/h</td>
      <td className="py-2.5 px-4">
        <span className={`text-[11px] font-bold ${s[status] || 'text-charcoal-400'}`}>{status.replace('_', ' ')}</span>
      </td>
    </tr>
  )
}

// ─── Main ─────────────────────────────────────────────────────────────────────
export default function OperatorOverview() {
  return (
    <div className="space-y-5 animate-fade-in pb-10">

      {/* ── Page header ── */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="section-label">Operations Dashboard</span>
            <span className="section-label text-charcoal-300">·</span>
            <span className="section-label text-accent">Demo · 2026-09-10</span>
          </div>
          <h2 className="text-[22px] font-black text-charcoal-900 tracking-tight leading-tight">
            Network Overview
          </h2>
        </div>
        <button className="btn-primary shrink-0">
          <Zap size={13} strokeWidth={2.5} />
          Run AI Analysis
        </button>
      </div>

      {/* ── KPI Cards ── */}
      <KpiSection />

      {/* ── Predicted Service Risk ── */}
      <PredictedServiceRisk />

      {/* ── Row 1: Predicted Risk + What Should We Do ── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">

        <Panel title="Predicted Service Risk" badge="4 active" icon={AlertTriangle} iconClass="text-risk-high" action="View all">
          <div>
            <RiskRow bus="B101" route="R01" stop="Saidapet"  level="HIGH"   score={72} />
            <RiskRow bus="B103" route="R01" stop="Saidapet"  level="HIGH"   score={68} />
            <RiskRow bus="B301" route="R03" stop="Guindy"    level="MEDIUM" score={51} />
            <RiskRow bus="B403" route="R04" stop="Saidapet"  level="MEDIUM" score={48} />
          </div>
        </Panel>

        <Panel title="What Should We Do?" badge="AI Powered" icon={Zap} iconClass="text-accent">
          <div className="space-y-3">
            {/* AI recommendation highlight */}
            <div className="rounded-lg border border-accent/20 bg-accent-light p-4">
              <div className="flex items-center gap-2 mb-2.5">
                <span className="px-2 py-0.5 rounded-md bg-accent text-white text-[9px] font-black uppercase tracking-wide">AI Recommended</span>
                <span className="text-[10px] text-charcoal-400 font-mono">Bus B101 · Route R01</span>
              </div>
              <p className="text-[13px] font-bold text-charcoal-900 leading-snug">Deploy Bus B302 as alternate coverage</p>
              <p className="text-[11px] text-charcoal-500 mt-1">ETA 4 min · 6 downstream stops · 89% coverage</p>
              <div className="flex gap-2 mt-3">
                <button className="btn-primary text-[11px] px-3 py-1.5">Deploy Now</button>
                <button className="btn-secondary text-[11px] px-3 py-1.5">View Options</button>
              </div>
            </div>
            <p className="text-[10px] text-charcoal-400 text-center">Placeholder — Ripple Impact Engine not yet connected</p>
          </div>
        </Panel>
      </div>

      {/* ── Row 2: AI Recommendation + Passengers Affected ── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">

        <Panel title="AI Recommendation" icon={TrendingUp} iconClass="text-teal">
          <div className="flex flex-col items-center justify-center py-8 gap-3">
            {/* Route motif placeholder */}
            <div className="flex items-center gap-1">
              {[...Array(5)].map((_, i) => (
                <span key={i} className={`rounded-full ${i === 2 ? 'w-3 h-3 bg-accent' : 'w-2 h-2 bg-charcoal-200'}`} />
              ))}
            </div>
            <p className="text-[12px] text-charcoal-400 text-center max-w-[220px] leading-relaxed">
              AI-generated intervention recommendations will appear here once the Ripple Impact Engine is connected.
            </p>
            <span className="px-3 py-1 rounded-full border border-charcoal-200 text-[9px] font-bold uppercase tracking-widest text-charcoal-400">
              API integration coming soon
            </span>
          </div>
        </Panel>

        <Panel title="Passengers Affected" badge="Est. 1,240" icon={Users} iconClass="text-charcoal-500">
          <div className="space-y-3.5">
            {[
              { route: 'R01', stop: 'Saidapet → Guindy',    pax: 480, pct: 78 },
              { route: 'R03', stop: 'Guindy → Velachery',   pax: 310, pct: 50 },
              { route: 'R04', stop: 'Saidapet → T Nagar',   pax: 450, pct: 72 },
            ].map(r => (
              <div key={r.route} className="flex items-center gap-3">
                <span className="text-[10px] font-black font-mono text-charcoal-500 w-7 shrink-0">{r.route}</span>
                <div className="flex-1">
                  <div className="flex justify-between mb-1.5">
                    <span className="text-[11px] text-charcoal-600">{r.stop}</span>
                    <span className="text-[11px] font-bold text-charcoal-900">{r.pax}</span>
                  </div>
                  <div className="h-1 bg-charcoal-100 rounded-full overflow-hidden">
                    <div className="h-full bg-accent rounded-full transition-all" style={{ width: `${r.pct}%` }} />
                  </div>
                </div>
              </div>
            ))}
            <p className="text-[10px] text-charcoal-400 pt-1 border-t border-charcoal-100">Placeholder — real passenger data loads from API</p>
          </div>
        </Panel>
      </div>

      {/* ── Row 3: Live Bus Network (2/3) + Dispatch (1/3) ── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">

        {/* Live Bus Network */}
        <div className="lg:col-span-2 bg-card border border-charcoal-200 rounded-xl shadow-card overflow-hidden">
          <div className="flex items-center justify-between px-5 py-3.5 border-b border-charcoal-100">
            <div className="flex items-center gap-2">
              <Navigation size={13} strokeWidth={2} className="text-charcoal-400" />
              <span className="card-title">Live Bus Network</span>
              <span className="px-1.5 py-0.5 rounded-md bg-charcoal-100 text-charcoal-500 text-[10px] font-bold">16 buses</span>
            </div>
            <button className="text-[11px] font-semibold text-accent hover:underline flex items-center gap-0.5">
              View map <ChevronRight size={11} />
            </button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-charcoal-100 bg-charcoal-50/50">
                  {['Bus ID', 'Route', 'Current Stop', 'Speed', 'Status'].map(h => (
                    <th key={h} className="text-left py-2.5 px-4 text-[9px] font-bold uppercase tracking-[0.1em] text-charcoal-400">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                <BusRow bus="B101" route="R01" stop="Saidapet"  speed={12} status="SLOW"    />
                <BusRow bus="B102" route="R01" stop="Saidapet"  speed={28} status="ON_TIME" />
                <BusRow bus="B201" route="R02" stop="Kilpauk"   speed={22} status="ON_TIME" />
                <BusRow bus="B301" route="R03" stop="Guindy"    speed={8}  status="SLOW"    />
                <BusRow bus="B401" route="R04" stop="Saidapet"  speed={14} status="SLOW"    />
                <BusRow bus="B501" route="R05" stop="Koyambedu" speed={20} status="ON_TIME" />
              </tbody>
            </table>
          </div>
          <div className="px-5 py-3 border-t border-charcoal-100">
            <button className="w-full text-center text-[11px] font-semibold text-charcoal-400 hover:text-accent transition-colors">
              Show all 16 buses
            </button>
          </div>
        </div>

        {/* Dispatch & Comms */}
        <Panel title="Dispatch & Comms" icon={Send} iconClass="text-charcoal-400">
          <div className="space-y-3">
            {[
              { msg: 'Deploy B302 to cover R01 downstream', time: '2 min ago', type: 'action' },
              { msg: 'Weather alert: Heavy rain near Guindy', time: '8 min ago', type: 'weather' },
              { msg: 'B103 speed drop detected on R01', time: '12 min ago', type: 'alert' },
            ].map((item, i) => (
              <div key={i} className="flex gap-3">
                <div className="flex flex-col items-center gap-1 shrink-0 pt-0.5">
                  <span className={`w-1.5 h-1.5 rounded-full ${item.type === 'action' ? 'bg-accent' : item.type === 'weather' ? 'bg-teal' : 'bg-risk-high'}`} />
                  {i < 2 && <span className="w-px flex-1 bg-charcoal-100" />}
                </div>
                <div className="pb-3 min-w-0">
                  <p className="text-[12px] text-charcoal-800 font-medium leading-snug">{item.msg}</p>
                  <p className="text-[10px] text-charcoal-400 mt-0.5">{item.time}</p>
                </div>
              </div>
            ))}
            <p className="text-[10px] text-charcoal-400 pt-1 border-t border-charcoal-100">Placeholder — real dispatch data loads from API</p>
          </div>
        </Panel>
      </div>

    </div>
  )
}
