import React, { useState, useEffect } from 'react'
import { Play, Square, RefreshCw, Terminal, CheckCircle, XCircle } from 'lucide-react'
import { api } from '../lib/api'

export default function ScraperControl() {
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(false)
  const [notifications, setNotifications] = useState([])

  const fetchStatus = () => {
    setLoading(true)
    Promise.all([
      api.getScrapeStatus(),
      api.getNotifications(5),
    ])
      .then(([s, n]) => { setStatus(s); setNotifications(n.notifications || []) })
      .catch(console.error)
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    fetchStatus()
    const interval = setInterval(fetchStatus, 10000)
    return () => clearInterval(interval)
  }, [])

  const handleStart = async (slug = null) => {
    setActionLoading(true)
    try {
      const result = await api.startScrape(slug ? { slug } : {})
      alert(result.status === 'already_running'
        ? `Scraper already running (PID ${result.pid})`
        : `Scraper started (PID ${result.pid})`)
      fetchStatus()
    } catch (e) {
      alert('Failed to start: ' + e.message)
    }
    setActionLoading(false)
  }

  const handleStop = async () => {
    setActionLoading(true)
    try {
      const result = await api.stopScrape()
      alert(result.status === 'stopped'
        ? `Scraper stopped (PID ${result.pid})`
        : 'Scraper was not running')
      fetchStatus()
    } catch (e) {
      alert('Failed to stop: ' + e.message)
    }
    setActionLoading(false)
  }

  const running = status?.running
  const state = status?.state?.stats?.scrape || {}

  return (
    <div className="max-w-4xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Scraper Control</h1>
        <p className="text-sm text-slate-500">Manage the tender scraping engine</p>
      </div>

      {/* Status card */}
      <div className={`rounded-xl border p-6 ${running ? 'border-green-200 bg-green-50' : 'border-slate-200 bg-white'}`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`w-3 h-3 rounded-full ${running ? 'bg-green-500 animate-pulse' : 'bg-slate-300'}`} />
            <div>
              <p className="font-semibold text-slate-900">
                {running ? 'Scraper Running' : 'Scraper Idle'}
              </p>
              {running && status?.pid && (
                <p className="text-xs text-slate-500">PID: {status.pid}</p>
              )}
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={fetchStatus}
              disabled={loading}
              className="p-2 rounded-lg border border-slate-300 hover:bg-slate-100 disabled:opacity-50">
              <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
            </button>

            {running ? (
              <button
                onClick={handleStop}
                disabled={actionLoading}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-700 disabled:opacity-50">
                <Square size={16} /> Stop
              </button>
            ) : (
              <button
                onClick={() => handleStart()}
                disabled={actionLoading}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary-dark disabled:opacity-50">
                <Play size={16} /> Start Full Scrape
              </button>
            )}
          </div>
        </div>

        {/* Progress stats */}
        {Object.keys(state).length > 0 && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6">
            <div className="text-center">
              <p className="text-2xl font-bold text-slate-900">{state.institutions_processed || 0}</p>
              <p className="text-xs text-slate-500">Processed</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">{state.tenders_found || 0}</p>
              <p className="text-xs text-slate-500">Tenders Found</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">{state.docs_downloaded || 0}</p>
              <p className="text-xs text-slate-500">Docs Downloaded</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-red-600">{state.failed_batches || 0}</p>
              <p className="text-xs text-slate-500">Failed Batches</p>
            </div>
          </div>
        )}

        {/* Progress bar */}
        {state.total_batches > 0 && (
          <div className="mt-4">
            <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
              <span>Batch {state.completed_batches || 0} of {state.total_batches}</span>
              <span>{((state.completed_batches / state.total_batches) * 100).toFixed(0)}%</span>
            </div>
            <div className="h-2 bg-slate-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-primary rounded-full transition-all duration-500"
                style={{ width: `${((state.completed_batches / state.total_batches) * 100)}%` }}
              />
            </div>
          </div>
        )}
      </div>

      {/* Single institution scrape */}
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">Scrape Single Institution</h3>
        <div className="flex gap-2">
          <input
            type="text"
            id="single-slug"
            placeholder="Institution slug (e.g., crdb-bank)"
            className="flex-1 px-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/30"
          />
          <button
            onClick={() => {
              const slug = document.getElementById('single-slug').value.trim()
              if (slug) handleStart(slug)
            }}
            disabled={actionLoading || running}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800 text-white hover:bg-slate-900 disabled:opacity-50">
            <Play size={16} /> Scrape
          </button>
        </div>
      </div>

      {/* Log output */}
      {status?.last_log_lines?.length > 0 && (
        <div className="bg-slate-900 rounded-xl p-5 overflow-x-auto">
          <h3 className="text-sm font-semibold text-slate-400 mb-3 flex items-center gap-2">
            <Terminal size={16} /> Recent Log
          </h3>
          <pre className="text-xs text-green-400 font-mono leading-relaxed">
            {status.last_log_lines.join('\n')}
          </pre>
        </div>
      )}

      {/* Recent notifications */}
      {notifications.length > 0 && (
        <div className="bg-white rounded-xl border border-slate-200 p-5">
          <h3 className="text-sm font-semibold text-slate-700 mb-3">Recent Notifications</h3>
          <div className="space-y-2">
            {notifications.map((n, i) => (
              <div key={i} className="flex items-center gap-3 p-3 rounded-lg bg-slate-50 text-sm">
                {n._type === 'sent'
                  ? <CheckCircle size={16} className="text-green-500 shrink-0" />
                  : <XCircle size={16} className="text-amber-500 shrink-0" />
                }
                <div className="min-w-0 flex-1">
                  <p className="text-slate-700 truncate">{n.type || n._file}</p>
                  <p className="text-xs text-slate-400">{n.timestamp || n.created_at || '—'}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
