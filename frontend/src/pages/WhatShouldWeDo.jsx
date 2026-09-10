import { useEffect, useState } from 'react'
import { fetchAlerts, fetchRecommendation, fetchAltBuses } from '../api'
import { fmt, fmtNum, riskBg } from '../utils'
import { LoadingCard, ErrorCard } from '../components/Spinner'
import RiskBadge from '../components/RiskBadge'
import { HelpCircle, CheckCircle, XCircle, AlertTriangle, ChevronDown, ChevronUp, Zap, Users, Clock, Route } from 'lucide-react'

const DATE = '2026-09-10'

export default function WhatShouldWeDo() {
  const [alerts, setAlerts] = useState(null)
  const [selected, setSelected] = useState(null)
  const [rec, setRec] = useState(null)
  const [altBuses, setAltBuses] = useState(null)
  const [loading, setLoading] = useState(true)
  const [recLoading, setRecLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showTrace, setShowTrace] = useState(false)

  useEffect(() => {
    fetchAlerts(DATE)
      .then(r => {
        setAlerts(r.data)
        const first = r.data?.alerts?.[0]
        if (first) loadRec(first.bus_id)
        else setLoading(false)
      })
      .catch(e => { setError(e.message); setLoading(false) })
  }, [])

  function loadRec(busId) {
    setRecLoading(true)
    setSelected(busId)
    Promise.all([
      fetchRecommendation(busId, DATE),
      fetchAltBuses(busId, DATE),
    ])
      .then(([r, a]) => { setRec(r.data); setAltBuses(a.data) })
      .catch(e => setError(e.message))
      .finally(() => { setLoading(false); setRecLoading(false) })
  }

  if (loading) return <LoadingCard label="Loading incident data..." />
  if (error) return <ErrorCard message={`Backend error: ${error}`} />

  const alertList = alerts?.alerts || []
  const candidates = altBuses?.candidate_buses || []
  const options = rec?.intervention_options || []
  const bestOption = rec?.recommended_option

  return (
    <div className="space-y-5 animate-fade-in">
      <div className="flex items-center gap-2">
        <HelpCircle size={18} className="text-brand-orange" />
        <h2 className="text-lg font-bold text-ink">What Should We Do?</h2>
        <span className="px-2 py-0.5 rounded-full bg-brand-orange-light text-brand-orange text-[10px] font-bold uppercase">Ripple Simulator</span>
      </div>

      {alertList.length === 0 ? (
        <div className="card p-8 text-center text-ink-muted">
          <CheckCircle size={32} className="text-risk-low mx-auto mb-2" />
          <p className="font-semibold">No active incidents requiring intervention.</p>
        </div>
      ) : (
        <>
          {/* Bus selector */}
          <div className="card p-4 space-y-2">
            <p className="text-xs font-semibold text-ink-muted uppercase tracking-wide">Select incident bus to simulate</p>
            <div className="flex flex-wrap gap-2">
              {alertList.map(a => (
                <button
                  key={a.bus_id}
                  onClick={() => loadRec(a.bus_id)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold border transition-all ${selected === a.bus_id ? 'bg-brand-orange text-white border-brand-orange' : 'bg-surface-low border-surface-high text-ink hover:border-brand-orange'}`}
                >
                  Bus {a.bus_id} · {a.risk_level}
                </button>
              ))}
            </div>
          </div>

          {recLoading && <LoadingCard label="Computing ripple impact..." />}

          {rec && !recLoading && (
            <>
              {/* Problem context */}
              <div className={`card border-2 p-4 ${riskBg(rec.risk_level)}`}>
                <div className="flex flex-wrap items-center gap-3 text-sm">
                  <AlertTriangle size={16} className="text-risk-high" />
                  <span className="font-bold text-ink">Bus {rec.bus_id}</span>
                  <span className="text-ink-muted">Route {rec.route_id}</span>
                  <span className="text-ink-muted">·</span>
                  <span className="text-ink">{fmt(rec.current_stop)}</span>
                  <RiskBadge level={rec.risk_level} />
                  <span className="font-mono text-xs text-ink-muted">Score: {rec.risk_score}/100</span>
                </div>
                {rec.problem && (
                  <p className="text-xs text-ink-muted mt-2">{rec.problem}</p>
                )}
                {rec.risk_reasons?.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 mt-2">
                    {rec.risk_reasons.map((r, i) => (
                      <span key={i} className="px-2 py-0.5 rounded bg-surface-card border border-surface-high text-[10px] text-ink-muted">{r}</span>
                    ))}
                  </div>
                )}
              </div>

              {/* 3 Options */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Option 1: Do Nothing */}
                <div className="card border-2 border-surface-high p-4 flex flex-col gap-3">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold uppercase text-ink-muted">Option 1</span>
                    <span className="px-2 py-0.5 rounded bg-risk-high-bg text-risk-high text-[10px] font-bold">Not Recommended</span>
                  </div>
                  <div className="flex items-center gap-2 font-bold text-ink">
                    <XCircle size={16} className="text-risk-high" /> Do Nothing
                  </div>
                  <p className="text-xs text-ink-muted">Allow the bus to continue without intervention. Passengers experience full delay.</p>
                  <div className="mt-auto pt-3 border-t border-surface-high space-y-1.5 text-xs font-mono">
                    <div className="flex justify-between"><span className="text-ink-muted">Passengers affected:</span><span className="font-bold text-risk-high">{fmtNum(rec.affected_passengers)}</span></div>
                    <div className="flex justify-between"><span className="text-ink-muted">Downstream stops:</span><span className="font-bold text-ink">{rec.downstream_stops?.length || 0}</span></div>
                    <div className="flex justify-between"><span className="text-ink-muted">Network impact:</span><span className="font-bold text-ink">Contained to route</span></div>
                  </div>
                </div>

                {/* Option 2: Deploy best alternate (AI Recommended) */}
                <div className="card border-2 border-brand-orange p-4 flex flex-col gap-3 relative shadow-elevated">
                  <div className="absolute -top-3 right-4 px-2.5 py-0.5 rounded-full bg-brand-orange text-white text-[10px] font-bold flex items-center gap-1">
                    <Zap size={10} /> AI Recommended
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold uppercase text-brand-orange">Option 2</span>
                    <span className="px-2 py-0.5 rounded bg-risk-low-bg text-risk-low text-[10px] font-bold">Optimal</span>
                  </div>
                  <div className="flex items-center gap-2 font-bold text-ink">
                    <CheckCircle size={16} className="text-risk-low" />
                    Deploy {bestOption ? `Bus ${bestOption.bus_id}` : 'Alternate Bus'}
                  </div>
                  <p className="text-xs text-ink-muted">
                    {bestOption?.explanation || 'Deploy the best available alternate bus to cover downstream stops.'}
                  </p>
                  <div className="mt-auto pt-3 border-t border-brand-orange/20 space-y-1.5 text-xs font-mono">
                    <div className="flex justify-between"><span className="text-ink-muted">ETA:</span><span className="font-bold text-risk-low">{bestOption?.eta_minutes ?? '—'} min</span></div>
                    <div className="flex justify-between"><span className="text-ink-muted">Stops covered:</span><span className="font-bold text-ink">{bestOption?.downstream_stops_covered ?? '—'}</span></div>
                    <div className="flex justify-between"><span className="text-ink-muted">Coverage:</span><span className="font-bold text-ink">{bestOption ? `${Math.round(bestOption.coverage_ratio * 100)}%` : '—'}</span></div>
                    <div className="flex justify-between"><span className="text-ink-muted">Secondary impact:</span><span className="font-bold text-risk-medium">{fmtNum(bestOption?.secondary_pax_impact)} pax</span></div>
                  </div>
                </div>

                {/* Option 3: Second candidate or reroute */}
                {options[1] ? (
                  <div className="card border-2 border-risk-medium/40 p-4 flex flex-col gap-3">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-bold uppercase text-risk-medium">Option 3</span>
                      <span className="px-2 py-0.5 rounded bg-risk-medium-bg text-risk-medium text-[10px] font-bold">⚠ Risky</span>
                    </div>
                    <div className="flex items-center gap-2 font-bold text-ink">
                      <AlertTriangle size={16} className="text-risk-medium" />
                      Deploy Bus {options[1].bus_id}
                    </div>
                    <p className="text-xs text-ink-muted">{options[1].explanation}</p>
                    <div className="mt-auto pt-3 border-t border-risk-medium/20 space-y-1.5 text-xs font-mono">
                      <div className="flex justify-between"><span className="text-ink-muted">ETA:</span><span className="font-bold text-risk-medium">{options[1].eta_minutes} min</span></div>
                      <div className="flex justify-between"><span className="text-ink-muted">Stops covered:</span><span className="font-bold text-ink">{options[1].downstream_stops_covered}</span></div>
                      <div className="flex justify-between"><span className="text-ink-muted">Secondary impact:</span><span className="font-bold text-risk-high">{fmtNum(options[1].secondary_pax_impact)} pax</span></div>
                    </div>
                  </div>
                ) : (
                  <div className="card border-2 border-surface-high p-4 flex flex-col gap-3 opacity-60">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-bold uppercase text-ink-muted">Option 3</span>
                    </div>
                    <div className="font-bold text-ink-muted">No further candidates</div>
                    <p className="text-xs text-ink-muted">No additional alternate buses available for this route.</p>
                  </div>
                )}
              </div>

              {/* All candidates */}
              {candidates.length > 0 && (
                <div className="card p-4 space-y-3">
                  <h3 className="section-title flex items-center gap-2"><Route size={14} /> All Candidate Alternate Buses</h3>
                  <div className="overflow-x-auto">
                    <table className="w-full text-xs">
                      <thead>
                        <tr className="border-b border-surface-high">
                          {['Bus','Route','Distance','ETA','Stops Covered','Coverage','Score'].map(h => (
                            <th key={h} className="text-left py-2 px-2 text-ink-muted font-semibold uppercase tracking-wide text-[10px]">{h}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {candidates.map((c, i) => (
                          <tr key={c.bus_id} className={`border-b border-surface-high/50 ${i === 0 ? 'bg-brand-orange-light' : 'hover:bg-surface-low'}`}>
                            <td className="py-2 px-2 font-mono font-bold text-ink">{c.bus_id} {i === 0 && <span className="text-brand-orange text-[9px]">★ BEST</span>}</td>
                            <td className="py-2 px-2 font-mono text-ink-muted">{c.route_id}</td>
                            <td className="py-2 px-2 font-mono">{c.distance_to_incident_km} km</td>
                            <td className="py-2 px-2 font-mono">{c.eta_minutes} min</td>
                            <td className="py-2 px-2 font-mono">{c.downstream_stops_covered}</td>
                            <td className="py-2 px-2 font-mono">{Math.round(c.coverage_ratio * 100)}%</td>
                            <td className="py-2 px-2 font-mono font-bold text-brand-teal">{c.score}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* AI Decision Trace */}
              <div className="card p-4">
                <button
                  onClick={() => setShowTrace(v => !v)}
                  className="flex items-center justify-between w-full text-left"
                >
                  <span className="section-title flex items-center gap-2">
                    <Zap size={13} /> AI Decision Trace & Telemetry
                  </span>
                  {showTrace ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                </button>
                {showTrace && (
                  <div className="mt-3 pt-3 border-t border-surface-high space-y-3 animate-fade-in">
                    <div className="bg-ink rounded-lg p-3 font-mono text-[11px] text-green-400 space-y-1 max-h-40 overflow-y-auto">
                      <div>[RISK] Bus {rec.bus_id} · Score: {rec.risk_score} · Level: {rec.risk_level}</div>
                      {rec.risk_reasons?.map((r, i) => <div key={i}>[REASON] {r}</div>)}
                      <div>[PASSENGERS] Affected: {rec.affected_passengers} · Downstream stops: {rec.downstream_stops?.length}</div>
                      {rec.weather && <div>[WEATHER] {rec.weather.condition} · {rec.weather.temperature_c}°C · Precip: {rec.weather.precipitation_mm}mm · Wind: {rec.weather.wind_speed_kmh}km/h</div>}
                      {rec.traffic && <div>[TRAFFIC] Source: {rec.traffic.source} · Delay: {rec.traffic.traffic_delay_min}min · Available: {String(rec.traffic.traffic_available)}</div>}
                      {bestOption && <div>[RECOMMEND] Deploy {bestOption.bus_id} · ETA {bestOption.eta_minutes}min · Score {bestOption.overall_score}</div>}
                      <div>[NOTE] {rec.ripple_note}</div>
                    </div>
                    <p className="text-[10px] text-ink-subtle">Model: RandomForestClassifier · Operational Service Risk (NOT mechanical failure prediction)</p>
                  </div>
                )}
              </div>
            </>
          )}
        </>
      )}
    </div>
  )
}
