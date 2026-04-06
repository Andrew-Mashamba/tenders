import React, { useState, useEffect, useCallback } from 'react'
import { Search, ExternalLink, Mail, Briefcase, Handshake, Wrench } from 'lucide-react'
import DataTable from '../components/DataTable'
import StatsCard from '../components/StatsCard'
import { StatusBadge } from '../components/StatusBadge'
import { api } from '../lib/api'

const TYPE_ICONS = { sell: Briefcase, partner: Handshake, build: Wrench }
const TYPE_COLORS = { sell: 'text-blue-600', partner: 'text-green-600', build: 'text-purple-600' }

export default function Opportunities() {
  const [data, setData] = useState({ leads: [], total: 0 })
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [typeFilter, setTypeFilter] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [offset, setOffset] = useState(0)
  const [expanded, setExpanded] = useState(null)

  const fetchData = useCallback(() => {
    setLoading(true)
    const params = { limit: 50, offset }
    if (search) params.search = search
    if (typeFilter) params.opportunity_type = typeFilter
    if (statusFilter) params.status = statusFilter

    api.getOpportunities(params)
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [search, typeFilter, statusFilter, offset])

  useEffect(() => { fetchData() }, [fetchData])

  const columns = [
    {
      header: 'Institution',
      render: (row) => (
        <div className="max-w-xs">
          <p className="font-medium text-slate-900 truncate">{row.institution_name || row.institution_slug}</p>
          {row.website_url && (
            <a href={row.website_url} target="_blank" rel="noopener"
               className="text-xs text-primary hover:underline inline-flex items-center gap-1">
              <ExternalLink size={10} /> website
            </a>
          )}
        </div>
      )
    },
    {
      header: 'Type',
      render: (row) => {
        const Icon = TYPE_ICONS[row.opportunity_type] || Briefcase
        const color = TYPE_COLORS[row.opportunity_type] || 'text-slate-600'
        return (
          <div className={`flex items-center gap-1.5 text-sm ${color}`}>
            <Icon size={14} />
            <span className="capitalize">{row.opportunity_type || '—'}</span>
          </div>
        )
      }
    },
    {
      header: 'Description',
      render: (row) => (
        <p className="text-sm text-slate-600 truncate max-w-md">
          {row.opportunity_description || '—'}
        </p>
      ),
      className: 'hidden lg:table-cell'
    },
    {
      header: 'Emails',
      render: (row) => (
        <div className="flex flex-wrap gap-1">
          {(row.emails || []).slice(0, 2).map((e, i) => (
            <a key={i} href={`mailto:${e}`}
               className="text-xs text-primary hover:underline inline-flex items-center gap-0.5">
              <Mail size={10} /> {e}
            </a>
          ))}
          {(row.emails || []).length > 2 && (
            <span className="text-xs text-slate-400">+{row.emails.length - 2}</span>
          )}
        </div>
      ),
      className: 'hidden md:table-cell'
    },
    {
      header: 'Status',
      render: (row) => <StatusBadge status={row.status || 'pending'} />,
    },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Opportunities</h1>
        <p className="text-sm text-slate-500">{data.total} business leads</p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3">
        <div className="relative flex-1 min-w-[200px] max-w-md">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text" placeholder="Search opportunities..."
            value={search}
            onChange={(e) => { setSearch(e.target.value); setOffset(0) }}
            className="w-full pl-9 pr-4 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary"
          />
        </div>

        <select value={typeFilter} onChange={(e) => { setTypeFilter(e.target.value); setOffset(0) }}
                className="px-3 py-2 text-sm border border-slate-300 rounded-lg">
          <option value="">All Types</option>
          <option value="sell">Sell</option>
          <option value="partner">Partner</option>
          <option value="build">Build</option>
        </select>

        <select value={statusFilter} onChange={(e) => { setStatusFilter(e.target.value); setOffset(0) }}
                className="px-3 py-2 text-sm border border-slate-300 rounded-lg">
          <option value="">All Status</option>
          <option value="pending">Pending</option>
          <option value="sent">Sent</option>
          <option value="engaged">Engaged</option>
        </select>
      </div>

      <DataTable
        columns={columns}
        data={data.leads}
        total={data.total}
        offset={offset}
        limit={50}
        loading={loading}
        onRowClick={(row) => setExpanded(expanded === row.institution_slug ? null : row.institution_slug)}
        onPageChange={setOffset}
      />

      {/* Expanded lead detail */}
      {expanded && (() => {
        const lead = data.leads.find(l => l.institution_slug === expanded)
        if (!lead) return null
        return (
          <div className="bg-white rounded-xl border border-slate-200 p-5">
            <h3 className="text-sm font-semibold text-slate-700 mb-2">
              Draft Email — {lead.institution_name}
            </h3>
            <p className="text-xs text-slate-500 mb-2">
              Subject: {lead.draft_email_subject}
            </p>
            <pre className="text-xs text-slate-600 bg-slate-50 p-3 rounded-lg whitespace-pre-wrap max-h-48 overflow-y-auto">
              {lead.draft_email_body}
            </pre>
          </div>
        )
      })()}
    </div>
  )
}
