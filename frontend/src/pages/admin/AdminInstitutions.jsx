import React, { useState, useEffect, useCallback } from 'react'
import { Search, CheckCircle, XCircle, Play, Users, FileText, Plus, X } from 'lucide-react'
import DataTable from '../../components/DataTable'
import { StatusBadge } from '../../components/StatusBadge'
import { api } from '../../lib/api'

export default function AdminInstitutions() {
  const [data, setData] = useState({ institutions: [], total: 0 })
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [enabledFilter, setEnabledFilter] = useState('')
  const [offset, setOffset] = useState(0)
  const [toggling, setToggling] = useState(null)
  const [scraping, setScraping] = useState(null)
  const [showAdd, setShowAdd] = useState(false)
  const [addUrl, setAddUrl] = useState('')
  const [addError, setAddError] = useState(null)
  const [adding, setAdding] = useState(false)
  const [createJob, setCreateJob] = useState(null)

  const fetchData = useCallback(() => {
    setLoading(true)
    const params = { limit: 50, offset }
    if (search) params.search = search
    if (enabledFilter !== '') params.enabled = enabledFilter

    api.adminGetInstitutions(params)
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [search, enabledFilter, offset])

  useEffect(() => { fetchData() }, [fetchData])

  const handleToggle = async (e, slug) => {
    e.stopPropagation()
    setToggling(slug)
    try {
      await api.adminToggleInstitution(slug)
      fetchData()
    } catch (err) { console.error(err) }
    setToggling(null)
  }

  const handleScrape = async (e, slug) => {
    e.stopPropagation()
    setScraping(slug)
    try {
      await api.adminTriggerScrape(slug)
    } catch (err) { console.error(err) }
    setTimeout(() => setScraping(null), 3000)
  }

  const pollJob = (jobId) => {
    const interval = setInterval(async () => {
      try {
        const job = await api.adminGetCreateJob(jobId)
        setCreateJob(job)
        if (job.status === 'completed' || job.status === 'completed_partial' || job.status === 'failed') {
          clearInterval(interval)
          setAdding(false)
          fetchData()
        }
      } catch {
        clearInterval(interval)
        setAdding(false)
      }
    }, 3000)
  }

  const handleAddSubmit = async (e) => {
    e.preventDefault()
    setAddError(null)
    setCreateJob(null)
    setAdding(true)
    try {
      const result = await api.adminCreateInstitution({ url: addUrl })
      setCreateJob({ status: 'queued', slug: result.slug })
      setAddUrl('')
      pollJob(result.job_id)
    } catch (err) {
      setAddError(err.message || 'Failed to create institution')
      setAdding(false)
    }
  }

  const columns = [
    {
      header: 'Institution',
      render: (row) => (
        <div>
          <p className="font-medium text-slate-900">{row.name || row.slug}</p>
          <p className="text-xs text-slate-400 font-mono">{row.slug}</p>
        </div>
      ),
    },
    {
      header: 'Category',
      render: (row) => <span className="text-xs text-slate-600">{row.category || '—'}</span>,
      className: 'hidden md:table-cell',
    },
    {
      header: 'Enabled',
      render: (row) => (
        <button
          onClick={(e) => handleToggle(e, row.slug)}
          disabled={toggling === row.slug}
          className="p-1 rounded hover:bg-slate-100 transition-colors"
        >
          {row.enabled !== false
            ? <CheckCircle size={18} className="text-green-500" />
            : <XCircle size={18} className="text-red-400" />
          }
        </button>
      ),
    },
    {
      header: 'Tenders',
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
      header: 'Followers',
      render: (row) => (
        <div className="flex items-center gap-1.5">
          <Users size={14} className="text-slate-400" />
          <span className="text-sm text-slate-600">{row.followers_count}</span>
        </div>
      ),
      className: 'hidden lg:table-cell',
    },
    {
      header: 'Last Scraped',
      render: (row) => (
        <div>
          <p className="text-xs text-slate-500">
            {row.last_scraped ? new Date(row.last_scraped).toLocaleDateString() : 'Never'}
          </p>
          {row.last_scrape_status && <StatusBadge status={row.last_scrape_status} />}
        </div>
      ),
      className: 'hidden md:table-cell',
    },
    {
      header: '',
      render: (row) => (
        <button
          onClick={(e) => handleScrape(e, row.slug)}
          disabled={scraping === row.slug}
          className={`flex items-center gap-1.5 px-3 py-1.5 text-xs rounded-lg border transition-colors ${
            scraping === row.slug
              ? 'border-green-200 bg-green-50 text-green-600'
              : 'border-slate-300 text-slate-600 hover:bg-slate-50'
          }`}
        >
          <Play size={12} />
          {scraping === row.slug ? 'Started' : 'Scrape'}
        </button>
      ),
    },
  ]

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Manage Institutions</h1>
          <p className="text-sm text-slate-500">{data.total} institutions</p>
        </div>
        <button
          onClick={() => setShowAdd(!showAdd)}
          className="flex items-center gap-2 px-4 py-2 bg-primary text-white text-sm font-medium rounded-lg hover:bg-primary/90 transition-colors"
        >
          {showAdd ? <X size={16} /> : <Plus size={16} />}
          {showAdd ? 'Cancel' : 'Add Institution'}
        </button>
      </div>

      {/* Add Institution Form */}
      {showAdd && (
        <div className="bg-white rounded-xl border border-slate-200 p-5 space-y-4">
          <div>
            <h2 className="text-sm font-semibold text-slate-700">Add Institution</h2>
            <p className="text-xs text-slate-400 mt-1">Paste the website URL. AI will visit the site and configure everything automatically.</p>
          </div>

          {addError && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">{addError}</div>
          )}

          {createJob && (
            <div className={`p-3 rounded-lg border text-sm ${
              createJob.status === 'completed' ? 'bg-green-50 border-green-200 text-green-700' :
              createJob.status === 'failed' ? 'bg-red-50 border-red-200 text-red-700' :
              'bg-blue-50 border-blue-200 text-blue-700'
            }`}>
              <div className="flex items-center gap-2">
                {!['completed', 'failed'].includes(createJob.status) && (
                  <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
                )}
                <span className="font-medium">
                  {createJob.status === 'queued' && 'Starting...'}
                  {createJob.status === 'creating_folder' && 'Creating directory structure...'}
                  {createJob.status === 'analyzing' && 'AI is visiting the website...'}
                  {createJob.status === 'scraping' && `"${createJob.institution_name || createJob.slug}" configured — now scraping for tenders...`}
                  {createJob.status === 'completed' && `"${createJob.institution_name || createJob.slug}" added and scraped successfully.`}
                  {createJob.status === 'failed' && `Failed: ${createJob.error || 'Unknown error'}`}
                </span>
              </div>
              {createJob.status === 'analyzing' && (
                <p className="text-xs mt-1 opacity-70">The AI agent is visiting the website, discovering the institution name, finding the tender page, analyzing HTML structure, and configuring scraping selectors. This takes a few minutes.</p>
              )}
              {createJob.status === 'scraping' && (
                <p className="text-xs mt-1 opacity-70">Scraping tender pages, downloading documents, and extracting text. This takes a few minutes.</p>
              )}
              {createJob.status === 'completed' && createJob.scrape_skipped && (
                <p className="text-xs mt-1 opacity-70">Scraping was skipped — the AI determined this site has no procurement section. You can enable it later.</p>
              )}
              {createJob.status === 'completed' && createJob.scrape_error && (
                <p className="text-xs mt-1 opacity-70">{createJob.scrape_error}</p>
              )}
            </div>
          )}

          <form onSubmit={handleAddSubmit} className="flex gap-3">
            <input
              type="text" required
              value={addUrl}
              onChange={(e) => setAddUrl(e.target.value)}
              placeholder="https://www.whizztanzania.com/"
              disabled={adding}
              className="flex-1 px-4 py-2.5 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={adding || !addUrl.trim()}
              className="flex items-center gap-2 px-5 py-2.5 bg-primary text-white text-sm font-medium rounded-lg hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors whitespace-nowrap"
            >
              <Plus size={16} />
              {adding ? 'Working...' : 'Add'}
            </button>
          </form>
        </div>
      )}

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
      </div>

      <DataTable
        columns={columns}
        data={data.institutions}
        total={data.total}
        offset={offset}
        limit={50}
        loading={loading}
        onPageChange={setOffset}
        emptyMessage="No institutions found"
      />
    </div>
  )
}
