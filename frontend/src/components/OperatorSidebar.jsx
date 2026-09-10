import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard, Radio, AlertTriangle, HelpCircle, Brain,
  Users, Send, RouteIcon, Activity, BarChart2, Settings,
  ChevronRight, Zap, Shield
} from 'lucide-react'

const NAV = [
  {
    group: 'Operations',
    items: [
      { to: '/operator',            icon: LayoutDashboard, label: 'Overview' },
      { to: '/operator/live',       icon: Radio,           label: 'Live Bus Network' },
      { to: '/operator/risks',      icon: AlertTriangle,   label: 'Predicted Risks' },
    ],
  },
  {
    group: 'AI Intelligence',
    items: [
      { to: '/operator/solutions',  icon: HelpCircle,      label: 'What Should We Do?' },
      { to: '/operator/recommend',  icon: Brain,           label: 'AI Recommendations' },
    ],
  },
  {
    group: 'Network',
    items: [
      { to: '/operator/passengers', icon: Users,           label: 'Passengers Affected' },
      { to: '/operator/dispatch',   icon: Send,            label: 'Dispatch & Communications' },
      { to: '/operator/routes',     icon: RouteIcon,       label: 'Routes' },
      { to: '/operator/traffic',    icon: Activity,        label: 'Traffic & Delays' },
    ],
  },
  {
    group: 'System',
    items: [
      { to: '/operator/analytics',  icon: BarChart2,       label: 'Analytics' },
      { to: '/operator/settings',   icon: Settings,        label: 'Settings' },
    ],
  },
]

export default function OperatorSidebar() {
  return (
    <aside
      className="h-screen w-[228px] shrink-0 flex flex-col sticky top-0 z-40 overflow-hidden"
      style={{ background: '#1C1917' }}
    >
      {/* ── Brand ─────────────────────────────────────── */}
      <div className="px-5 pt-6 pb-5" style={{ borderBottom: '1px solid #292524' }}>
        <div className="flex items-center gap-3">
          {/* Logo mark */}
          <div className="relative shrink-0 w-9 h-9">
            <div className="absolute inset-0 rounded-xl" style={{ background: '#E8440A' }} />
            <div className="absolute inset-0 flex items-center justify-center">
              <Shield size={16} className="text-white" strokeWidth={2.5} />
            </div>
            {/* route-node dot */}
            <span
              className="absolute -top-[3px] -right-[3px] w-[9px] h-[9px] rounded-full"
              style={{ background: '#0D9488', border: '2px solid #1C1917' }}
            />
          </div>
          <div className="min-w-0">
            <div className="font-black text-[14px] text-white leading-tight tracking-tight">
              TransitShield
            </div>
            <div
              className="text-[9px] font-semibold leading-tight mt-0.5 truncate"
              style={{ color: '#57534E', letterSpacing: '0.08em', textTransform: 'uppercase' }}
            >
              AI-Powered Mobility Intelligence
            </div>
          </div>
        </div>
      </div>

      {/* ── Nav ───────────────────────────────────────── */}
      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-5">
        {NAV.map(({ group, items }) => (
          <div key={group}>
            <p
              className="px-2.5 mb-1.5 font-bold uppercase"
              style={{ fontSize: '9px', letterSpacing: '0.12em', color: '#44403C' }}
            >
              {group}
            </p>
            <div className="space-y-px">
              {items.map(({ to, icon: Icon, label }) => (
                <NavLink
                  key={to}
                  to={to}
                  end={to === '/operator'}
                  className={({ isActive }) =>
                    `flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-[12.5px] font-medium transition-all duration-150 group ${
                      isActive ? 'active-nav' : 'inactive-nav'
                    }`
                  }
                  style={({ isActive }) =>
                    isActive
                      ? { background: '#E8440A', color: '#ffffff' }
                      : {}
                  }
                >
                  {({ isActive }) => (
                    <>
                      <Icon
                        size={13}
                        strokeWidth={isActive ? 2.5 : 1.75}
                        style={{ color: isActive ? '#ffffff' : '#78716C', flexShrink: 0 }}
                      />
                      <span className="flex-1 truncate" style={{ color: isActive ? '#ffffff' : '#A8A29E' }}>
                        {label}
                      </span>
                      {isActive && (
                        <ChevronRight size={10} style={{ color: 'rgba(255,255,255,0.4)', flexShrink: 0 }} />
                      )}
                    </>
                  )}
                </NavLink>
              ))}
            </div>
          </div>
        ))}
      </nav>

      {/* ── Footer ────────────────────────────────────── */}
      <div className="px-3 pb-5 pt-3 space-y-2" style={{ borderTop: '1px solid #292524' }}>
        {/* AI status pill */}
        <div
          className="flex items-center gap-2 px-3 py-2 rounded-lg"
          style={{ background: '#292524' }}
        >
          <span
            className="w-1.5 h-1.5 rounded-full shrink-0 animate-beacon"
            style={{ background: '#0D9488' }}
          />
          <span
            className="font-bold uppercase flex-1"
            style={{ fontSize: '9px', letterSpacing: '0.1em', color: 'rgba(204,251,241,0.6)' }}
          >
            AI System Online
          </span>
          <Zap size={10} style={{ color: '#0D9488', flexShrink: 0 }} />
        </div>

        {/* Operator profile */}
        <div
          className="flex items-center gap-2.5 px-2.5 py-2 rounded-lg cursor-pointer transition-colors"
          style={{ ':hover': { background: '#292524' } }}
          onMouseEnter={e => e.currentTarget.style.background = '#292524'}
          onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
        >
          <div
            className="w-7 h-7 rounded-full flex items-center justify-center text-[10px] font-black text-white shrink-0"
            style={{ background: '#E8440A' }}
          >
            OP
          </div>
          <div className="min-w-0">
            <div className="text-[12px] font-semibold leading-tight truncate" style={{ color: '#D6D3D1' }}>
              Operator
            </div>
            <div className="text-[9px] leading-tight truncate" style={{ color: '#57534E' }}>
              Transit Controller
            </div>
          </div>
        </div>
      </div>
    </aside>
  )
}
