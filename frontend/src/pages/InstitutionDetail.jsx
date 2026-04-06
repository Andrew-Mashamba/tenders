import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import {
  ArrowLeft, ExternalLink, CheckCircle, XCircle,
  FileText, Calendar, Globe
} from 'lucide-react'
import { StatusBadge, DaysRemainingBadge } from '../components/StatusBadge'
import { api } from '../lib/api'

export default function InstitutionDetail() {
  const { slug } = useParams()
  const [institution, setInstitution] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    api.getInstitution(slug)
      .then(setInstitution)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [slug])

  if (loading) {
    return <div className="flex items-center justify-center h-64 animate-pulse text-slate-400">Loading...</div>
  }
  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-500">{error}</p>
        <Link to="/institutions" className="text-primary mt-4 inline-block">Back to institutions</Link>
      </div>
    )
  }

  const inst = institution
  const tenders = inst.active_tenders || []
  const lastScrape = inst.last_scrape || {}

  return (
    <div className="max-w-4xl space-y-6">
      <Link to="/institutions"
            className="inline-flex items-center gap-1 text-sm text-slate-500 hover:text-slate-700">
        <ArrowLeft size={16} /> Back to institutions
      </Link>

      {/* Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-6">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-xl font-bold text-slate-900">{inst.name || slug}</h1>
            <p className="text-sm text-slate-500 font-mono mt-1">{slug}</p>
          </div>
          {inst.enabled !== false
            ? <span className="flex items-center gap-1 text-sm text-green-600"><CheckCircle size={16} /> Enabled</span>
            : <span className="flex items-center gap-1 text-sm text-red-400"><XCircle size={16} /> Disabled</span>
          }
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
          {inst.category && (
            <div className="text-sm"><span className="text-slate-400">Category:</span> {inst.category}</div>
          )}
          {inst.domain && (
            <div className="text-sm flex items-center gap-1">
              <Globe size={14} className="text-slate-400" />
              <a href={`https://${inst.domain}`} target="_blank" rel="noopener"
                 className="text-primary hover:underline">{inst.domain}</a>
            </div>
          )}
          {inst.tender_url && (
            <div className="text-sm flex items-center gap-1">
              <ExternalLink size={14} className="text-slate-400" />
              <a href={inst.tender_url} target="_blank" rel="noopener"
                 className="text-primary hover:underline truncate">Tender page</a>
            </div>
          )}
          {inst.method && (
            <div className="text-sm"><span className="text-slate-400">Method:</span> {inst.method}</div>
          )}
          {inst.schedule && (
            <div className="text-sm"><span className="text-slate-400">Schedule:</span> {inst.schedule}</div>
          )}
        </div>
      </div>

      {/* Last scrape */}
      {Object.keys(lastScrape).length > 0 && (
        <div className="bg-white rounded-xl border border-slate-200 p-5">
          <h3 className="text-sm font-semibold text-slate-700 mb-3">Last Scrape</h3>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3 text-sm">
            <div><span className="text-slate-400">Time:</span> {lastScrape.last_scrape || '—'}</div>
            <div><span className="text-slate-400">Status:</span> {lastScrape.status || '—'}</div>
            <div><span className="text-slate-400">Tenders found:</span> {lastScrape.tenders_found ?? '—'}</div>
            <div><span className="text-slate-400">New tenders:</span> {lastScrape.new_tenders ?? '—'}</div>
            <div><span className="text-slate-400">Docs downloaded:</span> {lastScrape.documents_downloaded ?? '—'}</div>
            {lastScrape.error && (
              <div className="text-red-500 col-span-full">Error: {lastScrape.error}</div>
            )}
          </div>
        </div>
      )}

      {/* Active tenders */}
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">
          Active Tenders ({tenders.length})
        </h3>
        {tenders.length === 0 ? (
          <p className="text-sm text-slate-400">No active tenders</p>
        ) : (
          <div className="space-y-2">
            {tenders.map((t, i) => (
              <Link key={i} to={`/tenders/${t.tender_id}`}
                    className="flex items-center justify-between p-3 rounded-lg hover:bg-slate-50 transition-colors border border-slate-100">
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-slate-900 truncate">{t.title}</p>
                  <div className="flex items-center gap-3 mt-1 text-xs text-slate-500">
                    <span className="font-mono">{t.tender_id}</span>
                    {t.closing_date && (
                      <span className="flex items-center gap-1">
                        <Calendar size={12} /> {t.closing_date}
                      </span>
                    )}
                    {t.documents?.length > 0 && (
                      <span className="flex items-center gap-1">
                        <FileText size={12} /> {t.documents.length} docs
                      </span>
                    )}
                  </div>
                </div>
                <DaysRemainingBadge days={t.days_remaining} />
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
