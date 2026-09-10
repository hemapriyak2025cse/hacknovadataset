import { useState, useEffect } from 'react'
import { Search, Bell, Sun, ChevronDown, MapPin } from 'lucide-react'

export default function OperatorHeader() {
  const [clock, setClock]   = useState('')
  const [dateStr, setDate]  = useState('')

  useEffect(() => {
    const tick = () => {
      const now = new Date()
      setClock(now.toLocaleTimeString('en-IN', {
        hour: '2-digit', minute: '2-digit', second: '2-digit',
        hour12: false, timeZone: 'Asia/Kolkata',
      }))
      setDate(now.toLocaleDateString('en-IN', {
        weekday: 'short', day: 'numeric', month: 'short', year: 'numeric',
        timeZone: 'Asia/Kolkata',
      }))
    }
    tick()
    const id = setInterval(tick, 1000)
    return () => clearInterval(id)
  }, [])

  return (
    <header
      className="shrink-0 sticky top-0 z-30 flex items-center justify-between gap-4 px-6"
      style={{
        height: '60px',
        background: '#FDFCFB',
        borderBottom: '1px solid #E7E5E4',
      }}
    >
      {/* ── Left: title + meta ── */}
      <div className="flex items-center gap-4 min-w-0">
        <div className="min-w-0">
          {/* Title row */}
          <div className="flex items-center gap-2.5 flex-wrap">
            <h1
              className="font-black tracking-tight leading-none truncate"
              style={{ fontSize: '15px', color: '#1C1917' }}
            >
              Chennai Mobility Control Center
            </h1>

            {/* Monitoring Active */}
            <span
              className="hidden sm:inline-flex items-center gap-1.5 px-2.5 py-[3px] rounded-full font-bold uppercase shrink-0"
              style={{
                fontSize: '9px',
                letterSpacing: '0.1em',
                background: 'rgba(13,148,136,0.07)',
                border: '1px solid rgba(13,148,136,0.2)',
                color: '#0F766E',
              }}
            >
              <span
                className="w-1.5 h-1.5 rounded-full animate-beacon shrink-0"
                style={{ background: '#0D9488' }}
              />
              Monitoring Active
            </span>
          </div>

          {/* Sub-row: date · time · zone */}
          <div className="flex items-center gap-2 mt-[3px]">
            <span className="font-mono" style={{ fontSize: '10px', color: '#A8A29E' }}>{dateStr}</span>
            <span style={{ color: '#D6D3D1' }}>·</span>
            <span className="font-mono font-semibold" style={{ fontSize: '10px', color: '#57534E' }}>{clock}</span>
            <span style={{ color: '#D6D3D1' }}>·</span>
            <span
              className="inline-flex items-center gap-1 font-semibold"
              style={{ fontSize: '10px', color: '#A8A29E' }}
            >
              <MapPin size={9} strokeWidth={2} />
              IST · Chennai
            </span>
          </div>
        </div>
      </div>

      {/* ── Right: controls ── */}
      <div className="flex items-center gap-1.5 shrink-0">

        {/* Search */}
        <div className="relative hidden md:block">
          <Search
            size={12}
            strokeWidth={2}
            className="absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none"
            style={{ color: '#A8A29E' }}
          />
          <input
            className="h-8 w-48 pl-8 pr-3 rounded-lg text-[12px] transition-all outline-none"
            style={{
              background: '#F5F2EE',
              border: '1px solid #E7E5E4',
              color: '#1C1917',
            }}
            placeholder="Search routes, buses…"
            onFocus={e => {
              e.target.style.border = '1px solid #E8440A'
              e.target.style.boxShadow = '0 0 0 3px rgba(232,68,10,0.08)'
            }}
            onBlur={e => {
              e.target.style.border = '1px solid #E7E5E4'
              e.target.style.boxShadow = 'none'
            }}
          />
        </div>

        {/* Weather */}
        <div
          className="hidden lg:flex items-center gap-1.5 px-3 rounded-lg font-medium"
          style={{
            height: '32px',
            background: '#F5F2EE',
            border: '1px solid #E7E5E4',
            fontSize: '12px',
            color: '#57534E',
          }}
        >
          <Sun size={12} strokeWidth={2} style={{ color: '#F59E0B' }} />
          <span className="font-bold" style={{ color: '#1C1917' }}>32°C</span>
          <span style={{ color: '#D6D3D1' }}>·</span>
          <span style={{ fontSize: '11px', color: '#A8A29E' }}>Partly cloudy</span>
        </div>

        {/* Notifications */}
        <button
          className="relative flex items-center justify-center rounded-lg transition-colors"
          style={{
            width: '32px', height: '32px',
            background: '#F5F2EE',
            border: '1px solid #E7E5E4',
            color: '#78716C',
          }}
          onMouseEnter={e => e.currentTarget.style.background = '#F0EDE9'}
          onMouseLeave={e => e.currentTarget.style.background = '#F5F2EE'}
        >
          <Bell size={14} strokeWidth={1.75} />
          <span
            className="absolute -top-[4px] -right-[4px] flex items-center justify-center rounded-full font-black text-white"
            style={{
              width: '15px', height: '15px',
              fontSize: '8px',
              background: '#E8440A',
            }}
          >
            3
          </span>
        </button>

        {/* Divider */}
        <div className="w-px h-4 mx-1" style={{ background: '#E7E5E4' }} />

        {/* Profile */}
        <button
          className="flex items-center gap-2 px-2 py-1 rounded-lg transition-colors"
          onMouseEnter={e => e.currentTarget.style.background = '#F5F2EE'}
          onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
        >
          <div
            className="w-7 h-7 rounded-full flex items-center justify-center font-black text-white shrink-0"
            style={{ fontSize: '10px', background: '#E8440A' }}
          >
            OP
          </div>
          <div className="hidden lg:block text-left">
            <div className="font-bold leading-tight" style={{ fontSize: '12px', color: '#1C1917' }}>
              Operator
            </div>
            <div className="leading-tight" style={{ fontSize: '9px', color: '#A8A29E' }}>
              Admin · Zone A
            </div>
          </div>
          <ChevronDown size={11} className="hidden lg:block" style={{ color: '#A8A29E' }} />
        </button>
      </div>
    </header>
  )
}
