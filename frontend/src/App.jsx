import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import UploadPage from './pages/UploadPage'
import EmailListPage from './pages/EmailListPage'
import EmailDetailPage from './pages/EmailDetailPage'

function Sidebar() {
  const linkClass = ({ isActive }) =>
    `flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
      isActive
        ? 'bg-primary/10 text-primary'
        : 'text-text-muted hover:bg-surface hover:text-text'
    }`

  return (
    <aside className="w-64 bg-surface border-r border-border flex flex-col min-h-screen">
      <div className="p-6 border-b border-border">
        <h1 className="text-lg font-bold text-text tracking-tight">
          <span className="text-primary">Mail</span>Trace
        </h1>
        <p className="text-xs text-text-dim mt-1">Email Forensic Intelligence</p>
      </div>
      <nav className="flex-1 p-4 space-y-1">
        <NavLink to="/" className={linkClass} end>
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
          </svg>
          Upload Email
        </NavLink>
        <NavLink to="/emails" className={linkClass}>
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
          </svg>
          Analyzed Emails
        </NavLink>
      </nav>
      <div className="p-4 border-t border-border">
        <p className="text-[10px] text-text-dim text-center">
          SIH 2026 — Forensic Platform
        </p>
      </div>
    </aside>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen">
        <Sidebar />
        <main className="flex-1 overflow-auto">
          <Routes>
            <Route path="/" element={<UploadPage />} />
            <Route path="/emails" element={<EmailListPage />} />
            <Route path="/emails/:id" element={<EmailDetailPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
