import { Routes, Route, Navigate } from 'react-router-dom'
import OperatorSidebar from './components/OperatorSidebar'
import OperatorHeader from './components/OperatorHeader'
import OperatorOverview from './pages/OperatorOverview'
import WhatShouldWeDo from './pages/WhatShouldWeDo'

function Placeholder({ title }) {
  return (
    <div className="flex flex-col items-center justify-center h-64 gap-3">
      <div className="w-10 h-10 rounded-xl bg-charcoal-100 flex items-center justify-center">
        <span className="text-charcoal-300 text-lg">—</span>
      </div>
      <p className="text-[13px] font-semibold text-charcoal-400">{title}</p>
      <span className="text-[10px] uppercase tracking-widest text-charcoal-300 font-bold">Coming soon</span>
    </div>
  )
}

function Layout({ children }) {
  return (
    <div className="flex h-screen overflow-hidden" style={{ background: '#F5F2EE' }}>
      <OperatorSidebar />
      <div className="flex flex-col flex-1 min-w-0 overflow-hidden">
        <OperatorHeader />
        <main className="flex-1 overflow-y-auto px-6 py-5">
          {children}
        </main>
      </div>
    </div>
  )
}

export default function App() {
  return (
    <Routes>
      <Route path="/"                    element={<Navigate to="/operator" replace />} />
      <Route path="/operator"            element={<Layout><OperatorOverview /></Layout>} />
      <Route path="/operator/solutions"  element={<Layout><WhatShouldWeDo /></Layout>} />
      <Route path="/operator/live"       element={<Layout><Placeholder title="Live Bus Network" /></Layout>} />
      <Route path="/operator/risks"      element={<Layout><Placeholder title="Predicted Risks" /></Layout>} />
      <Route path="/operator/recommend"  element={<Layout><Placeholder title="AI Recommendations" /></Layout>} />
      <Route path="/operator/passengers" element={<Layout><Placeholder title="Passengers Affected" /></Layout>} />
      <Route path="/operator/dispatch"   element={<Layout><Placeholder title="Dispatch & Communications" /></Layout>} />
      <Route path="/operator/routes"     element={<Layout><Placeholder title="Routes" /></Layout>} />
      <Route path="/operator/traffic"    element={<Layout><Placeholder title="Traffic & Delays" /></Layout>} />
      <Route path="/operator/analytics"  element={<Layout><Placeholder title="Analytics" /></Layout>} />
      <Route path="/operator/settings"   element={<Layout><Placeholder title="Settings" /></Layout>} />
      <Route path="*"                    element={<Navigate to="/operator" replace />} />
    </Routes>
  )
}
