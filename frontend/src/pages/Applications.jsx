import React, { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, Mail, CheckCircle2, Clock, AlertTriangle, Trash2 } from 'lucide-react'
import DataTable from '../components/DataTable'
import StatsCard from '../components/StatsCard'
import { DaysRemainingBadge } from '../components/StatusBadge'
import { api } from '../lib/api'

const STATUS_COLORS = {
  interested: 'bg-slate-100 text-slate-700',
  preparing: 'bg-yellow-100 text-yellow-700',
  submitted: 'bg-green-100 text-green-700',
  sent: 'bg-blue-100 text-blue-700',
  won: 'bg-emerald-100 text-emerald-700',
  lost: 'bg-red-100 text-red-700',
}

export default function Applications() {
  const navigate = useNavigate()
  const [data, setData] = useState({ applications: [], total: 0 })
  const [sentLog, setSentLog] = useState({ entries: [], total: 0 })
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [offset, setOffset] = useState(0)

  const fetchData = useCallback(() => {
    setLoading(true)
    const params = { limit: 50, offset }
    if (search) params.search = search
    if (statusFilter) params.status = statusFilter

    Promise.all([
      api.getApplications(params),
      api.getSentLog(10),
    ])
      .then(([apps, log]) => { setData(apps); setSentLog(log) })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [search, statusFilter, offset])

  useEffect(() => { fetchData() }, [fetchData])

  const handleStatusChange = async (e, appId) => {
    e.stopPropagation()
    try {
      await api.updateApplication(appId, { status: e.target.value })
      fetchData()
    } catch {}
  }

  const handleDelete = async (e, appId) => {
    e.stopPropagation()
    if (!confirm('Remove this application?')) return
    try {
      await api.deleteApplication(appId)
      fetchData()
    } catch {}
  }

  const allApps = data.applications || []
  const submitted = allApps.filter(a => ['submitted', 'sent'].includes(a.status)).length
  const pending = allApps.filter(a => !['submitted', 'sent'].includes(a.status)).length

  const columns = [
    {
      header: 'Tender',
      render: (row) => (
        <div className="max-w-xs">
          <p className="font-medium text-slate-900 truncate">{row.title || row.tender_id}</p>
          <p className="text-xs text-slate-500 mt-0.5">
            {row.tender_id} — {row.institution_slug}
          </p>
        </div>
      )
    },
    {
      header: 'Status',
      render: (row) => (
        <select
          value={row.status}
          onClick={(e) => e.stopPropagation()}
          onChange={(e) => handleStatusChange(e, row.id)}
          className={`text-xs font-medium px-2 py-1 rounded-lg border-0 cursor-pointer ${STATUS_COLORS[row.status] || STATUS_COLORS.interested}`}
        >
          {Object.keys(STATUS_COLORS).map(s => (
            <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>
          ))}
        </select>
      ),
    },
    {
      header: 'Closing',
      render: (row) => (
        <div>
          <p className="text-sm">{row.closing_date || '—'}</p>
          <DaysRemainingBadge days={row.days_remaining} />
        </div>
      )
    },
    {
      header: 'Category',
      render: (row) => (
        <span className="text-xs text-slate-500">{row.category || '—'}</span>
      ),
      className: 'hidden lg:table-cell'
    },
    {
      header: 'Notes',
      render: (row) => (
        <p className="text-xs text-slate-400 truncate max-w-[150px]">{row.notes || '—'}</p>
      ),
      className: 'hidden xl:table-cell'
    },
    {
      header: '',
      render: (row) => (
        <button
          onClick={(e) => handleDelete(e, row.id)}
          className="text-slate-300 hover:text-red-500 p-1"
        >
          <Trash2 size={14} />
        </button>
      ),
    },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Applications</h1>
        <p className="text-sm text-slate-500">{data.total} applications tracked</p>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard title="Total" value={data.total} icon={Mail} color="primary" />
        <StatsCard title="Submitted" value={submitted} icon={CheckCircle2} color="success" />
        <StatsCard title="Pending" value={pending} icon={Clock} color="warning" />
        <StatsCard title="Tracking" value={allApps.filter(a => a.status === 'interested').length} icon={AlertTriangle} color="info" />
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3">
        <div className="relative flex-1 min-w-[200px] max-w-md">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text" placeholder="Search applications..."
            value={search}
            onChange={(e) => { setSearch(e.target.value); setOffset(0) }}
            className="w-full pl-9 pr-4 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary"
          />
        </div>

        <select value={statusFilter} onChange={(e) => { setStatusFilter(e.target.value); setOffset(0) }}
                className="px-3 py-2 text-sm border border-slate-300 rounded-lg">
          <option value="">All Status</option>
          <option value="interested">Interested</option>
          <option value="preparing">Preparing</option>
          <option value="submitted">Submitted</option>
          <option value="sent">Sent</option>
          <option value="won">Won</option>
          <option value="lost">Lost</option>
        </select>
      </div>

      <DataTable
        columns={columns}
        data={data.applications}
        total={data.total}
        offset={offset}
        limit={50}
        loading={loading}
        onRowClick={(row) => navigate(`/tenders/${row.tender_id}`)}
        onPageChange={setOffset}
      />

      {/* Recent sends */}
      {sentLog.entries?.length > 0 && (
        <div className="bg-white rounded-xl border border-slate-200 p-5">
          <h3 className="text-sm font-semibold text-slate-700 mb-3">Recent Email Activity</h3>
          <div className="space-y-2">
            {sentLog.entries.map((entry, i) => (
              <div key={i} className="flex items-center justify-between text-sm py-2 border-b border-slate-50 last:border-0">
                <div className="min-w-0 flex-1">
                  <p className="font-medium text-slate-700 truncate">{entry.tender_id}</p>
                  <p className="text-xs text-slate-400">{entry.to} — {entry.sent_at?.slice(0, 16)}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
