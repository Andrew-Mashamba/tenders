import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import {
  ArrowLeft, FileText, Calendar, Building2, Mail, Phone,
  MapPin, ExternalLink, Download, Clock, Bookmark, CheckCircle
} from 'lucide-react'
import { StatusBadge, DaysRemainingBadge } from '../components/StatusBadge'
import { api } from '../lib/api'

const STATUSES = ['interested', 'preparing', 'submitted', 'sent', 'won', 'lost']

export default function TenderDetail() {
  const { tenderId } = useParams()
  const [tender, setTender] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [tracking, setTracking] = useState(false)
  const [trackStatus, setTrackStatus] = useState(null)

  useEffect(() => {
    api.getTender(tenderId)
      .then(setTender)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [tenderId])

  const handleTrack = async () => {
    if (!tender) return
    setTracking(true)
    try {
      await api.createApplication({
        tender_id: tenderId,
        institution_slug: tender.institution_slug,
      })
      setTrackStatus('created')
      // Refresh tender to get user_application
      const updated = await api.getTender(tenderId)
      setTender(updated)
    } catch (err) {
      if (err.status === 409) {
        setTrackStatus('already')
      } else {
        setTrackStatus(err.message)
      }
    }
    setTracking(false)
  }

  const handleStatusChange = async (newStatus) => {
    if (!tender?.user_application) return
    try {
      await api.updateApplication(tender.user_application.id, { status: newStatus })
      const updated = await api.getTender(tenderId)
      setTender(updated)
    } catch {}
  }

  if (loading) {
    return <div className="flex items-center justify-center h-64 animate-pulse text-slate-400">Loading...</div>
  }
  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-500">{error}</p>
        <Link to="/tenders" className="text-primary mt-4 inline-block">Back to tenders</Link>
      </div>
    )
  }

  const contact = tender.contact || {}
  const emails = contact.emails || (contact.email ? [contact.email] : [])
  const userApp = tender.user_application

  return (
    <div className="max-w-4xl space-y-6">
      <Link to="/tenders" className="inline-flex items-center gap-1 text-sm text-slate-500 hover:text-slate-700">
        <ArrowLeft size={16} /> Back to tenders
      </Link>

      {/* Header */}
      <div className="bg-white rounded-xl border border-slate-200 p-6">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 text-sm text-slate-500 mb-2">
              <span className="font-mono">{tender.tender_id}</span>
              <StatusBadge status={tender.status} />
              <DaysRemainingBadge days={tender.days_remaining} />
            </div>
            <h1 className="text-xl font-bold text-slate-900">{tender.title}</h1>
            {tender.reference_number && (
              <p className="text-sm text-slate-500 mt-1">Ref: {tender.reference_number}</p>
            )}
          </div>

          {/* Track button */}
          <div className="shrink-0">
            {userApp ? (
              <div className="flex items-center gap-2">
                <select
                  value={userApp.status}
                  onChange={(e) => handleStatusChange(e.target.value)}
                  className="text-sm border border-slate-300 rounded-lg px-2 py-1.5"
                >
                  {STATUSES.map(s => (
                    <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>
                  ))}
                </select>
                <CheckCircle size={16} className="text-green-500" />
              </div>
            ) : (
              <button
                onClick={handleTrack}
                disabled={tracking}
                className="inline-flex items-center gap-1.5 px-3 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                <Bookmark size={14} />
                {tracking ? 'Tracking...' : 'Track Tender'}
              </button>
            )}
            {trackStatus === 'already' && (
              <p className="text-xs text-slate-400 mt-1">Already tracking</p>
            )}
          </div>
        </div>

        {tender.description && (
          <p className="text-sm text-slate-600 mt-4 leading-relaxed">{tender.description}</p>
        )}

        {/* Meta grid */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
          <div className="flex items-center gap-2 text-sm">
            <Building2 size={16} className="text-slate-400" />
            <span>
              <Link to={`/institutions/${tender.institution_slug}`}
                    className="text-primary hover:underline">
                {tender.institution_slug || tender.institution}
              </Link>
            </span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <Calendar size={16} className="text-slate-400" />
            <span>Published: {tender.published_date || '—'}</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <Clock size={16} className="text-slate-400" />
            <span>Closes: {tender.closing_date || '—'} {tender.closing_time || ''}</span>
          </div>
          {tender.category && (
            <div className="flex items-center gap-2 text-sm">
              <FileText size={16} className="text-slate-400" />
              <span>Category: {tender.category}</span>
            </div>
          )}
          {tender.source_url && (
            <div className="flex items-center gap-2 text-sm">
              <ExternalLink size={16} className="text-slate-400" />
              <a href={tender.source_url} target="_blank" rel="noopener"
                 className="text-primary hover:underline truncate">Source</a>
            </div>
          )}
          {tender.eligibility && (
            <div className="flex items-center gap-2 text-sm">
              <span className="text-slate-500">Eligibility: {tender.eligibility}</span>
            </div>
          )}
        </div>
      </div>

      {/* Contact */}
      {emails.length > 0 && (
        <div className="bg-white rounded-xl border border-slate-200 p-5">
          <h3 className="text-sm font-semibold text-slate-700 mb-3">Contact</h3>
          <div className="space-y-2">
            {contact.name && (
              <div className="flex items-center gap-2 text-sm">
                <Building2 size={14} className="text-slate-400" />
                <span>{contact.name}</span>
              </div>
            )}
            {emails.map((email, i) => (
              <div key={i} className="flex items-center gap-2 text-sm">
                <Mail size={14} className="text-slate-400" />
                <a href={`mailto:${email}`} className="text-primary hover:underline">{email}</a>
              </div>
            ))}
            {contact.phone && (
              <div className="flex items-center gap-2 text-sm">
                <Phone size={14} className="text-slate-400" />
                <span>{contact.phone}</span>
              </div>
            )}
            {contact.address && (
              <div className="flex items-center gap-2 text-sm">
                <MapPin size={14} className="text-slate-400" />
                <span>{contact.address}</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Documents */}
      {tender.documents?.length > 0 && (
        <div className="bg-white rounded-xl border border-slate-200 p-5">
          <h3 className="text-sm font-semibold text-slate-700 mb-3">Documents</h3>
          <div className="space-y-2">
            {tender.documents.map((doc, i) => (
              <div key={i} className="flex items-center justify-between p-3 rounded-lg bg-slate-50">
                <div className="flex items-center gap-3 min-w-0">
                  <FileText size={16} className="text-blue-500 shrink-0" />
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-slate-700 truncate">{doc.filename}</p>
                    <p className="text-xs text-slate-400">{doc.content_type}</p>
                  </div>
                </div>
                {doc.original_url && (
                  <a href={doc.original_url} target="_blank" rel="noopener"
                     className="text-primary hover:text-primary-dark p-1">
                    <Download size={16} />
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Metadata */}
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">Metadata</h3>
        <div className="grid sm:grid-cols-2 gap-2 text-xs text-slate-500">
          <div>Scraped: {tender.scraped_at || '—'}</div>
          <div>Last checked: {tender.last_checked || '—'}</div>
          {tender.local_files?.length > 0 && (
            <div>Local files: {tender.local_files.join(', ')}</div>
          )}
        </div>
      </div>
    </div>
  )
}
