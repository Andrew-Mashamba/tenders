import React, { useState, useEffect, useMemo, useCallback } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import {
  Search, FileText, Eye, Send, CheckSquare, Square,
  FileDown, Loader2, CheckCircle2, AlertCircle, ChevronDown, ChevronUp,
  XCircle, Clock, Terminal, ExternalLink, Download, Building2,
  Calendar, Mail, Phone, Filter, Bookmark, BookmarkCheck,
  X, MapPin, ArrowUpRight, FileCheck, Printer
} from 'lucide-react'
import { StatusBadge, DaysRemainingBadge } from '../components/StatusBadge'
import { api } from '../lib/api'

// ── Urgency bar color ────────────────────────────────────────────────────────

function urgencyColor(days) {
  if (days === null || days === undefined) return 'border-l-slate-300'
  if (days < 0) return 'border-l-slate-300 opacity-60'
  if (days === 0) return 'border-l-red-500'
  if (days <= 3) return 'border-l-red-500'
  if (days <= 7) return 'border-l-orange-400'
  if (days <= 14) return 'border-l-amber-400'
  return 'border-l-green-400'
}

// ── Job Entry (for batch actions panel) ──────────────────────────────────────

function JobEntry({ job }) {
  const [expanded, setExpanded] = useState(false)

  const statusIcon = {
    running: <Loader2 size={14} className="animate-spin text-blue-500" />,
    queued: <Clock size={14} className="text-slate-400" />,
    completed: <CheckCircle2 size={14} className="text-green-500" />,
    failed: <XCircle size={14} className="text-red-500" />,
    error: <XCircle size={14} className="text-red-500" />,
    timeout: <AlertCircle size={14} className="text-amber-500" />,
  }

  const hasError = job.status === 'failed' || job.status === 'error' || job.status === 'timeout'
  const hasOutput = job.output || job.error

  return (
    <div className={`px-4 py-2.5 ${hasError ? 'bg-red-50/50' : ''}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-sm min-w-0 flex-1">
          {statusIcon[job.status] || <Clock size={14} className="text-slate-400" />}
          <span className="font-mono text-xs text-slate-500">{job.tender_id}</span>
          <span className={`text-xs px-1.5 py-0.5 rounded ${
            job.type === 'prepare' ? 'bg-blue-100 text-blue-700' :
            job.type === 'apply' ? 'bg-green-100 text-green-700' :
            'bg-slate-100 text-slate-600'
          }`}>{job.type}</span>
          {job.returncode !== undefined && job.returncode !== 0 && (
            <span className="text-xs text-red-500">exit={job.returncode}</span>
          )}
        </div>
        {hasOutput && (
          <button onClick={() => setExpanded(!expanded)}
                  className="text-xs text-slate-400 hover:text-slate-600 ml-2">
            {expanded ? 'Hide' : 'Details'}
          </button>
        )}
      </div>
      {expanded && hasOutput && (
        <div className="mt-2 space-y-1">
          {job.output && (
            <pre className="text-xs bg-slate-900 text-green-400 p-3 rounded-lg overflow-x-auto max-h-40 overflow-y-auto font-mono whitespace-pre-wrap">
              {job.output}
            </pre>
          )}
          {job.error && (
            <pre className="text-xs bg-red-900/90 text-red-200 p-3 rounded-lg overflow-x-auto max-h-32 overflow-y-auto font-mono whitespace-pre-wrap">
              {job.error}
            </pre>
          )}
        </div>
      )}
    </div>
  )
}

// ── Tender Card ──────────────────────────────────────────────────────────────

function TenderCard({ tender, isSelected, onToggleSelect, onPrepare, onApply, onView, actionLoading }) {
  const navigate = useNavigate()
  const [expanded, setExpanded] = useState(false)
  const preparing = actionLoading[`prepare_${tender.tender_id}`]
  const applying = actionLoading[`apply_${tender.tender_id}`]
  const contact = tender.contact || {}
  const emails = contact.emails || (contact.email ? (Array.isArray(contact.email) ? contact.email : [contact.email]) : [])
  const docs = tender.documents || []

  return (
    <div className={`bg-white rounded-xl border border-slate-200 border-l-4 ${urgencyColor(tender.days_remaining)} overflow-hidden transition-shadow hover:shadow-md`}>
      {/* Top row: checkbox, title, urgency, actions */}
      <div className="p-4 pb-3">
        <div className="flex items-start gap-3">
          {/* Checkbox */}
          <button onClick={(e) => { e.stopPropagation(); onToggleSelect(tender.tender_id) }}
                  className="mt-0.5 text-slate-400 hover:text-slate-600 shrink-0">
            {isSelected
              ? <CheckSquare size={18} className="text-blue-600" />
              : <Square size={18} />}
          </button>

          {/* Main content */}
          <div className="flex-1 min-w-0">
            {/* Title row */}
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0 flex-1">
                <h3 className="font-semibold text-slate-900 leading-snug cursor-pointer hover:text-blue-600 transition-colors"
                    onClick={() => navigate(`/tenders/${tender.tender_id}`)}>
                  {tender.title}
                </h3>
                <div className="flex flex-wrap items-center gap-x-3 gap-y-1 mt-1.5">
                  <Link to={`/institutions/${tender.institution_slug}`}
                        className="inline-flex items-center gap-1 text-xs text-primary hover:underline"
                        onClick={(e) => e.stopPropagation()}>
                    <Building2 size={12} />
                    {tender.institution_slug || tender.institution}
                  </Link>
                  <span className="text-xs text-slate-400 font-mono">{tender.tender_id}</span>
                  {tender.category && (
                    <span className="text-xs px-1.5 py-0.5 bg-slate-100 text-slate-600 rounded">{tender.category}</span>
                  )}
                </div>
              </div>

              {/* Urgency / deadline - prominent */}
              <div className="shrink-0 text-right">
                <DaysRemainingBadge days={tender.days_remaining} />
                {tender.closing_date && (
                  <p className="text-[11px] text-slate-400 mt-0.5">
                    {tender.closing_date}{tender.closing_time ? ` ${tender.closing_time}` : ''}
                  </p>
                )}
              </div>
            </div>

            {/* Description preview */}
            {tender.description && (
              <p className="text-sm text-slate-500 mt-2 line-clamp-2 leading-relaxed">{tender.description}</p>
            )}

            {/* Quick info row */}
            <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5 mt-3">
              {/* Documents count */}
              <span className="inline-flex items-center gap-1 text-xs text-slate-500">
                <FileText size={13} className={docs.length > 0 ? 'text-blue-500' : 'text-slate-300'} />
                {docs.length} document{docs.length !== 1 ? 's' : ''}
              </span>

              {/* Published date */}
              {tender.published_date && (
                <span className="inline-flex items-center gap-1 text-xs text-slate-400">
                  <Calendar size={12} />
                  Published {tender.published_date}
                </span>
              )}

              {/* Contact email */}
              {emails.length > 0 && (
                <a href={`mailto:${emails[0]}`}
                   onClick={(e) => e.stopPropagation()}
                   className="inline-flex items-center gap-1 text-xs text-primary hover:underline">
                  <Mail size={12} />
                  {emails[0]}
                </a>
              )}

              {/* Contact phone */}
              {contact.phone && (
                <span className="inline-flex items-center gap-1 text-xs text-slate-400">
                  <Phone size={12} />
                  {contact.phone}
                </span>
              )}

              {/* Source link */}
              {tender.source_url && (
                <a href={tender.source_url} target="_blank" rel="noopener"
                   onClick={(e) => e.stopPropagation()}
                   className="inline-flex items-center gap-1 text-xs text-primary hover:underline">
                  <ExternalLink size={12} />
                  Source
                </a>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Documents & Actions bar */}
      <div className="px-4 py-2.5 bg-slate-50/70 border-t border-slate-100 flex items-center justify-between gap-3">
        {/* Documents - inline list */}
        <div className="flex-1 min-w-0">
          {docs.length > 0 ? (
            <div className="flex items-center gap-2 overflow-x-auto">
              {docs.slice(0, 3).map((doc, i) => (
                <a key={i}
                   href={doc.original_url || '#'}
                   target="_blank" rel="noopener"
                   onClick={(e) => e.stopPropagation()}
                   className="inline-flex items-center gap-1.5 px-2.5 py-1.5 text-xs bg-white border border-slate-200 rounded-lg text-slate-700 hover:border-blue-300 hover:text-blue-700 transition-colors shrink-0 max-w-[200px]"
                   title={doc.filename}>
                  <Download size={12} className="shrink-0 text-blue-500" />
                  <span className="truncate">{doc.filename}</span>
                </a>
              ))}
              {docs.length > 3 && (
                <button onClick={(e) => { e.stopPropagation(); setExpanded(!expanded) }}
                        className="text-xs text-primary hover:underline shrink-0">
                  +{docs.length - 3} more
                </button>
              )}
            </div>
          ) : (
            <span className="text-xs text-slate-400">No documents attached</span>
          )}
        </div>

        {/* Action buttons */}
        <div className="flex items-center gap-1.5 shrink-0">
          <button
            onClick={(e) => { e.stopPropagation(); onPrepare(tender.tender_id) }}
            disabled={preparing}
            title="Prepare application document"
            className="inline-flex items-center gap-1 px-2.5 py-1.5 text-xs font-medium rounded-lg
              bg-blue-50 text-blue-700 hover:bg-blue-100 border border-blue-200
              disabled:opacity-50 transition-colors">
            {preparing ? <Loader2 size={12} className="animate-spin" /> : <FileDown size={12} />}
            Prepare
          </button>

          <button
            onClick={(e) => { e.stopPropagation(); onView(tender.tender_id) }}
            title="View application PDF"
            className="inline-flex items-center gap-1 px-2.5 py-1.5 text-xs font-medium rounded-lg
              bg-slate-50 text-slate-700 hover:bg-slate-100 border border-slate-200 transition-colors">
            <Eye size={12} />
            View
          </button>

          <button
            onClick={(e) => { e.stopPropagation(); onApply(tender.tender_id) }}
            disabled={applying}
            title="Generate & send application"
            className="inline-flex items-center gap-1 px-2.5 py-1.5 text-xs font-medium rounded-lg
              bg-green-50 text-green-700 hover:bg-green-100 border border-green-200
              disabled:opacity-50 transition-colors">
            {applying ? <Loader2 size={12} className="animate-spin" /> : <Send size={12} />}
            Apply
          </button>
        </div>
      </div>

      {/* Expanded documents list */}
      {expanded && docs.length > 3 && (
        <div className="px-4 py-3 bg-slate-50 border-t border-slate-100 space-y-1.5">
          {docs.slice(3).map((doc, i) => (
            <a key={i}
               href={doc.original_url || '#'}
               target="_blank" rel="noopener"
               className="flex items-center gap-2 p-2 bg-white rounded-lg border border-slate-200 text-sm hover:border-blue-300 transition-colors">
              <Download size={14} className="text-blue-500 shrink-0" />
              <span className="truncate text-slate-700">{doc.filename}</span>
              {doc.content_type && (
                <span className="text-[10px] text-slate-400 shrink-0 ml-auto">{doc.content_type.split('/').pop()}</span>
              )}
            </a>
          ))}
        </div>
      )}
    </div>
  )
}

// ── Tender Detail Slide-Over Panel ───────────────────────────────────────────

function TenderDetailPanel({ tenderId, onClose, onPrepare, onApply, actionLoading }) {
  const [tender, setTender] = useState(null)
  const [loading, setLoading] = useState(true)
  const [docText, setDocText] = useState(null)
  const [showDocText, setShowDocText] = useState(null)
  const wasPreparing = React.useRef(false)

  const fetchTender = useCallback(() => {
    if (!tenderId) return
    api.getTender(tenderId)
      .then(setTender)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [tenderId])

  useEffect(() => {
    setLoading(true)
    setDocText(null)
    setShowDocText(null)
    fetchTender()
  }, [fetchTender])

  // Re-fetch when prepare finishes (preparing goes from true → false)
  const isPreparing = actionLoading[`prepare_${tenderId}`]
  useEffect(() => {
    if (wasPreparing.current && !isPreparing) {
      fetchTender()
    }
    wasPreparing.current = isPreparing
  }, [isPreparing, fetchTender])

  const loadDocText = async (slug, tid, filename) => {
    if (showDocText === filename) { setShowDocText(null); return }
    try {
      const res = await api.getDocumentText(slug, tid, filename)
      setDocText(res.text)
      setShowDocText(filename)
    } catch { setDocText('Could not extract text.'); setShowDocText(filename) }
  }

  if (!tenderId) return null

  const contact = tender?.contact || {}
  const emails = contact.emails || (contact.email ? (Array.isArray(contact.email) ? contact.email : [contact.email]) : [])
  const docs = tender?.documents || []
  const localFiles = tender?.downloadable_docs || []
  const extractedFiles = tender?.extracted_files || []
  const pitch = tender?.pitch
  const appPdf = tender?.application_pdf
  const preparing = actionLoading[`prepare_${tenderId}`]
  const applying = actionLoading[`apply_${tenderId}`]

  return (
    <>
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black/40 z-40 transition-opacity" onClick={onClose} />

      {/* Panel */}
      <div className="fixed inset-y-0 right-0 w-full max-w-2xl bg-white z-50 shadow-2xl flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200 bg-slate-50 shrink-0">
          <div className="flex items-center gap-3">
            <span className="font-mono text-xs text-slate-400">{tenderId}</span>
            {tender && <StatusBadge status={tender.status} />}
            {tender && <DaysRemainingBadge days={tender.days_remaining} />}
          </div>
          <button onClick={onClose} className="p-1.5 hover:bg-slate-200 rounded-lg transition-colors">
            <X size={20} className="text-slate-500" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto">
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <Loader2 size={24} className="animate-spin text-slate-400" />
            </div>
          ) : !tender ? (
            <div className="text-center py-12 text-slate-400">Tender not found</div>
          ) : (
            <div className="p-6 space-y-6">
              {/* Title & Description */}
              <div>
                <h2 className="text-xl font-bold text-slate-900 leading-snug">{tender.title}</h2>
                {tender.reference_number && (
                  <p className="text-sm text-slate-500 mt-1">Ref: {tender.reference_number}</p>
                )}
                {tender.description && (
                  <p className="text-sm text-slate-600 mt-3 leading-relaxed whitespace-pre-line">{tender.description}</p>
                )}
              </div>

              {/* Key Info Grid */}
              <div className="grid sm:grid-cols-2 gap-3">
                <div className="flex items-center gap-2 text-sm">
                  <Building2 size={15} className="text-slate-400 shrink-0" />
                  <Link to={`/institutions/${tender.institution_slug}`}
                        className="text-primary hover:underline">
                    {tender.institution_slug}
                  </Link>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <Calendar size={15} className="text-slate-400 shrink-0" />
                  <span>Published: {tender.published_date || '—'}</span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <Clock size={15} className="text-slate-400 shrink-0" />
                  <span>Closes: {tender.closing_date || 'No deadline'} {tender.closing_time || ''}</span>
                </div>
                {tender.category && (
                  <div className="flex items-center gap-2 text-sm">
                    <FileText size={15} className="text-slate-400 shrink-0" />
                    <span>Category: {tender.category}</span>
                  </div>
                )}
                {tender.source_url && (
                  <div className="flex items-center gap-2 text-sm">
                    <ExternalLink size={15} className="text-slate-400 shrink-0" />
                    <a href={tender.source_url} target="_blank" rel="noopener"
                       className="text-primary hover:underline truncate">View on source website</a>
                  </div>
                )}
                {tender.eligibility && (
                  <div className="flex items-start gap-2 text-sm sm:col-span-2">
                    <FileCheck size={15} className="text-slate-400 shrink-0 mt-0.5" />
                    <span className="text-slate-600">Eligibility: {tender.eligibility}</span>
                  </div>
                )}
              </div>

              {/* Contact */}
              {(emails.length > 0 || contact.phone || contact.address) && (
                <div className="bg-slate-50 rounded-xl p-4 space-y-2">
                  <h3 className="text-sm font-semibold text-slate-700">Contact Information</h3>
                  {contact.name && (
                    <div className="flex items-center gap-2 text-sm text-slate-600">
                      <Building2 size={14} className="text-slate-400" />
                      {contact.name}
                    </div>
                  )}
                  {emails.map((email, i) => (
                    <div key={i} className="flex items-center gap-2 text-sm">
                      <Mail size={14} className="text-slate-400" />
                      <a href={`mailto:${email}`} className="text-primary hover:underline">{email}</a>
                    </div>
                  ))}
                  {contact.phone && (
                    <div className="flex items-center gap-2 text-sm text-slate-600">
                      <Phone size={14} className="text-slate-400" />
                      {contact.phone}
                    </div>
                  )}
                  {contact.address && (
                    <div className="flex items-center gap-2 text-sm text-slate-600">
                      <MapPin size={14} className="text-slate-400" />
                      {contact.address}
                    </div>
                  )}
                </div>
              )}

              {/* Source Documents (from institution) */}
              {docs.length > 0 && (
                <div>
                  <h3 className="text-sm font-semibold text-slate-700 mb-3">
                    <FileText size={15} className="inline mr-1.5 text-blue-500" />
                    Tender Documents ({docs.length})
                  </h3>
                  <div className="space-y-2">
                    {docs.map((doc, i) => (
                      <div key={i} className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-200">
                        <div className="flex items-center gap-3 min-w-0">
                          <FileText size={16} className="text-blue-500 shrink-0" />
                          <div className="min-w-0">
                            <p className="text-sm font-medium text-slate-700 truncate">{doc.filename}</p>
                            <p className="text-xs text-slate-400">{doc.content_type}</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-1.5 shrink-0">
                          {doc.original_url && (
                            <a href={doc.original_url} target="_blank" rel="noopener"
                               className="p-1.5 text-blue-500 hover:bg-blue-50 rounded transition-colors"
                               title="Open original">
                              <ExternalLink size={15} />
                            </a>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Downloaded Files (locally available for download) */}
              {localFiles.length > 0 && (
                <div>
                  <h3 className="text-sm font-semibold text-slate-700 mb-3">
                    <Download size={15} className="inline mr-1.5 text-green-500" />
                    Downloaded Files ({localFiles.length})
                  </h3>
                  <div className="space-y-2">
                    {localFiles.map((file, i) => (
                      <div key={i} className="flex items-center justify-between p-3 rounded-lg bg-green-50/50 border border-green-200">
                        <div className="flex items-center gap-3 min-w-0">
                          <FileText size={16} className="text-green-600 shrink-0" />
                          <p className="text-sm font-medium text-slate-700 truncate">{file.filename}</p>
                        </div>
                        <div className="flex items-center gap-1.5 shrink-0">
                          {extractedFiles.some(f => f.replace('.txt', '') === file.filename.replace(/\.[^.]+$/, '')) && (
                            <button
                              onClick={() => loadDocText(tender.institution_slug, tenderId, file.filename)}
                              className={`p-1.5 rounded transition-colors text-xs ${
                                showDocText === file.filename ? 'bg-amber-100 text-amber-700' : 'text-slate-400 hover:bg-slate-100'
                              }`}
                              title="View extracted text">
                              <Eye size={15} />
                            </button>
                          )}
                          <button
                             onClick={async () => {
                               const headers = {}
                               const token = localStorage.getItem('tenders_access_token')
                               if (token) headers['Authorization'] = `Bearer ${token}`
                               const res = await fetch(file.url, { headers })
                               const blob = await res.blob()
                               const a = document.createElement('a')
                               a.href = URL.createObjectURL(blob)
                               a.download = file.filename
                               a.click()
                               setTimeout(() => URL.revokeObjectURL(a.href), 60000)
                             }}
                             className="p-1.5 text-green-600 hover:bg-green-100 rounded transition-colors"
                             title="Download">
                            <Download size={15} />
                          </button>
                          <button
                             className="p-1.5 text-slate-400 hover:bg-slate-100 rounded transition-colors"
                             title="Print"
                             onClick={async () => {
                               const headers = {}
                               const token = localStorage.getItem('tenders_access_token')
                               if (token) headers['Authorization'] = `Bearer ${token}`
                               const res = await fetch(file.url, { headers })
                               const blob = await res.blob()
                               const blobUrl = URL.createObjectURL(blob)
                               const w = window.open(blobUrl, '_blank')
                               if (w) setTimeout(() => w.print(), 1000)
                               setTimeout(() => URL.revokeObjectURL(blobUrl), 60000)
                             }}>
                            <Printer size={15} />
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                  {/* Extracted text viewer */}
                  {showDocText && docText && (
                    <div className="mt-3 bg-slate-900 rounded-lg p-4 max-h-64 overflow-y-auto">
                      <pre className="text-xs text-green-400 font-mono whitespace-pre-wrap">{docText}</pre>
                    </div>
                  )}
                </div>
              )}

              {/* Prepared Application PDF */}
              <div className="bg-white rounded-xl border-2 border-dashed border-slate-300 p-5">
                <h3 className="text-sm font-semibold text-slate-700 mb-3">
                  <FileDown size={15} className="inline mr-1.5 text-purple-500" />
                  Application Package
                </h3>

                {appPdf ? (
                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg border border-purple-200">
                      <div className="flex items-center gap-3 min-w-0">
                        <FileCheck size={18} className="text-purple-600 shrink-0" />
                        <div className="min-w-0">
                          <p className="text-sm font-medium text-purple-900 truncate">{appPdf.filename}</p>
                          <p className="text-xs text-purple-500">{(appPdf.size / 1024).toFixed(0)} KB — Ready to send</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-1.5 shrink-0">
                        <button
                           onClick={() => api.openAuthenticatedUrl(appPdf.url)}
                           className="inline-flex items-center gap-1 px-3 py-1.5 text-xs font-medium rounded-lg bg-purple-600 text-white hover:bg-purple-700 transition-colors">
                          <Eye size={13} /> View PDF
                        </button>
                        <button
                           onClick={async () => {
                             const headers = {}
                             const token = localStorage.getItem('tenders_access_token')
                             if (token) headers['Authorization'] = `Bearer ${token}`
                             const res = await fetch(appPdf.url, { headers })
                             const blob = await res.blob()
                             const a = document.createElement('a')
                             a.href = URL.createObjectURL(blob)
                             a.download = appPdf.filename || 'application.pdf'
                             a.click()
                             setTimeout(() => URL.revokeObjectURL(a.href), 60000)
                           }}
                           className="p-1.5 text-purple-600 hover:bg-purple-100 rounded transition-colors"
                           title="Download">
                          <Download size={15} />
                        </button>
                        <button
                           className="p-1.5 text-slate-400 hover:bg-slate-100 rounded transition-colors"
                           title="Print"
                           onClick={async () => {
                             const headers = {}
                             const token = localStorage.getItem('tenders_access_token')
                             if (token) headers['Authorization'] = `Bearer ${token}`
                             const res = await fetch(appPdf.url, { headers })
                             const blob = await res.blob()
                             const blobUrl = URL.createObjectURL(blob)
                             const w = window.open(blobUrl, '_blank')
                             if (w) setTimeout(() => w.print(), 1000)
                             setTimeout(() => URL.revokeObjectURL(blobUrl), 60000)
                           }}>
                          <Printer size={15} />
                        </button>
                      </div>
                    </div>

                    {/* Pitch preview */}
                    {pitch && (
                      <PitchPreview pitch={pitch} />
                    )}
                  </div>
                ) : (
                  <div className="text-center py-4">
                    <p className="text-sm text-slate-400 mb-3">No application has been prepared yet.</p>
                    <button
                      onClick={() => onPrepare(tenderId)}
                      disabled={preparing}
                      className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-medium rounded-lg bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 transition-colors">
                      {preparing ? <Loader2 size={14} className="animate-spin" /> : <FileDown size={14} />}
                      {preparing ? 'Preparing...' : 'Prepare Application'}
                    </button>
                  </div>
                )}
              </div>

              {/* Metadata */}
              <div className="text-xs text-slate-400 space-y-1 pt-2 border-t border-slate-100">
                <div>Scraped: {tender.scraped_at || '—'}</div>
                <div>Last checked: {tender.last_checked || '—'}</div>
              </div>
            </div>
          )}
        </div>

        {/* Footer Actions */}
        {tender && (
          <div className="px-6 py-4 border-t border-slate-200 bg-slate-50 shrink-0 flex items-center justify-between gap-3">
            <Link to={`/tenders/${tenderId}`}
                  className="inline-flex items-center gap-1.5 text-sm text-primary hover:underline">
              <ArrowUpRight size={14} />
              Open full page
            </Link>
            <div className="flex items-center gap-2">
              <button
                onClick={() => onPrepare(tenderId)}
                disabled={preparing}
                className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-medium rounded-lg bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 transition-colors">
                {preparing ? <Loader2 size={14} className="animate-spin" /> : <FileDown size={14} />}
                {preparing ? 'Preparing...' : appPdf ? 'Re-Prepare' : 'Prepare'}
              </button>
              <button
                onClick={() => onApply(tenderId)}
                disabled={applying}
                className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-medium rounded-lg bg-green-600 text-white hover:bg-green-700 disabled:opacity-50 transition-colors">
                {applying ? <Loader2 size={14} className="animate-spin" /> : <Send size={14} />}
                {applying ? 'Sending...' : 'Apply & Send'}
              </button>
            </div>
          </div>
        )}
      </div>
    </>
  )
}

// ── Pitch Preview Component ─────────────────────────────────────────────────

function PitchPreview({ pitch }) {
  const [expanded, setExpanded] = useState(false)

  if (!pitch) return null

  return (
    <div className="bg-slate-50 rounded-lg border border-slate-200 overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between px-4 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-100 transition-colors">
        <span>AI-Generated Pitch Preview</span>
        {expanded ? <ChevronUp size={15} /> : <ChevronDown size={15} />}
      </button>
      {expanded && (
        <div className="px-4 pb-4 text-sm text-slate-600 space-y-2">
          {pitch.subject && <p className="font-medium text-slate-800">{pitch.subject}</p>}
          {pitch.executive_summary && <p className="leading-relaxed">{pitch.executive_summary}</p>}
          {pitch.key_points && Array.isArray(pitch.key_points) && (
            <ul className="list-disc list-inside space-y-1 text-slate-500">
              {pitch.key_points.map((point, i) => <li key={i}>{point}</li>)}
            </ul>
          )}
          {pitch.cover_letter && (
            <div className="mt-2 p-3 bg-white rounded-lg border text-xs whitespace-pre-line text-slate-600 max-h-48 overflow-y-auto">
              {pitch.cover_letter}
            </div>
          )}
          {typeof pitch === 'string' && (
            <div className="p-3 bg-white rounded-lg border text-xs whitespace-pre-line text-slate-600 max-h-48 overflow-y-auto">
              {pitch}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// ── Main Tenders Page ────────────────────────────────────────────────────────

export default function Tenders() {
  // All tenders from API — loaded once, never changes
  const [allTenders, setAllTenders] = useState([])
  const [loading, setLoading] = useState(true)

  // UI state
  const [status, setStatus] = useState('active')
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  const [institution, setInstitution] = useState('')
  const [sort, setSort] = useState('closing_date')
  const [page, setPage] = useState(0)
  const [selected, setSelected] = useState(new Set())
  const [selectAll, setSelectAll] = useState(false)
  const [actionLoading, setActionLoading] = useState({})
  const [batchAction, setBatchAction] = useState(null)
  const [toast, setToast] = useState(null)
  const [jobHistory, setJobHistory] = useState([])
  const [showJobs, setShowJobs] = useState(false)
  const [showFilters, setShowFilters] = useState(false)
  const [viewTenderId, setViewTenderId] = useState(null)
  const PAGE_SIZE = 50

  // ONE fetch on mount — get everything
  useEffect(() => {
    api.getTenders()
      .then(d => setAllTenders(d.tenders || []))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  // Filter options derived from ALL tenders (not filtered subset)
  const filterOptions = useMemo(() => {
    const cats = new Set()
    const insts = new Map()
    for (const t of allTenders) {
      if (t.category) cats.add(t.category)
      if (t.institution_slug) {
        insts.set(t.institution_slug, t.institution_name || t.institution || t.institution_slug)
      }
    }
    return {
      categories: [...cats].sort(),
      institutions: [...insts.entries()]
        .map(([slug, name]) => ({ slug, name }))
        .sort((a, b) => a.name.localeCompare(b.name)),
    }
  }, [allTenders])

  // Everything computed from allTenders + filters — no API calls
  const { filtered, paginated, total } = useMemo(() => {
    let list = allTenders

    // 1. Status
    list = list.filter(t => t.status === status)

    // 2. Search
    if (search) {
      const q = search.toLowerCase()
      list = list.filter(t =>
        `${t.title || ''} ${t.description || ''} ${t.institution || ''} ${t.institution_slug || ''} ${t.tender_id || ''}`
          .toLowerCase().includes(q)
      )
    }

    // 3. Category
    if (category) {
      list = list.filter(t => (t.category || '').toLowerCase() === category.toLowerCase())
    }

    // 4. Institution
    if (institution) {
      list = list.filter(t => t.institution_slug === institution)
    }

    // 5. Sort
    list = [...list]
    if (sort === 'closing_date') {
      list.sort((a, b) => (a.closing_date || '9999-12-31').localeCompare(b.closing_date || '9999-12-31'))
    } else if (sort === 'days_remaining') {
      list.sort((a, b) => (a.days_remaining ?? 9999) - (b.days_remaining ?? 9999))
    } else if (sort === 'title') {
      list.sort((a, b) => (a.title || '').toLowerCase().localeCompare((b.title || '').toLowerCase()))
    } else if (sort === 'institution') {
      list.sort((a, b) => (a.institution_slug || '').localeCompare(b.institution_slug || ''))
    }

    // 6. Paginate
    const start = page * PAGE_SIZE
    return {
      filtered: list,
      paginated: list.slice(start, start + PAGE_SIZE),
      total: list.length,
    }
  }, [allTenders, status, search, category, institution, sort, page])

  // Status counts for tab labels
  const statusCounts = useMemo(() => {
    const counts = { active: 0, closed: 0, archive: 0 }
    for (const t of allTenders) counts[t.status] = (counts[t.status] || 0) + 1
    return counts
  }, [allTenders])

  // Reset page + selection when any filter changes
  const changeStatus = (v) => { setStatus(v); setPage(0); setSelected(new Set()); setSelectAll(false) }
  const changeSearch = (v) => { setSearch(v); setPage(0) }
  const changeCategory = (v) => { setCategory(v); setPage(0) }
  const changeInstitution = (v) => { setInstitution(v); setPage(0) }

  const showToast = (message, type = 'info') => {
    setToast({ message, type })
    setTimeout(() => setToast(null), 5000)
  }

  const toggleSelect = (tenderId) => {
    const next = new Set(selected)
    next.has(tenderId) ? next.delete(tenderId) : next.add(tenderId)
    setSelected(next)
    setSelectAll(next.size === paginated.length && paginated.length > 0)
  }

  const toggleSelectAll = () => {
    if (selectAll) {
      setSelected(new Set())
      setSelectAll(false)
    } else {
      setSelected(new Set(paginated.map(t => t.tender_id)))
      setSelectAll(true)
    }
  }

  // ── Actions ────────────────────────────────────────────────────────────────

  const addJobEntries = (jobs, type) => {
    const entries = jobs.map(j => ({
      ...j, type,
      startedAt: new Date().toLocaleTimeString(),
      status: 'running', output: null, error: null,
    }))
    setJobHistory(prev => [...entries, ...prev].slice(0, 50))
    setShowJobs(true)
  }

  const handlePrepare = async (tenderIds) => {
    const ids = Array.isArray(tenderIds) ? tenderIds : [tenderIds]
    ids.forEach(id => setActionLoading(prev => ({ ...prev, [`prepare_${id}`]: true })))
    try {
      const result = await api.prepareApplications(ids)
      showToast(`Preparing ${result.total} application document(s)...`, 'success')
      if (result.jobs?.length) { addJobEntries(result.jobs, 'prepare'); pollJobs(result.jobs) }
    } catch (e) {
      showToast(`Failed: ${e.message}`, 'error')
      ids.forEach(id => setActionLoading(prev => ({ ...prev, [`prepare_${id}`]: false })))
    }
  }

  const handleApply = async (tenderIds, dryRun = false) => {
    const ids = Array.isArray(tenderIds) ? tenderIds : [tenderIds]
    if (!dryRun && !window.confirm(
      `Send application emails to ${ids.length} tender(s)?\n\nThis will generate PDFs and email them to the tender contacts.`
    )) return

    ids.forEach(id => setActionLoading(prev => ({ ...prev, [`apply_${id}`]: true })))
    try {
      const result = await api.applyToTenders(ids, dryRun)
      showToast(dryRun ? `Dry run started for ${result.total} tender(s)` : `Applying to ${result.total} tender(s)...`, 'success')
      if (result.jobs?.length) { addJobEntries(result.jobs, dryRun ? 'dry-run' : 'apply'); pollJobs(result.jobs) }
    } catch (e) {
      showToast(`Failed: ${e.message}`, 'error')
      ids.forEach(id => setActionLoading(prev => ({ ...prev, [`apply_${id}`]: false })))
    }
  }

  const handleView = (tenderId) => {
    setViewTenderId(tenderId)
  }

  const pollJobs = (jobs) => {
    let attempts = 0
    const interval = setInterval(async () => {
      attempts++
      if (attempts > 120) { clearInterval(interval); return }
      try {
        const result = await api.getJobs()
        setJobHistory(prev => prev.map(entry => {
          const serverJob = result.jobs?.[entry.job_id]
          if (!serverJob) return entry
          return { ...entry, status: serverJob.status, output: serverJob.stdout || null, error: serverJob.stderr || serverJob.error || null, returncode: serverJob.returncode }
        }))
        const allDone = jobs.every(j => {
          const job = result.jobs?.[j.job_id]
          return job && ['completed', 'failed', 'timeout', 'error'].includes(job.status)
        })
        if (allDone) {
          clearInterval(interval)
          const completed = jobs.filter(j => result.jobs?.[j.job_id]?.status === 'completed').length
          const failed = jobs.length - completed
          showToast(`Done: ${completed} succeeded, ${failed} failed`, failed > 0 ? 'warning' : 'success')
          jobs.forEach(j => setActionLoading(prev => ({ ...prev, [`prepare_${j.tender_id}`]: false, [`apply_${j.tender_id}`]: false })))
        }
      } catch {}
    }, 3000)
  }

  // ── Derived ────────────────────────────────────────────────────────────────

  const selectedIds = Array.from(selected)
  const hasSelection = selectedIds.length > 0
  const totalPages = Math.ceil(total / PAGE_SIZE)
  const currentPage = page + 1
  const activeFilters = [category, institution].filter(Boolean).length

  // ── Stats from filtered data ───────────────────────────────────────────────

  const closingSoon = filtered.filter(t => t.days_remaining !== null && t.days_remaining >= 0 && t.days_remaining <= 7).length
  const withDocs = filtered.filter(t => t.documents?.length > 0).length

  return (
    <div className="space-y-4">
      {/* Toast */}
      {toast && (
        <div className={`fixed top-4 right-4 z-50 px-4 py-3 rounded-lg shadow-lg text-sm font-medium flex items-center gap-2
          ${toast.type === 'success' ? 'bg-green-600 text-white' :
            toast.type === 'error' ? 'bg-red-600 text-white' :
            toast.type === 'warning' ? 'bg-amber-500 text-white' :
            'bg-blue-600 text-white'}`}>
          {toast.type === 'success' ? <CheckCircle2 size={16} /> : <AlertCircle size={16} />}
          {toast.message}
        </div>
      )}

      {/* Header */}
      <div className="flex items-start justify-between flex-wrap gap-3">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Tenders</h1>
          <p className="text-sm text-slate-500">
            {total} tenders
            {closingSoon > 0 && <span className="text-red-600 font-medium"> — {closingSoon} closing within 7 days</span>}
            {withDocs > 0 && <span> — {withDocs} with documents</span>}
          </p>
        </div>

        {/* Batch actions */}
        <div className="flex items-center gap-2 flex-wrap">
          {hasSelection && (
            <span className="text-xs text-blue-600 font-medium mr-1">{selectedIds.length} selected</span>
          )}
          <button onClick={toggleSelectAll}
                  className="inline-flex items-center gap-1.5 px-3 py-2 text-sm rounded-lg border border-slate-300 text-slate-600 hover:bg-slate-50 transition-colors">
            {selectAll ? <CheckSquare size={15} className="text-blue-600" /> : <Square size={15} />}
            {selectAll ? 'Deselect All' : 'Select All'}
          </button>
          <button
            onClick={() => handlePrepare(hasSelection ? selectedIds : paginated.map(t => t.tender_id))}
            disabled={batchAction === 'prepare'}
            className="inline-flex items-center gap-1.5 px-3 py-2 text-sm font-medium rounded-lg bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 transition-colors">
            <FileDown size={15} />
            {hasSelection ? `Prepare (${selectedIds.length})` : 'Prepare All'}
          </button>
          <button
            onClick={() => handleApply(hasSelection ? selectedIds : paginated.map(t => t.tender_id))}
            disabled={batchAction === 'apply'}
            className="inline-flex items-center gap-1.5 px-3 py-2 text-sm font-medium rounded-lg bg-green-600 text-white hover:bg-green-700 disabled:opacity-50 transition-colors">
            <Send size={15} />
            {hasSelection ? `Apply (${selectedIds.length})` : 'Apply All'}
          </button>
        </div>
      </div>

      {/* Search + Filters */}
      <div className="flex flex-wrap gap-3">
        <div className="relative flex-1 min-w-[220px] max-w-lg">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search by title, description, institution..."
            value={search}
            onChange={(e) => changeSearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2.5 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-500"
          />
        </div>

        <div className="inline-flex rounded-lg border border-slate-300 overflow-hidden">
          {[
            { value: 'active', label: 'Active' },
            { value: 'closed', label: 'Closed' },
            { value: 'archive', label: 'Archived' },
          ].map(tab => (
            <button key={tab.value}
              onClick={() => changeStatus(tab.value)}
              className={`px-3 py-2 text-sm font-medium transition-colors ${
                status === tab.value
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-slate-600 hover:bg-slate-50'
              }`}>
              {tab.label}
              <span className={`ml-1.5 text-xs ${status === tab.value ? 'text-blue-200' : 'text-slate-400'}`}>
                {statusCounts[tab.value] || 0}
              </span>
            </button>
          ))}
        </div>

        <select value={sort} onChange={(e) => setSort(e.target.value)}
                className="px-3 py-2.5 text-sm border border-slate-300 rounded-lg">
          <option value="closing_date">Closing Soonest</option>
          <option value="days_remaining">Most Urgent</option>
          <option value="title">Title A-Z</option>
          <option value="institution">Institution</option>
        </select>

        <button onClick={() => setShowFilters(!showFilters)}
                className={`inline-flex items-center gap-1.5 px-3 py-2.5 text-sm border rounded-lg transition-colors ${
                  activeFilters > 0 ? 'border-blue-300 bg-blue-50 text-blue-700' : 'border-slate-300 text-slate-600 hover:bg-slate-50'
                }`}>
          <Filter size={15} />
          Filters
          {activeFilters > 0 && (
            <span className="w-5 h-5 bg-blue-600 text-white rounded-full text-[10px] flex items-center justify-center">{activeFilters}</span>
          )}
        </button>
      </div>

      {/* Extended filters */}
      {showFilters && (
        <div className="flex flex-wrap gap-3 p-3 bg-slate-50 rounded-lg border border-slate-200">
          <select
            value={category}
            onChange={(e) => changeCategory(e.target.value)}
            className="px-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/30"
          >
            <option value="">All Categories</option>
            {filterOptions.categories.map(c => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
          <select
            value={institution}
            onChange={(e) => changeInstitution(e.target.value)}
            className="px-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/30"
          >
            <option value="">All Institutions</option>
            {filterOptions.institutions.map(i => (
              <option key={i.slug} value={i.slug}>{i.name}</option>
            ))}
          </select>
          {(category || institution) && (
            <button onClick={() => { changeCategory(''); changeInstitution('') }}
                    className="text-xs text-red-600 hover:underline px-2">
              Clear filters
            </button>
          )}
        </div>
      )}

      {/* Selection banner */}
      {hasSelection && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg px-4 py-2 text-sm text-blue-700 flex items-center justify-between">
          <span>{selectedIds.length} tender(s) selected</span>
          <button onClick={() => { setSelected(new Set()); setSelectAll(false) }}
                  className="text-blue-600 hover:text-blue-800 font-medium">Clear</button>
        </div>
      )}

      {/* Jobs panel */}
      {jobHistory.length > 0 && (
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <button onClick={() => setShowJobs(!showJobs)}
                  className="w-full flex items-center justify-between px-4 py-3 bg-slate-50 hover:bg-slate-100 transition-colors">
            <div className="flex items-center gap-2 text-sm font-medium text-slate-700">
              <Terminal size={16} />
              Job Activity
              <span className="text-xs text-slate-400">({jobHistory.length})</span>
              {jobHistory.some(j => j.status === 'running' || j.status === 'queued') && (
                <Loader2 size={14} className="animate-spin text-blue-500" />
              )}
            </div>
            {showJobs ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </button>
          {showJobs && (
            <div className="max-h-80 overflow-y-auto divide-y divide-slate-100">
              {jobHistory.map((job, i) => <JobEntry key={`${job.job_id}-${i}`} job={job} />)}
            </div>
          )}
        </div>
      )}

      {/* Tender cards */}
      {loading ? (
        <div className="py-16 text-center">
          <Loader2 size={24} className="animate-spin text-slate-400 mx-auto" />
          <p className="text-sm text-slate-400 mt-2">Loading tenders...</p>
        </div>
      ) : paginated.length === 0 ? (
        <div className="py-16 text-center">
          <FileText size={32} className="text-slate-300 mx-auto" />
          <p className="text-sm text-slate-400 mt-2">No tenders match your filters</p>
        </div>
      ) : (
        <div className="space-y-3">
          {paginated.map((t) => (
            <TenderCard
              key={t.tender_id}
              tender={t}
              isSelected={selected.has(t.tender_id)}
              onToggleSelect={toggleSelect}
              onPrepare={handlePrepare}
              onApply={handleApply}
              onView={handleView}
              actionLoading={actionLoading}
            />
          ))}
        </div>
      )}

      {/* Pagination */}
      {total > PAGE_SIZE && (
        <div className="flex items-center justify-between py-3">
          <span className="text-xs text-slate-500">
            Showing {page * PAGE_SIZE + 1}–{Math.min((page + 1) * PAGE_SIZE, total)} of {total}
          </span>
          <div className="flex items-center gap-2">
            <button disabled={page <= 0}
                    onClick={() => setPage(page - 1)}
                    className="px-3 py-1.5 text-xs rounded-lg border border-slate-300 hover:bg-slate-100 disabled:opacity-30">
              Previous
            </button>
            <span className="text-xs text-slate-600">Page {currentPage} of {totalPages}</span>
            <button disabled={currentPage >= totalPages}
                    onClick={() => setPage(page + 1)}
                    className="px-3 py-1.5 text-xs rounded-lg border border-slate-300 hover:bg-slate-100 disabled:opacity-30">
              Next
            </button>
          </div>
        </div>
      )}

      {/* Detail slide-over panel */}
      {viewTenderId && (
        <TenderDetailPanel
          tenderId={viewTenderId}
          onClose={() => setViewTenderId(null)}
          onPrepare={handlePrepare}
          onApply={handleApply}
          actionLoading={actionLoading}
        />
      )}
    </div>
  )
}
