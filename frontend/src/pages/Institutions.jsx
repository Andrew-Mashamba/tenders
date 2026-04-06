import React, { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, CheckCircle, XCircle, FileText, Heart, HeartOff } from 'lucide-react'
import DataTable from '../components/DataTable'
import { StatusBadge } from '../components/StatusBadge'
import UpgradePrompt from '../components/UpgradePrompt'
import { useAuth } from '../lib/auth'
import { api } from '../lib/api'

export default function Institutions() {
  const navigate = useNavigate()
  const { user, refreshUser } = useAuth()
  const [data, setData] = useState({ institutions: [], total: 0 })
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [enabledFilter, setEnabledFilter] = useState('')
  const [tenderFilter, setTenderFilter] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('')
  const [offset, setOffset] = useState(0)
  const [toggling, setToggling] = useState(null)
  const [limitError, setLimitError] = useState(null)

  const fetchData = useCallback(() => {
    setLoading(true)
    const params = { limit: 50, offset }
    if (search) params.search = search
    if (enabledFilter !== '') params.enabled = enabledFilter
    if (tenderFilter !== '') params.has_tenders = tenderFilter
    if (categoryFilter) params.category = categoryFilter

    api.getInstitutions(params)
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [search, enabledFilter, tenderFilter, categoryFilter, offset])

  useEffect(() => { fetchData() }, [fetchData])

  const toggleFollow = async (e, slug, isFollowed) => {
    e.stopPropagation()
    setToggling(slug)
    setLimitError(null)
    try {
      if (isFollowed) {
        await api.unfollowInstitution(slug)
      } else {
        await api.followInstitution(slug)
      }
      fetchData()
      refreshUser()
    } catch (err) {
      if (err.status === 403 && err.data?.error === 'institution_limit') {
        setLimitError(err.data.message)
      }
    }
    setToggling(null)
  }

  const followedCount = data.institutions.filter(i => i.followed).length

  const columns = [
    {
      header: 'Institution',
      render: (row) => (
        <div>
          <p className="font-medium text-slate-900">{row.name || row.slug}</p>
          <p className="text-xs text-slate-400 font-mono">{row.slug}</p>
        </div>
      )
    },
    {
      header: 'Category',
      render: (row) => (
        <span className="text-xs text-slate-600">{row.category || '—'}</span>
      ),
      className: 'hidden md:table-cell'
    },
    {
      header: 'Following',
      render: (row) => (
        <button
          onClick={(e) => toggleFollow(e, row.slug, row.followed)}
          disabled={toggling === row.slug}
          className={`p-1.5 rounded-lg transition-colors ${
            row.followed
              ? 'text-red-500 hover:bg-red-50'
              : 'text-slate-300 hover:text-blue-500 hover:bg-blue-50'
          }`}
        >
          {row.followed ? <Heart size={16} className="fill-current" /> : <HeartOff size={16} />}
        </button>
      ),
    },
    {
      header: 'Enabled',
      render: (row) => row.enabled !== false
        ? <CheckCircle size={16} className="text-green-500" />
        : <XCircle size={16} className="text-red-400" />,
    },
    {
      header: 'Active Tenders',
      render: (row) => (
        <div className="flex items-center gap-1.5">
          <FileText size={14} className={row.active_tenders > 0 ? 'text-blue-500' : 'text-slate-300'} />
          <span className={`text-sm font-medium ${row.active_tenders > 0 ? 'text-blue-700' : 'text-slate-400'}`}>
            {row.active_tenders}
          </span>
        </div>
      ),
    },
    {
      header: 'Last Scraped',
      render: (row) => (
        <div>
          <p className="text-xs text-slate-500">
            {row.last_scraped ? new Date(row.last_scraped).toLocaleDateString() : 'Never'}
          </p>
          {row.last_scrape_status && (
            <StatusBadge status={row.last_scrape_status} />
          )}
        </div>
      ),
      className: 'hidden lg:table-cell'
    },
    {
      header: 'Domain',
      render: (row) => row.domain
        ? <a href={`https://${row.domain}`} target="_blank" rel="noopener"
             className="text-xs text-primary hover:underline">{row.domain}</a>
        : <span className="text-xs text-slate-300">—</span>,
      className: 'hidden xl:table-cell'
    },
  ]

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Institutions</h1>
          <p className="text-sm text-slate-500">
            {data.total} institutions — Following {user?.followed_institutions || 0} / {user?.max_institutions || 10}
          </p>
        </div>
      </div>

      {limitError && (
        <UpgradePrompt message={limitError} feature="more institution follows" />
      )}

      {/* Filters */}
      <div className="flex flex-wrap gap-3">
        <div className="relative flex-1 min-w-[200px] max-w-md">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text" placeholder="Search institutions..."
            value={search}
            onChange={(e) => { setSearch(e.target.value); setOffset(0) }}
            className="w-full pl-9 pr-4 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary"
          />
        </div>

        <select value={enabledFilter} onChange={(e) => { setEnabledFilter(e.target.value); setOffset(0) }}
                className="px-3 py-2 text-sm border border-slate-300 rounded-lg">
          <option value="">All</option>
          <option value="true">Enabled</option>
          <option value="false">Disabled</option>
        </select>

        <select value={tenderFilter} onChange={(e) => { setTenderFilter(e.target.value); setOffset(0) }}
                className="px-3 py-2 text-sm border border-slate-300 rounded-lg">
          <option value="">All</option>
          <option value="true">Has Tenders</option>
          <option value="false">No Tenders</option>
        </select>

        <input
          type="text" placeholder="Category..."
          value={categoryFilter}
          onChange={(e) => { setCategoryFilter(e.target.value); setOffset(0) }}
          className="px-3 py-2 text-sm border border-slate-300 rounded-lg w-32"
        />
      </div>

      <DataTable
        columns={columns}
        data={data.institutions}
        total={data.total}
        offset={offset}
        limit={50}
        loading={loading}
        onRowClick={(row) => navigate(`/institutions/${row.slug}`)}
        onPageChange={setOffset}
      />
    </div>
  )
}
